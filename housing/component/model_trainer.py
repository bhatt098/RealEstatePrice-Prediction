# import shutil
import shutil
from housing.exception import HousingException
import sys
# from housing.logger import logging
from typing import List
from housing.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact,DataIngestionArtifact
from housing.entity.config_entity import ModelTrainerConfig
from housing.util.util import load_numpy_array_data,save_object,load_object
from housing.entity.model_factory import MetricInfoArtifact, ModelFactory,GridSearchedBestModel
from housing.entity.model_factory import evaluate_regression_model

# from housing.component.data_transformation import target_feature_train_df,target_feature_test_df
import numpy as np
import pandas as pd
import os

SAVED_MODELS_DIR_NAME = "saved_models"
SAVED_MODELS_NAME = "saved"

ROOT_DIR = os.getcwd()


class HousingEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
      
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"




class ModelTrainer:

    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact,data_ignestion_artifact=DataIngestionArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            self.data_ingnestion_artifact=data_ignestion_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            # train_file_path = self.data_ingnestion_artifact.train_file_path
            # test_file_path=self.data_ingnestion_artifact.test_file_path

            # train_data=pd.read_csv(train_file_path)
            # target_feature_train_df=train_data['Y house price of unit area']

            # test_data=pd.read_csv(test_file_path)
            # target_feature_test_df=test_data['Y house price of unit area']

            # transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            # train_array = load_numpy_array_data(file_path=transformed_train_file_path)

            # transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            # test_array = load_numpy_array_data(file_path=transformed_test_file_path)

            
            # print(target_feature_train_df)
            # x_train=train_array
            # y_train=np.array(target_feature_train_df)
            # x_test=test_array
            # y_test=np.array(target_feature_test_df)

            # print(type(y_train))
            # print(type(y_test))



            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array_data(file_path=transformed_train_file_path)

            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)

            x_train,y_train,x_test,y_test = train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]

            model_config_file_path = self.model_trainer_config.model_config_file_path

            model_factory = ModelFactory(model_config_path=model_config_file_path)
            
            
            base_accuracy = self.model_trainer_config.base_accuracy

            best_model = model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=base_accuracy)
            
            
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list
            
            model_list = [model.best_model for model in grid_searched_best_model_list ]
            metric_info:MetricInfoArtifact = evaluate_regression_model(model_list=model_list,X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,base_accuracy=base_accuracy)

            
            preprocessing_obj=  load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
            model_object = metric_info.model_object


            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            housing_model = HousingEstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            save_object(file_path=trained_model_file_path,obj=housing_model)

            # copying model from one location to another location----------------
            MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
            basename = os.path.basename(trained_model_file_path)
            files=os.path.join(MODEL_DIR,basename)
            os.makedirs(os.path.dirname(files), exist_ok=True)
            shutil.copy(trained_model_file_path, files)
            #-------------------------------------------------------

            model_trainer_artifact=  ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            train_rmse=metric_info.train_rmse,
            test_rmse=metric_info.test_rmse,
            train_accuracy=metric_info.train_accuracy,
            test_accuracy=metric_info.test_accuracy,
            model_accuracy=metric_info.model_accuracy
            
            )

            return model_trainer_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def preprocess(self,X):
        preprocessing_obj=  load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
        transformed_feature = preprocessing_obj.transform(X)



    


#loading transformed training and testing datset
#reading model config file 
#getting best model on training datset
#evaludation models on both training & testing datset -->model object
#loading preprocessing pbject
#custom model object by combining both preprocessing obj and model obj
#saving custom model object
#return model_trainer_artifact
