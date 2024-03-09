import sys, os
from datetime import datetime
from sensor.exception import SensorException


TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"


class TrainingPipelineConfig():

    def __init__(self) :
        try :
            self.artifact_dir = os.path.join(os.getcwd(), "artifacts", f"{datetime.now().strftime('%d%m%Y_%H%M%S')}")

        except Exception as e:
            raise SensorException(e, sys)


class DataIngestionConfig :

    def __init__(self, training_pipeline_config : TrainingPipelineConfig) :
        self.database_name = "APS"
        self.collection_name = "SENSOR_DATA"
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir, "feature_store")
        self.train_file_path = os.path.join(self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir, "dataset", TEST_FILE_NAME)
        self.test_size = 0.2

    def to_dict(self) -> dict :
        try :
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)



class DataValidationConfig :
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_threshold = 0.7
        self.base_file_path = os.path.join(os.getcwd(), "aps_failure_training_set1.csv")


class DataTransformationConfig :
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) :
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
        self.transformer_object_path = os.path.join(self.data_transformation_dir, "transformer", TRANSFORMER_OBJECT_FILE_NAME)
        self.transformed_train_path = os.path.join(self.data_transformation_dir, "transformed", TRAIN_FILE_NAME)
        self.transformed_test_path = os.path.join(self.data_transformation_dir, "transformed", TEST_FILE_NAME)
        self.target_encoder_path = os.path.join(self.data_transformation_dir, "target_encoder", TARGET_ENCODER_FILE_NAME)

class ModelTrainingConfig :
    pass

class ModelEvaluationConfig :
    pass

class ModelPusherConfig :
    pass

