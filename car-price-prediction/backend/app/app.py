from flask import Flask, request, jsonify
from flask_cors import CORS

from src.predict import predict_price
from src.data_cleaning import clean_data

import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

CORS(app)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "quikr_car.csv"
MODEL_DIR = BASE_DIR / "models"


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_PATH)

df = clean_data(df)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "message": "Car Price Prediction API is running"
    })


# =========================================================
# DROPDOWN OPTIONS
# =========================================================

@app.route("/options", methods=["GET"])
def get_options():

    companies = sorted(
        df["company"]
        .dropna()
        .unique()
        .tolist()
    )

    fuel_types = sorted(
        df["fuel_type"]
        .dropna()
        .unique()
        .tolist()
    )

    models = [
        "linear_regression",
        "random_forest",
        "random_forest_tuned"
    ]

    return jsonify({
        "companies": companies,
        "fuel_types": fuel_types,
        "models": models
    })


# =========================================================
# PREDICTION
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        company = data["company"]
        fuel_type = data["fuel_type"]
        car_age = float(data["car_age"])
        kms_driven = float(data["kms_driven"])

        model_name = data.get(
            "model",
            "random_forest"
        )

        prediction = predict_price(
            company=company,
            fuel_type=fuel_type,
            car_age=car_age,
            kms_driven=kms_driven,
            model_name=model_name
        )

        return jsonify({
            "success": True,
            "model": model_name,
            "predicted_price": round(
                float(prediction),
                2
            )
        })

    except KeyError as e:

        return jsonify({
            "success": False,
            "error": f"Missing field: {str(e)}"
        }), 400

    except ValueError as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# MODEL EVALUATION
# =========================================================

@app.route("/evaluation", methods=["GET"])
def evaluation():

    try:

        # -----------------------------
        # Prepare data
        # -----------------------------

        X = df[
            [
                "car_age",
                "kms_driven",
                "company",
                "fuel_type"
            ]
        ]

        y = df["price"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )


        # -----------------------------
        # Load trained models
        # -----------------------------

        linear_model = joblib.load(
            MODEL_DIR / "linear_regression.pkl"
        )

        random_forest = joblib.load(
            MODEL_DIR / "random_forest.pkl"
        )

        tuned_random_forest = joblib.load(
            MODEL_DIR / "random_forest_tuned.pkl"
        )


        # -----------------------------
        # Evaluate models
        # -----------------------------

        model_objects = {
            "linear_regression": linear_model,
            "random_forest": random_forest,
            "random_forest_tuned": tuned_random_forest
        }


        results = {}

        for name, model in model_objects.items():

            predictions = model.predict(X_test)

            mae = mean_absolute_error(
                y_test,
                predictions
            )

            rmse = mean_squared_error(
                y_test,
                predictions
            ) ** 0.5

            r2 = r2_score(
                y_test,
                predictions
            )

            results[name] = {
                "mae": round(float(mae), 2),
                "rmse": round(float(rmse), 2),
                "r2": round(float(r2), 4)
            }


        # -----------------------------
        # Feature importance
        # -----------------------------

        rf_pipeline = random_forest

        preprocessor = rf_pipeline.named_steps[
            "preprocessor"
        ]

        rf_model = rf_pipeline.named_steps[
            "regressor"
        ]

        feature_names = (
            preprocessor
            .get_feature_names_out()
        )

        importances = rf_model.feature_importances_


        feature_data = []

        for feature, importance in zip(
            feature_names,
            importances
        ):

            feature_data.append({
                "feature": feature,
                "importance": round(
                    float(importance),
                    6
                )
            })


        return jsonify({
            "success": True,
            "models": results,
            "feature_importance": feature_data
        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )