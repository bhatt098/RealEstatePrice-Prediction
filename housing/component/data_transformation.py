# from cgi import test
from sklearn import preprocessing
from housing.exception import HousingException
# from housing.logger import logging
from housing.entity.config_entity import DataTransformationConfig 
from housing.entity.artifact_entity import*
import sys,os
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from housing.constant import *
from housing.util.util import read_yaml_file,save_object,save_numpy_array_data,load_data
import dill
# target_feature_train_df=target_feature_test_df
# target_feature_test_df=





class DataTransformation:
    
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact
                 ):
        try:
            # logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    

    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            # schema_file_path = self.data_validation_artifact.schema_file_path

            # dataset_schema = read_yaml_file(file_path=schema_file_path)

            train_file_path = self.data_ingestion_artifact.train_file_path
            # test_file_path = self.data_ingestion_artifact.test_file_path
            df=pd.read_csv(train_file_path)
            numerical_columns = [feature for feature in df.columns if df[feature].dtypes!='O' and feature!='Y house price of unit area']
            # categorical_columns = [feature for feature in df.columns if df[feature].dtypes=='O']
            print(numerical_columns)


            num_pipeline = Pipeline(steps=[
                # ('imputer', SimpleImputer(strategy="median")),
                ('scaler', StandardScaler())
            ]
            )

            # cat_pipeline = Pipeline(steps=[
            #      ('impute', SimpleImputer(strategy="most_frequent")),
            #      ('one_hot_encoder', OneHotEncoder(handle_unknown="ignore")),
            #      ('scaler', StandardScaler(with_mean=False))
            # ]
            # )

            # logging.info(f"Categorical columns: {categorical_columns}")
            # logging.info(f"Numerical columns: {numerical_columns}")


            preprocessing = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                # ('cat_pipeline', cat_pipeline, categorical_columns),
            ])
            return preprocessing

        except Exception as e:
            raise HousingException(e,sys) from e   


    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            preprocessing_obj = self.get_data_transformer_object()


            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            

            schema_file_path = self.data_validation_artifact.schema_file_path
            
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            

           
            input_feature_train_df = train_df.drop(columns=['Y house price of unit area'],axis=1)
            target_feature_train_df = train_df['Y house price of unit area']

            input_feature_test_df = test_df.drop(columns=['Y house price of unit area'],axis=1)
            target_feature_test_df = test_df['Y house price of unit area']
            
            # print(input_feature_train_df.columns)

            print(input_feature_test_df)
           

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            # dataTrs=[[2012.917,32.0,84.87882,10,24.98298,121.54024]]
            # input_feature = preprocessing_obj.transform(dataTrs)

            train_arr=np.array(target_feature_train_df)

            test_arr=np.array(target_feature_test_df)

            # print(type(input_feature_train_arr))


            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            # Here saving individual tranformed train and test files
            self.save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            self.save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            # saving preprocessed object 
            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
            self.save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path=transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            preprocessed_object_file_path=preprocessing_obj_file_path

            )
            return data_transformation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e


    def save_object(self,file_path:str,obj):
     """
     file_path: str
     obj: Any sort of object
     """
     try:
         dir_path = os.path.dirname(file_path)
         os.makedirs(dir_path, exist_ok=True)
         with open(file_path, "wb") as file_obj:
             dill.dump(obj, file_obj)
     except Exception as e:
         raise HousingException(e,sys) from e

    def save_numpy_array_data(self,file_path: str, array: np.array):
     """
     Save numpy array data to file
     file_path: str location of file to save
     array: np.array data to save
     """
     try:
         dir_path = os.path.dirname(file_path)
         os.makedirs(dir_path, exist_ok=True)
         with open(file_path, 'wb') as file_obj:
             np.save(file_obj, array)
     except Exception as e:
         raise HousingException(e, sys) from e

   