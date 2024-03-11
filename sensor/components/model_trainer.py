import os
import sys
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from sensor.entity.config_entity import ModelTrainingConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainingArtifact
from sensor.logger import logging
from sensor import utils
from sensor.exception import SensorException



class ModelTrainer :

    def __init__(self, model_training_config: ModelTrainingConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_training_config = model_training_config
            self.data_transformation_artifact = data_transformation_artifact  

        except Exception as e:
            raise SensorException(e, sys)
    

    def train_model(self, x,y):
        xgb = XGBClassifier()
        xgb.fit(x,y)
        return xgb


    def initiate_model_training(self) -> ModelTrainingArtifact:
        try:
            
            logging.info(f"{'>>'*10}Initiating model training phase...")

            logging.info(f"Loading and preparing the data...")

            # load the data
            train_arr = utils.load_numpy_array(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array(file_path=self.data_transformation_artifact.transformed_test_path)

            # split the data to input features and target
            x_train, y_train = train_arr[:,:-1], train_arr[:, -1]
            x_test, y_test = test_arr[:,:-1], test_arr[:, -1]

            # train the model

            logging.info("Training the model...")

            model = self.train_model(x_train, y_train)

            # get the model predictions
            yhat_train = model.predict(x_train)
            yhat_test = model.predict(x_test)

            # calculate the losses
            f1_score_train = f1_score(y_true=y_train, y_pred=yhat_train)
            f1_score_test = f1_score(y_true=y_test, y_pred=yhat_test)
            
            logging.info(f"Model scores : f1_score for training:{f1_score_train} \
                         | f1_score_test : {f1_score_test}")

            # check for underfitting 
            if f1_score_test < self.model_training_config.expected_accuracy:
                raise Exception(f"Low model accuracy. Expected accuracy:{self.model_training_config.expected_accuracy} \
                                Current accuracy: {f1_score_test}")
            
            # check for overfitting
            diff = abs(f1_score_test-f1_score_train)
            if diff>self.model_training_config.overfitting_threshold:
                raise Exception(f"Train and test accuracies found greater than the expected threshold. |\
                                Expected overfitting threshold : {self.model_training_config.overfitting_threshold} | \
                                Current difference:{diff}")
            

            # save the model
            utils.save_object(file_path=self.model_training_config.model_path,
                              obj=model)
            
            logging.info(f"Model saved successfully.")
            
            # prepare the artifact
            model_training_artifact = ModelTrainingArtifact(
                model_path=self.model_training_config.model_path,
                f1_train_score=f1_score_train,
                f1_test_score=f1_score_test
            )

            logging.info(f"{'>>'*10}Model training complete.")

            return model_training_artifact  




        except Exception as e:
            raise SensorException(e, sys)

    










