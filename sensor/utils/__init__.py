
import os, sys
import yaml
import dill
import pandas as pd
import numpy as np
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client


# extract data from database and return a dataframe
def get_dataframe_from_collection(db_name : str, collection_name : str) -> pd.DataFrame :
    """
    Description : 
    Retrieves data stored in mongodb and converts to a pandas dataframe

    Params : 
    db_name : database name
    collection_name : collection name
    ========================================

    returns : pandas.DataFrame 
    """
    
    try :
        logging.info(f"Reading data from database {db_name} and collection {collection_name}")
        df = pd.DataFrame(list(mongo_client[db_name][collection_name].find()))
        logging.info(f"Found columns : {df.columns}")
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])
            logging.info("_id column dropped.")
        return df
    except Exception as e:
        raise SensorException(e, sys)



def write_yaml_file(file_path:str, data:dict) ->  None:
    """Write the data to a yaml file.

    Args:
        file_path (str): file path
        data (dict) : Data to be written

    Returns :
        None.


    """
    try:
        f_path = os.path.dirname(file_path)
        os.makedirs(f_path, exist_ok=True)

        with open(file_path, "w") as f:
            yaml.dump(data, f)


    except Exception as e:
        raise SensorException(e, sys)


def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info(f"Saving object to path : {file_path}...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"Object saved successfully.")
    except Exception as e:
        raise SensorException(e, sys)
    

def load_object(file_path:str) -> object:
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys)
    

def save_numpy_array(file_path:str, array):
    try:
        logging.info(f"Saving the array to {file_path}...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as obj:
            np.save(obj, array)
        logging.info("Saved successfully.")
    except Exception as e:
        raise SensorException(e, sys)


def load_numpy_array(file_path:str):
    try:
        with open(file_path, "rb") as obj:
            return np.load(obj)
    except Exception as e:
        raise SensorException(e, sys)