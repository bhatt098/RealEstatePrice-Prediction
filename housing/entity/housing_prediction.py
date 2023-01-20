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
                 MSSubClass:float ,
                 LotFrontage:float,
                 LotArea:float,
                 OverallQual :float,
                 OverallCond :float,
                 YearBuilt :int,
                 YearRemodAdd:int,
                 MasVnrArea :float,
                 BsmtFinSF1 :float,
                 BsmtFinSF2 :float,
                 BsmtUnfSF :float,
                 TotalBsmtSF :float,
                #  H1stFlrSF :float,
                #  H2ndFlrSF : float,
                 LowQualFinSF:float,
                 GrLivArea : float,
                 BsmtFullBath:float,
                 FullBath : float,
                 HalfBath : float,
                 BedroomAbvGr:float,
                 KitchenAbvGr:float,
                 TotRmsAbvGrd:float,
                 Fireplaces :float,
                 GarageYrBlt :int,
                 GarageCars : float,
                 GarageArea : float,
                 WoodDeckSF : float,
                 OpenPorchSF :float,
                 EnclosedPorch:float,
                #  H3SsnPorch : float,
                 ScreenPorch :float,
                 PoolArea :float,
                 MiscVal : float,
                 MoSold : float,
                 YrSold : int,
                 
                #  categorical--------------
               
                 MSZoning :str,
                 Street:str ,
                 Alley :str,
                 LotShape : str,
                 LandContour :str,
                 Utilities : str,
                 LotConfig : str,
                 LandSlope : str,
                 Neighborhood:str,
                 Condition1 :str,
                 Condition2 :str,
                 BldgType : str,
                 HouseStyle : str,
                 RoofStyle : str,
                 Exterior1st :str,
                 Exterior2nd :str,
                         
                 MasVnrType :str,
                 ExterQual : str,
                 ExterCond : str,
                 Foundation : str,
                 BsmtQual : str,
                 BsmtCond :str,
                         
                 BsmtExposure:str,
                 BsmtFinType1: str,
                 BsmtFinType2:str,
                 Heating : str,
                 HeatingQC : str,
                 CentralAir : str,
                 Electrical :str,
                 KitchenQual :str,
                 Functional : str,
                 FireplaceQu :str,
                 GarageType : str,
                 GarageFinish:str,
                 GarageQual : str,
                 GarageCond : str,
                 PavedDrive : str,
                 PoolQC : str,
                 Fence :str,
                         
                 MiscFeature =str,
                 SaleType = str,
                 SaleCondition=str,  
                 RoofMatl=str,
           
                 #target feature----------
                 SalePrice : float = None
                 ):
         
        try:
            self.MSSubClass =MSSubClass,
            self.LotFrontage =LotFrontage,
            self.LotArea = LotArea,
            self.OverallQual =OverallQual,
            self.OverallCond =OverallCond,
            self.YearBuilt = YearBuilt,
            self.YearRemodAdd=YearRemodAdd,
           
            self.BsmtFinSF1 =BsmtFinSF1,
            self.BsmtFinSF2 =BsmtFinSF2,
            self.BsmtUnfSF = BsmtUnfSF,
            self.TotalBsmtSF =TotalBsmtSF,
            # self.H1stFlrSF =H1stFlrSF,
            # self.H2ndFlrSF = H2ndFlrSF,
            self.LowQualFinSF=LowQualFinSF,
            self.GrLivArea = GrLivArea,
            self.BsmtFullBath=BsmtFullBath,
            self.FullBath = FullBath,
            self.HalfBath = HalfBath,
            self.BedroomAbvGr=BedroomAbvGr,
            self.KitchenAbvGr=KitchenAbvGr,
            self.TotRmsAbvGrd=TotRmsAbvGrd,
            self.Fireplaces =Fireplaces,
            self.GarageYrBlt =GarageYrBlt,
            self.GarageCars = GarageCars,
            self.GarageArea = GarageArea,
            self.WoodDeckSF = WoodDeckSF,
            self.OpenPorchSF =OpenPorchSF,
            self.EnclosedPorch=EnclosedPorch,
            # self.H3SsnPorch = H3SsnPorch,
            self.ScreenPorch =ScreenPorch,
            self.PoolArea = PoolArea,
            self.MiscVal = MiscVal,
            self.MoSold = MoSold,
            self.YrSold = YrSold,
            
            ##      categ
            self.MSZoning = MSZoning,
            self.Street =Street ,
            self.Alley = Alley,
            self.LotShape = LotShape,
            self.LandContour =LandContour,
            self.Utilities = Utilities,
            self.LotConfig = LotConfig,
            self.LandSlope = LandSlope,
            self.Neighborhood=Neighborhood,
            self.Condition1 = Condition1,
            self.Condition2 = Condition2,
            self.BldgType = BldgType,
            self.HouseStyle = HouseStyle,
            self.RoofStyle = RoofStyle,
            self.Exterior1st =Exterior1st,
            self.Exterior2nd =Exterior2nd,
            self.MasVnrType = MasVnrType,
            self.ExterQual = ExterQual,
            self.ExterCond = ExterCond,
            self.Foundation = Foundation,
            self.BsmtQual = BsmtQual,
            self.BsmtCond = BsmtCond,
            self.BsmtExposure=BsmtExposure,
            self.BsmtFinType1= BsmtFinType1,
            self.BsmtFinType2=BsmtFinType2,
            self.Heating = Heating,
            self.HeatingQC = HeatingQC,
            self.CentralAir = CentralAir,
            self.Electrical = Electrical,
            self.KitchenQual =KitchenQual,
            self.Functional = Functional,
            self.FireplaceQu =FireplaceQu,
            self.GarageType = GarageType,
            self.GarageFinish=GarageFinish,
            self.GarageQual = GarageQual,
            self.GarageCond = GarageCond,
            self.PavedDrive = PavedDrive,
            self.PoolQC = PoolQC,
            self.Fence = Fence,
            self.MiscFeature =MiscFeature,
            self.SaleType = SaleType,
            self.SaleCondition=SaleCondition
            self.MasVnrArea=MasVnrArea
            self.RoofMatl=RoofMatl

            # output feature--------
            self.SalePrice = SalePrice
                                   
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_housing_input_data_frame(self):

        try:
            housing_input_dict = self.get_housing_data_as_dict()
            return pd.DataFrame(housing_input_dict)
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_housing_data_as_dict(self):
        try:
            input_data = {
                "MSSubClass":[self.MSSubClass],
                "MSZoning":[ self.MSZoning],

                "LotFrontage":[self.LotFrontage],
                "LotArea":[ self.LotArea],
                "Street" :[ self.Street],
                "Alley":[ self.Alley],
                "LotShape":[ self.LotShape],
                "LandContour":[ self.LandContour],
                "Utilities":[ self.Utilities],
                "LotConfig":[ self.LotConfig ],
                "LandSlope":[ self.LandSlope ],
                "Neighborhood":[ self.Neighborhood],
                "Condition1":[self.Condition1],
                "Condition2":[self.Condition2],
                "BldgType":[ self.BldgType],
                "HouseStyle":[ self.HouseStyle],
                "OverallQual":[self.OverallQual],
                "OverallCond":[self.OverallCond],
                "YearBuilt":[self.YearBuilt],
                "YearRemodAdd":[ self.YearRemodAdd],                
                "RoofStyle":[ self.RoofStyle],
                "RoofMatl":[self.RoofMatl],

                # ---RoofMatl need to add---
                "Exterior1st":[ self.Exterior1st],
                "Exterior2nd":[ self.Exterior2nd],
                "MasVnrType":[ self.MasVnrType],
                "MasVnrArea":[self.MasVnrArea],

                "ExterQual":[ self.ExterQual],
                "ExterCond":[self.ExterCond],
                "Foundation":[ self.Foundation],
                "BsmtQual":[ self.BsmtQual ],
                "BsmtCond":[ self.BsmtCond],
                "BsmtExposure":[ self.BsmtExposure],
                "BsmtFinType1":[ self.BsmtFinType1],
                "BsmtFinSF1":[self.BsmtFinSF1],

                "BsmtFinType2":[ self.BsmtFinType2],

                "BsmtFinSF2":[ self.BsmtFinSF2],
                "BsmtUnfSF":[self.BsmtUnfSF],
                "TotalBsmtSF":[self.TotalBsmtSF],
                "Heating":[self.Heating],
                "HeatingQC":[self.HeatingQC],
                "CentralAir":[ self.CentralAir],
                "Electrical":[ self.Electrical],

                
                # "H1stFlrSF":[self.H1stFlrSF],
                # "H2ndFlrSF":[self.H2ndFlrSF],
                "LowQualFinSF":[self.LowQualFinSF],

                "GrLivArea":[ self.GrLivArea],
                "BsmtFullBath":[self.BsmtFullBath],
                "FullBath":[self.FullBath],
                "HalfBath":[self.HalfBath],
                "BedroomAbvGr":[ self.BedroomAbvGr],
                "KitchenAbvGr":[ self.KitchenAbvGr],
                "KitchenQual":[ self.KitchenQual],
                "TotRmsAbvGrd":[ self.TotRmsAbvGrd],
                "Functional":[ self.Functional],
                "Fireplaces":[ self.Fireplaces],

                "FireplaceQu":[ self.FireplaceQu],
                "GarageType":[ self.GarageType],
                "GarageYrBlt":[ self.GarageYrBlt ],
                "GarageFinish":[ self.GarageFinish],
                "GarageCars":[ self.GarageCars ],
                "GarageArea":[ self.GarageArea ],
                "GarageQual":[ self.GarageQual],
                "GarageCond":[ self.GarageCond],
                "PavedDrive":[ self.PavedDrive],
                "WoodDeckSF":[ self.WoodDeckSF],
                "OpenPorchSF":[ self.OpenPorchSF ],
                "EnclosedPorch":[ self.EnclosedPorch],
                # "H3SsnPorch":[self.H3SsnPorch],
                "ScreenPorch":[ self.ScreenPorch],
                "PoolArea":[ self.PoolArea],
                "PoolQC":[ self.PoolQC],
                "Fence":[self.Fence],
                "MiscFeature":[ self.MiscFeature],
                "MiscVal":[ self.MiscVal],
                "MoSold":[ self.MoSold],
                "YrSold":[ self.YrSold],
                "SaleType":[ self.SaleType],
                "SaleCondition":[self.SaleCondition],

                
                
                
                
                
                
                
                 

               
                
                
                
                
                
                
                
                
     
                 # output feature--------
                #  "SalePrice":[self.SalePrice]
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
            print(model.preprocessing_object)

            # transformed_feature = model.preprocessing_object.transform(X)
            # return model.trained_model_object.predict(transformed_feature)

            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise HousingException(e, sys) from e