

class DataIngestionArtifact :
    
    def __init__(self, feature_store_file_path, train_path, test_path) :
        self.train_file_path : str = train_path
        self.test_file_path : str = test_path
        self.feature_store_file_path : str = feature_store_file_path
        


class DataValidationArtifact :

    def __init__(self, report_file_path) :
       self.report_file_path : str = report_file_path


class DataTransformationArtifact :
    def __init__(self,transformer_object_path, transformed_train_path, 
                 transformed_test_path, target_encoder_path) :
        self.transformer_object_path = transformer_object_path
        self.transformed_train_path = transformed_train_path
        self.transformed_test_path = transformed_test_path
        self.target_encoder_path = target_encoder_path


class ModelTrainingArtifact :
    def __init__(self, model_path, f1_train_score, f1_test_score):
        self.model_path = model_path
        self.f1_train_score = f1_train_score
        self.f1_test_score = f1_test_score



class ModelEvaluationArtifact :
    pass

class ModelPusherArtifact :
    pass
