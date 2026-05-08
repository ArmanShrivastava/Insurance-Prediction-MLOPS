from dataclasses import dataclass


@dataclass
class MyModel:
    preprocessing_object: object
    trained_model_object: object
    
    def predict(self, dataframe):
        """
        Preprocess the dataframe and make predictions using the trained model
        :param dataframe: Input dataframe for prediction
        :return: Predictions from the trained model
        """
        processed_dataframe = self.preprocessing_object.transform(dataframe)
        return self.trained_model_object.predict(processed_dataframe)