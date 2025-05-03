import sys
from dataclasses import dataclass
import pandas as pd 
import numpy as np
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.utils import save_object
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
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course',
            ]

            num_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='mean')),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
              steps = [
                  ('imputer',SimpleImputer(strategy='most_frequent')),
                  ('onehotencder',OneHotEncoder()),
                  ('scaler',StandardScaler(with_mean=False))
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
         
         try:
             
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            logging.info('the train and test has been read')

            logging.info('obtaining preprocessor')

            preprocessor_obj = self.get_data_transformer_object()

            #def add_total_and_average(df):
             #   df['total'] = df['math_score'] + df['reading_score'] + df['writing_score']
              #  df['average'] = df['total'] / 3
               # return df.drop(columns=['math_score', 'reading_score', 'writing_score'])

            train_data['total'] = train_data['math_score'] + train_data['reading_score'] + train_data['writing_score']
            train_data['average'] = train_data['total']/3
            num = ['math_score','reading_score','writing_score']
            train_data = train_data.drop(columns=num,axis= 1)
            
            test_data['total'] = test_data['math_score'] + test_data['reading_score'] + test_data['writing_score']
            test_data['average'] = test_data['total']/3
            num = ['math_score','reading_score','writing_score']
            test_data = test_data.drop(columns=num,axis= 1)
            target = 'average'
            numerical_features = ['total']
            input_feature_train = train_data.drop(columns=[target],axis = 1)
            target_feature_train = train_data[target]

            input_feature_test = test_data.drop(columns=[target],axis = 1)
            target_feature_test = test_data[target]
            logging.info('applying preprocessing on train and test data')
            
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test)
            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train)
            ]

            test_arr = np.c_[
                input_feature_test_arr,np.array(target_feature_test)

            ]
            logging.info('saved preprocessor objects')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
         except Exception as e:
           raise CustomException(e,sys)
