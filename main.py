from sensor import logger
from sensor.exception import SensorException
import sys
from sensor.utils import get_dataframe_from_collection
from sensor.entity import config_entity, artifact_entity
from sensor.components import data_ingestion, data_validation

if __name__ == '__main__':
    db_name = "APS"
    collection_name = "SENSOR_DATA"
    try :
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)
        
        data_ingestion_phase = data_ingestion.data_ingestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion_phase.initiate_data_ingestion()

        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config)
        data_validation_phase = data_validation.data_validation(data_validation_config=data_validation_config,
                                                                data_ingestion_artifact=data_ingestion_artifact)

        data_validation_artifact = data_validation_phase.initiate_data_validation()

    except Exception as e:
        print(SensorException(e, sys))
