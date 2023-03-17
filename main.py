from sensor import logger
from sensor.exception import SensorException
import sys
from sensor.utils import get_dataframe_from_collection

if __name__ == '__main__':
    db_name = "APS"
    collection_name = "SENSOR_DATA"
    try :
        df = get_dataframe_from_collection(db_name, collection_name)
        print(df.shape)

    except Exception as e:
        print(SensorException(e, sys))
