import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from joblib import load
import json

description = """
Welcome to the GetAround API, designed to assist you in predicting the rental price for your car!

Here are the available endpoints:

* `/`: This endpoint is provided as an example. You can explore its functionality.
* `/predict`: This endpoint accepts a POST request with JSON input data. You can use this endpoint to make predictions by providing the necessary information about your car.
Feel free to use the `/predict` endpoint by sending a POST request with the required JSON data to obtain accurate rental price predictions for your vehicule
"""

tags_metadata = [
    {
        "name": "Simple Endpoint",
        "description": "Simple endpoint to try out!",
    },
    {
        "name": "Prediction",
        "description": "Prediction of the rental price based"
    }
]

app = FastAPI(
    title="🚙 GetAround price prediction API ",
    description=description,
    version="0.1",
    contact={
        "name": "GetAround API - by Delphine Cesar",
        "url": "https://github.com/delphinecesar",
    }, 
    openapi_tags=tags_metadata,
)



# data types
class PredictionFeatures(BaseModel):
    model_key: str = "Peugeot"
    mileage: int = 13131
    engine_power: int = 110
    fuel: str = "diesel"
    paint_color: str = "grey"
    car_type: str = "convertible"
    private_parking_available: bool = False
    has_gps: bool = True
    has_air_conditioning: bool = True
    automatic_car: bool = False
    has_getaround_connect: bool = True
    has_speed_regulator: bool = False
    winter_tires: bool = True


@app.get("/", tags=["Simple Endpoint"])
async def index():
    return {"Hello World!"}

@app.post("/predict", tags=["Prediction"])
async def predict(features: PredictionFeatures):
    # data
    information = pd.DataFrame(features.dict(), index =[0])
    
    # preprocessor & model loading
    model = load('model.joblib')
    
    #prediction
    prediction = model.predict(information)

    # response
    response = {"prediction": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)