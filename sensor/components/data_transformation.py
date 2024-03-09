import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact
from sensor.logger import logging
from sensor.config import TARGET_COLUMN
from sensor import utils
from sensor.exception import SensorException



class DataTransformation():
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)
        

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        """Get the sklearn.pipeline.Pipeline object to perform data transformation
           on the data for training. Performs 2 steps: SimpleImputer and RobustScaler.

        Returns:
            Pipeline: sklearn.pipeline.Pipeline object.
        """
        try:
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            robust_scaler = RobustScaler()

            pipeline = Pipeline(
                steps=[
                    ("Imputer", simple_imputer),
                    ("RobustScaler", robust_scaler)
                ]
            )

            return pipeline
        except Exception as e:
            raise SensorException(e, sys)
        

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:

            logging.info(f"{'>>'*10}Initiating data transformation phase...")

            # read the train and test file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            train_df.replace({"na":np.nan}, inplace=True)
            test_df.replace({"na":np.nan}, inplace=True)

            # now separate the data into input features and target features
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            # create a label encoder to encode the target feature
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            # transform the target features
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)


            logging.info(f"Imputing missing data and removing outliers...")

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            # transform the input features
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            # the target column is highly imbalanced; hence we will populate it with minority value
            
            logging.info(f"Performing resampling...")
            
            smt = SMOTETomek(sampling_strategy="minority")

            logging.info(f"Before resampling in training data:\
                         Input features:{input_feature_train_arr.shape},Target feature:{target_feature_train_arr.shape}")
            
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            
            logging.info(f"After resampling in training data:\
                         Input features:{input_feature_train_arr.shape},Target feature:{target_feature_train_arr.shape}")
            
            logging.info(f"Before resampling in test data:\
                         Input features:{input_feature_test_arr.shape},Target feature:{target_feature_test_arr.shape}")
            
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            
            logging.info(f"Before resampling in test data:\
                         Input features:{input_feature_test_arr.shape},Target feature:{target_feature_test_arr.shape}")
            

            logging.info(f"Data transformation complete. Saving necessary files...")

            # prepare the train and test array 
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            # save the arrays
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_train_path,
                                   array=train_arr)
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_test_path,
                                   array=test_arr)
            
            # save the transformation objects
            utils.save_object(file_path=self.data_transformation_config.transformer_object_path,
                              obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
                              obj=label_encoder)
            

            # now prepare the data transformation artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformer_object_path=self.data_transformation_config.transformer_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                target_encoder_path=self.data_transformation_config.target_encoder_path
            )

            logging.info(f"{'>>'*10}Data Transformation complete.")

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)


