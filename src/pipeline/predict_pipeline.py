import sys 
import pandas as pd 
from src.utils import load_object
from src.exeption import CustomException

class PredictPipeline:
    def __init__(self):
        pass 

    def predict(self,features):
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            data_scaled = preprocessor.transform(features)
            prediction = model.predict(data_scaled)
            return prediction
        except Exception as e:
            raise CustomException(e,sys)

         

class CustomData:
    def __init__(self,
                 gender:str,
                 race_ethnicity:str,
                 parental_level_of_education:str,
                 lunch:str,
                 test_preparation_course:str,
                 total:int):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education=parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.total = total
    
    def get_data_as_dataframe(self):
        try:
            custum_data_dict = {
                'gender':[self.gender],
                'race_ethnicity':[self.race_ethnicity],
                'parental_level_of_education':[self.parental_level_of_education],
                'lunch':[self.lunch],
                'test_preparation_course':[self.test_preparation_course],
                'total':[self.total]
            }
            return pd.DataFrame(custum_data_dict)
        except Exception as e:
              raise CustomException(e,sys)