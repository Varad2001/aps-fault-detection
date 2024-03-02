import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from sensor.logger import logging
from sensor import utils
from sensor.exception import SensorException



class data_validation :

    def __init__(self, data_validation_config:DataValidationConfig, 
                 data_ingestion_artifact:DataIngestionArtifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.validation_error = dict()


    def drop_missing_values_columns(self, df:pd.DataFrame, report_key_name) -> pd.DataFrame | None:
        """
        Drops the columns with the null values greater than the threshold. Returns a pandas.DataFrame object or None if
        all the columns are dropped.

        df : input dataframe
        report_key_name : key for the dict report to be formed; e.g. missing_values_in_test_data
        returns : pd.DataFrame or None
        """
        try:
            threshold = self.data_validation_config.missing_threshold

            logging.info(f"Checking {report_key_name} greater than {threshold}...")

            
            null_percent = df.isnull().sum() / df.shape[0]
            drop_columns = null_percent[null_percent>threshold]
            drop_column_names = list(drop_columns.index)
            self.validation_error[report_key_name] = drop_column_names
            df.drop(drop_column_names, axis=1, inplace=True)

            logging.info(f"Following columns dropped : {drop_column_names}")

            
            return df

        except Exception as e:
            raise SensorException(e, sys)


    def is_required_columns_exist(self, base_df:pd.DataFrame, current_df:pd.DataFrame,report_key_name) -> bool:
        """Checks if there is any missing column in the 'current_df' compared to 'base_df'.

        Args:
            base_df (pd.DataFrame): Original dataframe
            current_df (pd.DataFrame): Current df to be compared
            report_key_name : key for the dict report to be formed; e.g. missing_values_in_test_data
        

        Returns:
            bool: True if all the columns are present else False
        """
        try:

            logging.info(f"Checking if there's any missing column for : {report_key_name}")

            base_columns = base_df.columns
            current_columns = current_df.columns
            missing_columns = []

            for base_col in base_columns:
                if base_col not in current_columns:
                    missing_columns.append(base_col)

            # if some columns are missing 
            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = missing_columns
                logging.info(f"Following columns were found missing : {missing_columns}")
                return False
            else:
                logging.info(f"No column was found missing.")
                return True
        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame,report_key_name) -> dict :
        """Checks the data drift for each column data.

        Args:
            base_df (pd.DataFrame): Original Dataframe
            current_df (pd.DataFrame): Current dataframe
            report_key_name : key for the dict report to be formed; e.g. missing_values_in_test_data
        

        Returns:
            dict: Returns a dict containing reports for each column
        """

        try:

            logging.info(f"Checking data drift for : {report_key_name}...")

            # np.Nan values are causing some unexpected behavior in ks2_samp
            # hence change the np.Nan to "na"
            base_df.replace({np.nan: "na"}, inplace=True)
            current_df.replace({np.nan: "na"}, inplace=True)


            drift_report = dict()
            base_columns = base_df.columns

            for base_col in base_columns:
                base_data , current_data = base_df[base_col], current_df[base_col]

                # null hypothesis : both data samples are having the same distribution
                same_distribution = ks_2samp(base_data, current_data)


                # if the pvalue is > 0.05, --> accept the null hypothesis
                if same_distribution.pvalue > 0.05:
                    drift_report[base_col] = {
                        "pvalues" : float(same_distribution.pvalue),
                        "same_distribution" : True
                    }
                else:
                    drift_report[base_col] = {
                        "pvalues" : float(same_distribution.pvalue),
                        "same_distribution" : False
                    }
            
            self.validation_error[report_key_name] = drift_report

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:

            logging.info(f"{'>>'*10}Initiating data validation phase...")

            # get the required dataframes
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # dataframes contain null values as "na", --> convert them to np.nan
            base_df.replace("na", np.nan, inplace=True)
            train_df.replace("na", np.nan, inplace=True)
            test_df.replace("na", np.nan, inplace=True)

            # drop the missing values columns 
            base_df = self.drop_missing_values_columns(base_df, report_key_name="missing_values_in_base_data")
            train_df = self.drop_missing_values_columns(train_df, report_key_name="missing_values_in_train_data")
            test_df = self.drop_missing_values_columns(test_df, report_key_name="missing_values_in_test_data")

            # check if the required columns are there; if yes, proceed to check data drift
            if self.is_required_columns_exist(base_df, train_df, report_key_name="missing_columns_in_train_data"):
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name="data_drift_in_train_data")
            if self.is_required_columns_exist(base_df, test_df, report_key_name="missing_columns_in_test_data"):
                self.data_drift(base_df=base_df, current_df=test_df, report_key_name="data_drift_in_test_data")

            # write the report to a yaml file
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
                                  data=self.validation_error)
            
            logging.info(f"Drift report file successfully saved to : {self.data_validation_config.report_file_path}")
            

            logging.info(f"{'>>'*10}Data Validation complete.")

            return DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)


        except Exception as e:
            raise SensorException(e, sys)


