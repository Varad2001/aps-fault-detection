import os
import sys
from datetime import datetime
import pandas as pd
import numpy as np
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.logger import logging
from sensor import utils
from sensor.predictor import ModelResolver
from sensor.exception import SensorException


PREDICTION_FILE_DIR = os.path.join(os.getcwd(), "prediction")


def start_batch_prediction(input_file_path:str):
    try:

        logging.info(f"{'>>'*10}Starting batch prediction for {input_file_path}...")
        
        os.makedirs(name=PREDICTION_FILE_DIR, exist_ok=True)

        model_resolver = ModelResolver(model_registry="saved_models")

        logging.info(f"Loading the model details...")

        # load the input file
        df = pd.read_csv(input_file_path)
        df.replace({"na":np.NAN}, inplace=True)

        # load the model details
        model_transformer_path = model_resolver.get_latest_transformer_path()
        model_path = model_resolver.get_latest_model_path()
        target_encoder_path = model_resolver.get_latest_target_encoder_path()

        transformer = utils.load_object(file_path=model_transformer_path)
        model = utils.load_object(file_path=model_path)
        target_encoder = utils.load_object(file_path=target_encoder_path)

        logging.info(f"Transforming the input data...")

        # get the column names to be used to predict output
        column_names = list(transformer.feature_names_in_)

        input_arr = df[column_names]
        input_arr = transformer.transform(input_arr)

        logging.info(f"Making predictions and getting their corresponding labels...")

        # predict
        predictions = model.predict(input_arr)

        # convert the predictions to categorical values
        predictions_labels = target_encoder.inverse_transform(predictions)

        logging.info(f"Preparing the resultant file and saving ...")

        # append the results 
        df["predictions"] = predictions
        df["predictions_labels"] = predictions_labels

        # save the file like: <input_file_name>_<timestamp>.csv
        input_file_name = os.path.basename(input_file_path).replace(".csv", "")
        prediction_file_name = f"{input_file_name}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv"

        prediction_file_path = os.path.join(PREDICTION_FILE_DIR, prediction_file_name)

        # save the file
        df.to_csv(path_or_buf=prediction_file_path,
                  index=False, header=True)
        
        logging.info(f"Predictions file saved successfully at:{prediction_file_path}")

        logging.info(f"Batch prediction complete.")

        return prediction_file_path
        

    except Exception as e:
        raise SensorException(e, sys)


