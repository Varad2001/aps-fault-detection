# APS FAULT DETECTION

The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down.  This project tries to predict this using binary classification algorithms on the data collected by various sensors.

The project aims to build a complete end-to-end machine learning pipeline to perform the steps mentioned below.

## Architecture :
1. Data Ingestion : Collect data from the database.
2. Data validation : Validate the data. Check null values, data drift, etc.
3. Data Transformation : Impute null values, remove outliers, perform upsampling techniques if necessary.
4. Model Training : Traning a classification model.
5. Model Evaluation : Evaluation of the trained model.
6. Model Pusher : Deploy the model. 


## Key points:
- Follows OOPs model.
- Mainly contains 6 steps mentioned above. 
    - config entity : input to each stage
    - artifact entity : output of a stage
- Tech stack :
    - Scikit-learn, Numpy, Pandas, MongoDB, Airflow, etc.
