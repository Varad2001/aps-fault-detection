import pymongo
import os
from dataclasses import dataclass

@dataclass
class EnvironmentVariables : 
    mongodb_url : str = "mongodb+srv://varadkhonde:yadneshkhonde@cluster0.zeesz.mongodb.net/?retryWrites=true&w=majority"


env_var = EnvironmentVariables()

mongo_client = pymongo.MongoClient(env_var.mongodb_url)


