import sys
from sensor import logger
from sensor.exception import SensorException
from sensor.entity import config_entity, artifact_entity
from sensor.components import data_ingestion, data_validation, data_transformation, model_trainer

if __name__ == '__main__':
    db_name = "APS"
    collection_name = "SENSOR_DATA"
    try :
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)
        
        data_ingestion_phase = data_ingestion.DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion_phase.initiate_data_ingestion()
        

        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config)
        data_validation_phase = data_validation.DataValidation(data_validation_config=data_validation_config,
                                                                data_ingestion_artifact=data_ingestion_artifact)

        data_validation_artifact = data_validation_phase.initiate_data_validation()

        data_transformation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_transformation_phase = data_transformation.DataTransformation(
            data_transformation_config=data_transformation_config,
            data_ingestion_artifact=data_ingestion_artifact
        )

        data_transformation_artifact = data_transformation_phase.initiate_data_transformation()

        model_training_config = config_entity.ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
        model_training_phase = model_trainer.ModelTrainer(
            model_training_config=model_training_config,
            data_transformation_artifact=data_transformation_artifact
        )

        model_training_artifact = model_training_phase.initiate_model_training()

        print(model_training_artifact.__dict__)

    except Exception as e:
        print(SensorException(e, sys))
