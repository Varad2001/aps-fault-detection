import sys
from sensor import logger
from sensor.exception import SensorException
from sensor.pipeline import training_pipeline
from sensor.pipeline import batch_prediction



file_path = "/home/varad/Work/aps-fault-detection/artifacts/16032024_182657/data_ingestion/dataset/test.csv"

if __name__ == '__main__':
    
    try :
        #training_pipeline.start_training_pipeline()
        output = batch_prediction.start_batch_prediction(file_path)
        print(output)
        
    except Exception as e:
        print(SensorException(e, sys))
