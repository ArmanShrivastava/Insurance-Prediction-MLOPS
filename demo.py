import os
import sys
import pandas as pd
import numpy as np

# Ensure project root is on sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.pipline.training_pipeline import TrainPipeline
from src.exception import MyException
from src.logger import logging
from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME

def create_sample_insurance_data():
    """
    Create sample insurance data and insert it into MongoDB
    """
    try:
        logging.info("Creating sample insurance data...")
        
        # Generate sample data
        np.random.seed(42)
        n_samples = 100
        
        data = {
            'age': np.random.randint(18, 80, n_samples),
            'sex': np.random.choice(['male', 'female'], n_samples),
            'bmi': np.random.uniform(15, 45, n_samples),
            'children': np.random.randint(0, 5, n_samples),
            'smoker': np.random.choice(['yes', 'no'], n_samples),
            'region': np.random.choice(['southwest', 'southeast', 'northwest', 'northeast'], n_samples),
            'charges': np.random.uniform(1000, 50000, n_samples),
            'Response': np.random.randint(0, 2, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Connect to MongoDB and insert data
        logging.info(f"Connecting to MongoDB and inserting data into {DATA_INGESTION_COLLECTION_NAME}...")
        mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        collection = mongo_client.database[DATA_INGESTION_COLLECTION_NAME]
        
        # Clear existing data
        collection.delete_many({})
        
        # Insert new data
        records = df.to_dict('records')
        result = collection.insert_many(records)
        
        logging.info(f"✓ Inserted {len(result.inserted_ids)} documents into MongoDB collection: {DATA_INGESTION_COLLECTION_NAME}")
        return df
        
    except Exception as e:
        logging.error(f"Error creating sample data: {str(e)}")
        raise MyException(e, sys) from e

def main():
    """
    Main function to run the demo
    """
    try:
        logging.info("=" * 80)
        logging.info("INSURANCE DATA INGESTION PIPELINE - DEMO")
        logging.info("=" * 80)
        
        # Step 1: Create sample data
        logging.info("\nStep 1: Creating sample insurance data...")
        sample_df = create_sample_insurance_data()
        logging.info(f"Sample data shape: {sample_df.shape}")
        logging.info(f"\nSample data preview:\n{sample_df.head()}")
        
        # Step 2: Run the pipeline
        logging.info("\n" + "=" * 80)
        logging.info("Step 2: Running the training pipeline...")
        logging.info("=" * 80)
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
        
        logging.info("\n" + "=" * 80)
        logging.info("✓ PIPELINE COMPLETED SUCCESSFULLY!")
        logging.info("=" * 80)
        logging.info("\nPipeline Output Artifacts:")
        logging.info(f"  - Feature Store: artifact/*/data_ingestion/feature_store/data.csv")
        logging.info(f"  - Training Data: artifact/*/data_ingestion/ingested/train.csv")
        logging.info(f"  - Testing Data:  artifact/*/data_ingestion/ingested/test.csv")
        
    except Exception as e:
        logging.error(f"Error in demo: {str(e)}")
        raise MyException(e, sys) from e

if __name__ == "__main__":
    main()
