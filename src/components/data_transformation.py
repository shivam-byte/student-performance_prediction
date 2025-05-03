import sys
from dataclasses import dataclass
import pandas as pd 
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exeption import CustomException
from src.logger import logging
import os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:

            
            numerical_features = ['total']
            categorical_features = [
                'gender',
                'race_ethinicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course',
            ]

            num_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='mean')),
                    ('scaler',StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
              steps = [
                  ('imputer',SimpleImputer(strategy='most_frequent')),
                  ('onehotencder',OneHotEncoder()),
                  ('scaler',StandardScaler())
              ]    
            )
            logging.info('categorical encoding completed')
            logging.info('standard scaling completed')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_features),
                    ('cat_pipeline',cat_pipeline,categorical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
            pass


    def initiate_data_transformation(self,train_path,test_path):
      train_data = pd.read_csv('artifacts/train.csv')
      test_data = pd.read_csv("artifacts/test.csv")
