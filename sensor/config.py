import pymongo
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class EnvironmentVariables : 
    mongodb_url : str = os.getenv("MONGODB_URL")

env_var = EnvironmentVariables()

mongo_client = pymongo.MongoClient(env_var.mongodb_url)

TARGET_COLUMN = "class"

