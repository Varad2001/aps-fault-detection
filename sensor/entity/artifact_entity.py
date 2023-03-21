

class DataIngestionArtifact :
    
    def __init__(self, feature_store_file_path, train_path, test_path) :
        feature_store_file_path : str = feature_store_file_path
        train_file_path : str = train_path
        test_file_path : str = test_path

class DataValidationArtifact :
    pass

class DataTransformationArtifact :
    pass

class ModelTrainingArtifact :
    pass

class ModelEvaluationArtifact :
    pass

class ModelPusherArtifact :
    pass
