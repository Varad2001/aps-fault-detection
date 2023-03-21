from sensor import logger
from sensor.exception import SensorException
import sys
from sensor.utils import get_dataframe_from_collection
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.components.data_ingestion import data_ingestion

if __name__ == '__main__':
    db_name = "APS"
    collection_name = "SENSOR_DATA"
    try :
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion1 = data_ingestion(data_ingestion_config)
        data_ingestion1.initiate_data_ingestion()

    except Exception as e:
        print(SensorException(e, sys))
