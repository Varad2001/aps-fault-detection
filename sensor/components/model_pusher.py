import os
import sys
import pandas as pd
import numpy as np
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.logger import logging
from sensor import utils
from sensor.predictor import ModelResolver
from sensor.exception import SensorException



class ModelPusher:
    def __init__(self, 
                 model_pusher_config:config_entity.ModelPusherConfig,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact : artifact_entity.ModelTrainingArtifact,
                 model_eva_artifact : artifact_entity.ModelEvaluationArtifact) :
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_eva_artifact = model_eva_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.model_pusher_sync_dir)

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_model_pusher(self) -> artifact_entity.ModelPusherArtifact:
        try:

            logging.info(f"{'>>'*10}Initiating model pusher phase...")

            # first get the model details
            logging.info(f"Loading the model details...")

            model_transformer_path = self.data_transformation_artifact.transformer_object_path
            model_path = self.model_trainer_artifact.model_path
            target_encoder_path = self.data_transformation_artifact.target_encoder_path

            # load the objects
            model_transformer = utils.load_object(file_path=model_transformer_path)
            model = utils.load_object(file_path=model_path)
            target_encoder = utils.load_object(file_path=target_encoder_path)

            
            # save the model details to the model pusher artifacts dir
            logging.info(f"Saving the model details to model pusher artifacts dir...")

            utils.save_object(file_path=self.model_pusher_config.pusher_transformer_path,
                              obj=model_transformer)
            utils.save_object(file_path=self.model_pusher_config.pusher_model_path,
                              obj=model)
            utils.save_object(file_path=self.model_pusher_config.pusher_target_encoder_path,
                              obj=target_encoder)
            
            # save the details to models to be synced dir
            logging.info(f"Saving the model details to dir to be synced outside...")

            trans_path_sync = self.model_resolver.get_latest_save_transformer_path()
            model_path_sync = self.model_resolver.get_latest_save_model_path()
            target_encoder_path_sync = self.model_resolver.get_latest_save_target_encoder_path()


            utils.save_object(file_path=trans_path_sync,
                              obj=model_transformer)
            utils.save_object(file_path=model_path_sync,
                              obj=model)
            utils.save_object(file_path=target_encoder_path_sync,
                              obj=target_encoder)
            

            model_pusher_artifact = artifact_entity.ModelPusherArtifact(
                model_pusher_saved_models_dir=self.model_pusher_config.model_pusher_saved_models_dir,
                model_pusher_sync_dir=self.model_pusher_config.model_pusher_sync_dir
            )

            logging.info(f"{'>>'*10}Model pusher phase complete.")

            return model_pusher_artifact






        except Exception as e:
            raise SensorException(e, sys)
