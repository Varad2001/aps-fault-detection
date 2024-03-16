import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.logger import logging
from sensor import utils
from sensor.config import TARGET_COLUMN
from sensor.predictor import ModelResolver
from sensor.exception import SensorException



class ModelEvaluation:
    
    def __init__(self,
                 model_eval_config: config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_training_artifact:artifact_entity.ModelTrainingArtifact
                 ):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_training_artifact = model_training_artifact
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_model_evaluation(self):
        try:

            logging.info(f"{'>>'*10}Initiating model evaluation phase...")
            
            # first check if there are any available models 
            latest_dir = self.model_resolver.get_latest_dir()
            
            # if no model available, current model will be accepted
            if not latest_dir:
                logging.info(f"NO previous models were found. Returning the current model...")
                model_eva_artifact = artifact_entity.ModelEvaluationArtifact(
                    is_model_accepted=True,
                    improved_accuracy=None
                )
                return model_eva_artifact
            
            # if previous model is available, then compare the two models
            logging.info(f"Previous model is use. Comparing its accuracy with the current model..")
            
            # first, load the details of the previous model
            logging.info(f"Loading previous models details...")
            prev_transformer_path = self.model_resolver.get_latest_transformer_path()
            prev_model_path = self.model_resolver.get_latest_model_path()
            prev_target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            # load these objects
            prev_transformer = utils.load_object(file_path=prev_transformer_path)
            prev_model = utils.load_object(file_path=prev_model_path)
            prev_target_encoder = utils.load_object(file_path=prev_target_encoder_path)

            # load the test file
            logging.info(f"Loading the test file details...")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            test_df.replace({"na":np.nan}, inplace=True)
            
            target_column = test_df[TARGET_COLUMN]
            input_features = test_df.drop(TARGET_COLUMN, axis=1)

            logging.info(f"Calculating previous model's accuracy...")
            input_arr = prev_transformer.transform(input_features)
            y_pred = prev_model.predict(input_arr)
            y_true = prev_target_encoder.transform(target_column)

            # calculate the accuracy of the prev model
            prev_accuracy = f1_score(y_true=y_true, y_pred=y_pred)


            logging.info(f"Loading the current models details and calculating its accuracy...")
            # now load the current model details
            current_transformer_path = self.data_transformation_artifact.transformer_object_path
            current_model_path = self.model_training_artifact.model_path
            current_target_encoder_path = self.data_transformation_artifact.target_encoder_path

            current_transformer = utils.load_object(file_path=current_transformer_path)
            current_model = utils.load_object(file_path=current_model_path)
            current_target_encoder = utils.load_object(file_path=current_target_encoder_path)

            input_arr = current_transformer.transform(input_features)
            y_pred = current_model.predict(input_arr)
            y_true = current_target_encoder.transform(target_column)

            # calculate the accuracy of the current model
            current_accuracy = f1_score(y_true=y_true, y_pred=y_pred)

            logging.info(f"Previous model accuracy:{prev_accuracy} | \
                         Current model accuracy : {current_accuracy}")

            # if the current model has lower accuracy, stop the pipeline
            if current_accuracy < prev_accuracy:
                logging.info(f"Current model accuracy lower than the previous.Raising the exception...")
                raise Exception(f"Current model accuracy lower than the previous.")
            
            # if not, prepare the artifact
            model_eva_artifact = artifact_entity.ModelEvaluationArtifact(
                is_model_accepted=True,
                improved_accuracy=current_accuracy-prev_accuracy
            )

            logging.info(f"Current model accuracy is higher than the previous. Accepting the current model..")

            logging.info(f"{'>>'*10}Model evaluation complete.")

            return model_eva_artifact



            
            

        except Exception as e:
            raise SensorException(e, sys)



