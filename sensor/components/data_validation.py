import os
import sys
import pandas as pd
from scipy.stats import ks_2samp
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from sensor.logger import logging
from sensor.exception import SensorException


class data_validation :

    def __init__(self, data_validation_config:DataValidationConfig, 
                 data_ingestion_artifact:DataIngestionArtifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.validation_error = dict()


    def drop_missing_values_columns(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Drops the columns with the null values greater than the threshold. Returns a pandas.DataFrame object.

        df : input dataframe
        threshold : percentage of threshold
        returns : pd.DataFrame
        """
        try:
            threshold = self.data_validation_config.missing_threshold
            null_percent = df.isnull().sum() / df.shape[0]
            drop_columns = null_percent[null_percent>threshold]
            drop_column_names = drop_columns.index
            self.validation_error['dropped_columns'] = drop_column_names
            df.drop(list(drop_column_names), axis=1, inplace=True)

            if len(df.columns) == 0:
                return None
            else:
                return df

        except Exception as e:
            raise SensorException(e, sys)


    def is_required_columns_exist(self, base_df:pd.DataFrame, current_df:pd.DataFrame) -> bool:
        """Checks if there is any missing column before proceeding to the training phase.

        Args:
            base_df (pd.DataFrame): Original dataframe
            current_df (pd.DataFrame): Current df to be compared

        Returns:
            bool: True if all the columns are present else False
        """
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns
            missing_columns = []

            for base_col in base_columns:
                if base_col not in current_columns:
                    missing_columns.append(base_col)

            # if some columns are missing 
            if len(missing_columns) > 0:
                self.validation_error['missing_columns'] = missing_columns
                return False
            else:
                return True
        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame) -> dict :
        """Checks the data drift for each column data.

        Args:
            base_df (pd.DataFrame): Original Dataframe
            current_df (pd.DataFrame): Current dataframe

        Returns:
            dict: Returns a dict containing reports for each column
        """

        try:
            drift_report = dict()
            base_columns = base_df.columns

            for base_col in base_columns:
                base_data , current_data = base_df[base_col], current_df[base_col]

                # null hypothesis : both data samples are having the same distribution
                same_distribution = ks_2samp(base_data, current_data)

                # if the pvalue is > 0.05, --> accept the null hypothesis
                if same_distribution.pvalue > 0.05:
                    drift_report[base_col] = {
                        "pvalues" : same_distribution.pvalue,
                        "same_distribution" : True
                    }
                else:
                    drift_report[base_col] = {
                        "pvalues" : same_distribution.pvalue,
                        "same_distribution" : False
                    }
            
            self.validation_error["data_drift"] = drift_report

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:
        pass


