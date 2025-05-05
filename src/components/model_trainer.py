import os 
import sys
from dataclasses import dataclass

from src.utils import save_object,evaluate_models
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from src.exeption import CustomException
from src.logger import logging

@dataclass
class ModelTrainingConfig:
    triained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig()

    def initiate_model_trainer(self,train_array,test_array,preprocessor_path):
        try:
            logging.info('train and test split started')
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                'linear regression':LinearRegression(),
                'Decision tree':DecisionTreeRegressor(),
                'random forest':RandomForestRegressor(),
                'K-Neighbors':KNeighborsRegressor(),
            }
            params = {
                "Decision tree":{
                    'criterion':['squared_error','absolute_error','poisson'],

                },
                "random forest":{
                    'n_estimators':[8,16,32,64,128]
                  
                },
                'linear regression':{
                    'fit_intercept': [True, False]
                },
                'K-Neighbors':{
                    'n_neighbors':[3,5,7,9,11]}
            }




            model_report:dict = evaluate_models(X_train=X_train,y_train=y_train,X_test = X_test,y_test = y_test,
                                                models=models,param = params)
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("no best model")

            logging.info('best model found on both training and test data')

            save_object(
                file_path=self.model_trainer_config.triained_model_file_path,
                obj = best_model
            )    

            predicted = best_model.predict(X_test)
            r2score = r2_score(y_test,predicted)
            return r2score

        except Exception as e:
            raise CustomException(e,sys)
            pass 