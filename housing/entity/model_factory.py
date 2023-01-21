import os
import sys

from housing.exception import HousingException
from housing.util.util import load_object
import numpy as np

# from housing.component.model_trainer import preprocess
from housing.component.model_trainer import ModelTrainer

import pandas as pd


class HousingData:

    def __init__(self,
                 transaction_date:float,
                 house_age:float,
                 distance_MRT_station:float,
                 convenience_stores:float,
                 latitude:float,
                 longitude:float,
           
                 #target feature----------
                #  housepriceofunit_area : float = None
                 ):
         
        try:
            self.transaction_date =transaction_date,
            self.house_age =house_age,
            self.distance_MRT_station = distance_MRT_station,
            self.convenience_stores =convenience_stores,
            self.latitude =latitude,
            self.longitude = longitude,
          
            # output feature--------
            # self.housepriceofunit_area = housepriceofunit_area
                                   
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_housing_input_data_frame(self):

        try:
            housing_input_dict = self.get_housing_data_as_dict()
            data=pd.DataFrame(data=housing_input_dict)
            print('data')
            print(data)
            return data
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_housing_data_as_dict(self):
        try:
            input_data = {

                # "transaction_date":[self.transaction_date],
                #  "house_age":[self.house_age],
                #  "distance_MRT_station":[self.distance_MRT_station],
                #  "convenience_stores":[self.convenience_stores],
                #  "latitude":[self.latitude],
                #  "longitude":[self.longitude]

                 "X1 transaction date":[2012.917],
                 "X2 house age":[32.0],
                 "X3 distance to the nearest MRT station":[84.87882],
                 "X4 number of convenience stores":[10],
                 "X5 latitude":[24.98298],
                 "X6 longitude":[121.54024]
           
                
     
                 # output feature--------
                #  "housepriceofunit_area":[self.housepriceofunit_area]
                }
            return input_data
        except Exception as e:
            raise HousingException(e, sys)


class HousingPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_latest_model_path(self):
        try:
            # folder_name = list(map(int, os.listdir(self.model_dir)))
            # latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(self.model_dir)[0]
            latest_model_path = os.path.join(self.model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise HousingException(e, sys) from e

    def predict(self, X):
        try:
            # models=ModelTrainer()
            # models.preprocess(X)
            model_path = self.get_latest_model_path()
            # model_path=self.model_dir
            model = load_object(file_path=model_path)
            # print(model.preprocessing_object)

            # transformed_feature = model.preprocessing_object.transform(X)

            # return model.trained_model_object.predict(transformed_feature)
            print(X)
            # [[2012.917,32.0,84.87882,10,24.98298,121.54024]]
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise HousingException(e, sys) from e