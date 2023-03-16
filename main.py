from sensor import logger
from sensor.exception import SensorException
import sys


if __name__ == '__main__':
    try :
        result = 2/0

    except Exception as e:
        print(SensorException(e, sys))
