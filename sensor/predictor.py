import os
import sys
from sensor.entity.config_entity import MODEL_FILE_NAME, TARGET_ENCODER_FILE_NAME, TRANSFORMER_OBJECT_FILE_NAME
from sensor.exception import SensorException



class ModelResolver:

    def __init__(self, model_registry:str = "saved_models",
                 model_dir= "model",
                 transformer_dir = "transformer",
                 target_endoder_dir = "target_encoder") -> None:
        self.model_registry = model_registry
        os.makedirs(self.model_registry, exist_ok=True)
        self.model_dir = model_dir
        self.transformer_dir = transformer_dir
        self.target_endoder_dir = target_endoder_dir


    def get_latest_dir(self):
        try:
            dirs = os.listdir(self.model_registry)
            dirs = list(map(int, dirs))
            if len(dirs) == 0:
                return None
            latest_dir = max(dirs)
            return os.path.join(self.model_registry, f"{latest_dir}")
        except Exception as e:
            raise SensorException(e, sys)
        

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir()
            if not latest_dir:
                raise Exception(f"No model available.")
            return os.path.join(latest_dir, self.model_dir, MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir()
            if not latest_dir:
                raise Exception(f"No transformer available.")
            return os.path.join(latest_dir, self.transformer_dir, TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)
        

    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir()
            if not latest_dir:
                raise Exception(f"No target encoder available.")
            return os.path.join(latest_dir, self.target_endoder_dir, TARGET_ENCODER_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_save_dir(self):
        try:
            latest_dir = self.get_latest_dir()
            if not latest_dir:
                return os.path.join(self.model_registry, f"{0}")
            new_dir = os.path.join(self.model_registry, f"{int(os.path.basename(latest_dir))+1}")
            return new_dir
        except Exception as e:
            raise SensorException(e, sys)
        

    def get_latest_save_model_path(self):
        try:
            save_model_dir = self.get_latest_save_dir()
            return os.path.join(save_model_dir, self.model_dir, MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_save_transformer_path(self):
        try:
            save_model_dir = self.get_latest_save_dir()
            return os.path.join(save_model_dir, self.transformer_dir, TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_save_target_encoder_path(self):
        try:
            save_model_dir = self.get_latest_save_dir()
            return os.path.join(save_model_dir, self.target_endoder_dir, TARGET_ENCODER_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)
        


class Predictor:
    pass


