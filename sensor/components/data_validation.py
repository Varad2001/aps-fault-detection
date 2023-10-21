import os
import pandas as pd
from scipy.stats import ks_2samp
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataValidationArtifact
from sensor.logger import logging
from sensor.exception import SensorException


class data_validation :

    def __init__(self, data_validation_config:DataValidationConfig):
        self.data_validation_config = data_validation_config

    def is_required_columns_exist(self) -> bool:
        pass

    def drop_missing_values_columns(self, df:pd.DataFrame, threshold:float=0.3) -> pd.DataFrame:
        """
        Drops the columns with the null values greater than the threshold. Returns a pandas.DataFrame object.

        df : input dataframe
        threshold : percentage of threshold
        returns : pd.DataFrame
        """
        pass

    def initiate_data_validation(self) -> DataValidationArtifact:
        pass


