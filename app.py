from flask import Flask,render_template,request
from housing.entity.housing_prediction import HousingData,HousingPredictor
import os
HOUSING_DATA_KEY = "housing_data"
MEDIAN_HOUSING_VALUE_KEY = "Sale_Price"
SAVED_MODELS_DIR_NAME = "saved_models"
ROOT_DIR = os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


app=Flask(__name__)

@app.route('/',methods=['Get','POST'])
def run():
    # return "kkkkkk"
    return render_template("predict.html")


@app.route('/predict',methods=['GET','POST'])
def predict():
    context = {
        HOUSING_DATA_KEY: None,
        MEDIAN_HOUSING_VALUE_KEY: None
    }

    if request.method == "POST":
        ########      numerical variable        ######
        MSSubClass = float(request.form['MSSubClass'])
        LotFrontage = float(request.form['LotFrontage'])
        LotArea = float(request.form['LotArea'])
        OverallQual = float(request.form['OverallQual'])
        OverallCond = float(request.form['OverallCond'])
        YearBuilt = int(request.form['YearBuilt'])
        
        YearRemodAdd = int(request.form['YearRemodAdd'])
        MasVnrArea = float(request.form['MasVnrArea'])
        BsmtFinSF1 = float(request.form['BsmtFinSF1'])
        BsmtFinSF2 = float(request.form['BsmtFinSF2'])
        
        BsmtUnfSF = float(request.form['BsmtUnfSF'])
        TotalBsmtSF = float(request.form['TotalBsmtSF'])
        
        # H1stFlrSF = float(request.form['H1stFlrSF'])
        # H2ndFlrSF = float(request.form['H2ndFlrSF'])
        LowQualFinSF = float(request.form['LowQualFinSF'])
        GrLivArea = float(request.form['GrLivArea'])
        BsmtFullBath = float(request.form['BsmtFullBath'])
        FullBath = float(request.form['FullBath'])
        HalfBath = float(request.form['HalfBath'])
        BedroomAbvGr = float(request.form['BedroomAbvGr'])
        KitchenAbvGr = float(request.form['KitchenAbvGr'])
        TotRmsAbvGrd = float(request.form['TotRmsAbvGrd'])
        Fireplaces = float(request.form['Fireplaces'])
        GarageYrBlt = int(request.form['GarageYrBlt'])
        
        
        GarageCars = float(request.form['GarageCars'])
        GarageArea = float(request.form['GarageArea'])
        WoodDeckSF = float(request.form['WoodDeckSF'])
        OpenPorchSF = float(request.form['OpenPorchSF'])
        EnclosedPorch = float(request.form['EnclosedPorch'])
        # H3SsnPorch = float(request.form['H3SsnPorch'])
        
        ScreenPorch = float(request.form['ScreenPorch'])
        PoolArea = float(request.form['PoolArea'])
        MiscVal = float(request.form['MiscVal'])
        MoSold = float(request.form['MoSold'])
        YrSold = int(request.form['YrSold'])

        ##      categorical           #######
        MSZoning = request.form['MSZoning']
        Street = request.form['Street']
        Alley = request.form['Alley']
        LotShape = request.form['LotShape']
        LandContour = request.form['LandContour']
        Utilities = request.form['Utilities']
        LotConfig = request.form['LotConfig']
        LandSlope = request.form['LandSlope']
        Neighborhood = request.form['Neighborhood']
        Condition1 = request.form['Condition1']
        Condition2 = request.form['Condition2']
        BldgType = request.form['BldgType']
        HouseStyle = request.form['HouseStyle']
        RoofStyle = request.form['RoofStyle']
        Exterior1st = request.form['Exterior1st']
        Exterior2nd = request.form['Exterior2nd']
        
        MasVnrType = request.form['MasVnrType']
        ExterQual = request.form['ExterQual']
        ExterCond = request.form['ExterCond']
        Foundation = request.form['Foundation']
        BsmtQual = request.form['BsmtQual']
        BsmtCond = request.form['BsmtCond']
        
        BsmtExposure = request.form['BsmtExposure']
        BsmtFinType1 = request.form['BsmtFinType1']
        BsmtFinType2 = request.form['BsmtFinType2']
        Heating = request.form['Heating']
        HeatingQC = request.form['HeatingQC']
        CentralAir = request.form['CentralAir']
        Electrical = request.form['Electrical']
        KitchenQual = request.form['KitchenQual']
        Functional = request.form['Functional']
        FireplaceQu = request.form['FireplaceQu']
        GarageType = request.form['GarageType']
        GarageFinish = request.form['GarageFinish']
        GarageQual = request.form['GarageQual']
        GarageCond = request.form['GarageCond']
        PavedDrive = request.form['PavedDrive']
        PoolQC = request.form['PoolQC']
        Fence = request.form['Fence']
        
        MiscFeature = request.form['MiscFeature']
        SaleType = request.form['SaleType']
        SaleCondition = request.form['SaleCondition']
        RoofMatl = request.form['RoofMatl']




        

        housing_data = HousingData(

                                   MSSubClass =MSSubClass,
                                   LotFrontage =LotFrontage,
                                   LotArea = LotArea,
                                   OverallQual =OverallQual,
                                   OverallCond =OverallCond,
                                   YearBuilt = YearBuilt,
                                           
                                   YearRemodAdd=YearRemodAdd,
                                   MasVnrArea =MasVnrArea,
                                   BsmtFinSF1 =BsmtFinSF1,
                                   BsmtFinSF2 =BsmtFinSF2,
                                           
                                   BsmtUnfSF = BsmtUnfSF,
                                   TotalBsmtSF =TotalBsmtSF,
                                           
                                #    H1stFlrSF =H1stFlrSF,
                                #    H2ndFlrSF = H2ndFlrSF,
                                   LowQualFinSF=LowQualFinSF,
                                   GrLivArea = GrLivArea,
                                   BsmtFullBath=BsmtFullBath,
                                   FullBath = FullBath,
                                   HalfBath = HalfBath,
                                   BedroomAbvGr=BedroomAbvGr,
                                   KitchenAbvGr=KitchenAbvGr,
                                   TotRmsAbvGrd=TotRmsAbvGrd,
                                   Fireplaces =Fireplaces,
                                   GarageYrBlt =GarageYrBlt,
                                   GarageCars = GarageCars,
                                   GarageArea = GarageArea,
                                   WoodDeckSF = WoodDeckSF,
                                   OpenPorchSF =OpenPorchSF,
                                   EnclosedPorch=EnclosedPorch,
                                #    H3SsnPorch = H3SsnPorch,
                                           
                                   ScreenPorch =ScreenPorch,
                                   PoolArea = PoolArea,
                                   MiscVal = MiscVal,
                                   MoSold = MoSold,
                                   YrSold = YrSold,
                                   
                                   ##      categ
                                   MSZoning = MSZoning,
                                   Street =Street ,
                                   Alley = Alley,
                                   LotShape = LotShape,
                                   LandContour =LandContour,
                                   Utilities = Utilities,
                                   LotConfig = LotConfig,
                                   LandSlope = LandSlope,
                                   Neighborhood=Neighborhood,
                                   Condition1 = Condition1,
                                   Condition2 = Condition2,
                                   BldgType = BldgType,
                                   HouseStyle = HouseStyle,
                                   RoofStyle = RoofStyle,
                                   Exterior1st =Exterior1st,
                                   Exterior2nd =Exterior2nd,
                                           
                                   MasVnrType = MasVnrType,
                                   ExterQual = ExterQual,
                                   ExterCond = ExterCond,
                                   Foundation = Foundation,
                                   BsmtQual = BsmtQual,
                                   BsmtCond = BsmtCond,
                                           
                                   BsmtExposure=BsmtExposure,
                                   BsmtFinType1= BsmtFinType1,
                                   BsmtFinType2=BsmtFinType2,
                                   Heating = Heating,
                                   HeatingQC = HeatingQC,
                                   CentralAir = CentralAir,
                                   Electrical = Electrical,
                                   KitchenQual =KitchenQual,
                                   Functional = Functional,
                                   FireplaceQu =FireplaceQu,
                                   GarageType = GarageType,
                                   GarageFinish=GarageFinish,
                                   GarageQual = GarageQual,
                                   GarageCond = GarageCond,
                                   PavedDrive = PavedDrive,
                                   PoolQC = PoolQC,
                                   Fence = Fence,
                                           
                                   MiscFeature =MiscFeature,
                                   SaleType = SaleType,
                                   SaleCondition=SaleCondition,
                                   RoofMatl=RoofMatl
                                   
                                   
                                   )
        housing_df = housing_data.get_housing_input_data_frame()
        print(housing_df)
        # housing_df=housing_df.to_string()
        file_name = os.listdir(MODEL_DIR)[0]
        housing_predictor = HousingPredictor(model_dir=MODEL_DIR)
        median_housing_value = housing_predictor.predict(X=housing_df)
        context = {
            HOUSING_DATA_KEY: housing_data.get_housing_data_as_dict(),
            MEDIAN_HOUSING_VALUE_KEY: median_housing_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


if __name__ == "__main__":
    app.run()