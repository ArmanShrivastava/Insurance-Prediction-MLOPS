import os
import sys

# Ensure project root is on sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.pipline.training_pipeline import TrainPipeline
from src.exception import MyException
from src.logger import logging

def main():
    """
    Main function to run the training pipeline
    """
    try:
        logging.info("Starting the training pipeline...")
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
        logging.info("Training pipeline completed successfully!")
    except Exception as e:
        logging.error(f"Error in training pipeline: {str(e)}")
        raise MyException(e, sys) from e

if __name__ == "__main__":
    main()
