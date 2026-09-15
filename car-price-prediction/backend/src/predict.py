import joblib
import pandas as pd
from pathlib import Path


# =========================================================
# MODEL PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"


# =========================================================
# LOAD MODELS
# =========================================================

models = {
    "linear_regression": joblib.load(
        MODEL_DIR / "linear_regression.pkl"
    ),

    "random_forest": joblib.load(
        MODEL_DIR / "random_forest.pkl"
    ),

    "random_forest_tuned": joblib.load(
        MODEL_DIR / "random_forest_tuned.pkl"
    )
}


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_price(
    company,
    fuel_type,
    car_age,
    kms_driven,
    model_name="random_forest"
):

    # Check model name
    if model_name not in models:
        raise ValueError(
            f"Invalid model: {model_name}"
        )


    # Create input DataFrame
    input_data = pd.DataFrame({

        "car_age": [car_age],

        "kms_driven": [kms_driven],

        "company": [company],

        "fuel_type": [fuel_type]
    })


    # Select model
    model = models[model_name]


    # Make prediction
    prediction = model.predict(
        input_data
    )[0]


    return prediction


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    prediction = predict_price(

        company="Maruti",

        fuel_type="Petrol",

        car_age=5,

        kms_driven=45000,

        model_name="random_forest"
    )


    print("\nCar Price Prediction")
    print("--------------------")

    print(
        f"Predicted Price: ₹{prediction:,.2f}"
    )