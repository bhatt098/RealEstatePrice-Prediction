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
        transaction_date = float(request.form['transaction_date'])
        house_age = float(request.form['house_age'])
        distance_MRT_station = float(request.form['distance_MRT_station'])
        convenience_stores = float(request.form['convenience_stores'])
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
       
        housing_data = HousingData(

                                   transaction_date =transaction_date,
                                   house_age =house_age,
                                   distance_MRT_station = distance_MRT_station,
                                   convenience_stores =convenience_stores,
                                   latitude =latitude,
                                   longitude = longitude,
                                           
                                   )
        housing_df = housing_data.get_housing_input_data_frame()
        # housing_df=housing_df.to_string()
        file_name = os.listdir(MODEL_DIR)[0]
        housing_predictor = HousingPredictor(model_dir=MODEL_DIR)
        median_housing_value = housing_predictor.predict(housing_df)
        context = {
            HOUSING_DATA_KEY: housing_data.get_housing_data_as_dict(),
            MEDIAN_HOUSING_VALUE_KEY: median_housing_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


if __name__ == "__main__":
    app.run()