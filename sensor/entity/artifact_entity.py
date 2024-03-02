

class DataIngestionArtifact :
    
    def __init__(self, feature_store_file_path, train_path, test_path) :
        self.train_file_path : str = train_path
        self.test_file_path : str = test_path
        self.feature_store_file_path : str = feature_store_file_path
        


class DataValidationArtifact :

    def __init__(self, report_file_path) :
       self.report_file_path : str = report_file_path

class DataTransformationArtifact :
    pass

class ModelTrainingArtifact :
    pass

class ModelEvaluationArtifact :
    pass

class ModelPusherArtifact :
    pass
