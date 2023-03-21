# Dump the aps_training data to mongodb

import pymongo
import pandas as pd
import json

DATA_FILE_PATH = "/home/varad/Work/Data_science/aps_fault_detection/aps_failure_training_set1.csv"
DB_NAME = "APS" 
CLUSTER_NAME = "SENSOR_DATA"


client = pymongo.MongoClient("mongodb+srv://varadkhonde:yadneshkhonde@cluster0.zeesz.mongodb.net/?retryWrites=true&w=majority")


if __name__ == "__main__":

    db = client[DB_NAME]
    table = db[CLUSTER_NAME]

    df = pd.read_csv(DATA_FILE_PATH)

    # step by step convert the dataframe to json format

    # drop the index of the dataframe
    df.reset_index(drop=True, inplace=True)

    json_records = df.T.to_json()         
    json_records = json.loads(json_records)
    json_records = list(json_records.values())

    table.insert_many(json_records)
    print("Inserted successfully.")




    






