# data ingestion steps : 
# collect the data from mongodb database
# drop the nan values 
# store the dataframe as csv file 
# split the data into train and test files 
# save the files to relevant locations

import numpy as np
import pandas as pd
import os, sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.entity.config_entity import DataIngestionConfig
from sensor.utils import get_dataframe_from_collection
from sklearn.model_selection import train_test_split

class data_ingestion() :

    def __init__(self, data_ingestion_config : DataIngestionConfig):

        self.data_ingestion_config = data_ingestion_config

    def initiate_data_ingestion(self) -> DataIngestionArtifact :
        
        try :
            # get the data as a dataframe
            df : pd.DataFrame = get_dataframe_from_collection(
                self.data_ingestion_config.database_name,
                self.data_ingestion_config.collection_name)
            
            # replace the "na" values by np.nan
            df.replace(to_replace="nan", value=np.nan, inplace=True)

            # store the dataframe to 'feature_store_file_path' folder
            path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(path, exist_ok=True)
            path = os.path.join(path, "sensor.csv")
            df.to_csv(path_or_buf=path, header=True, index=False)

            # split the data to train and test
            train_df, test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size)

            # save the files
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir)
            train_df.to_csv(self.data_ingestion_config.train_file_path)
            test_df.to_csv(self.data_ingestion_config.test_file_path)

            # prepare the output : dataIngestionArtifact
            data_ingestion_artifact = DataIngestionArtifact(
                self.data_ingestion_config.feature_store_file_path,
                self.data_ingestion_config.train_file_path,
                self.data_ingestion_config.test_file_path)
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise SensorException(e, sys)

        




