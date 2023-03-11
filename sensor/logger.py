import os
import logging
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%d/%m/%Y__%H%M%S')}.log"

LOG_FILE_DIR = os.path.join(os.getcwd(), "logs")

# create folder if not available
os.makedirs(LOG_FILE_DIR, exist_ok = True)

# file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s %(message)s",
    level = logging.INFO
)
