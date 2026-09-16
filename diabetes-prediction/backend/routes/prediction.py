from flask import Blueprint, request, jsonify
import numpy as np
import json
from ml.model_factory import load_models, load_scalers


prediction_bp = Blueprint("prediction", __name__)

models = load_models()
scalers = load_scalers()

@prediction_bp.route("/models", methods=["GET"])
def get_models():

    return jsonify({
        "models": list(models.keys())
    })

@prediction_bp.route("/predict", methods=["POST"])
def predict():

    data = request.json

    model_name = data["model"]

    if model_name not in models:
        return jsonify({
            "error": "Invalid model selected"
        }), 400

    model = models[model_name]

    input_data = np.array([[
        float(data["Pregnancies"]),
        float(data["Glucose"]),
        float(data["BloodPressure"]),
        float(data["SkinThickness"]),
        float(data["Insulin"]),
        float(data["BMI"]),
        float(data["DiabetesPedigreeFunction"]),
        float(data["Age"])
    ]])

    if model_name in scalers:
        input_data = scalers[model_name].transform(input_data)

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    if prediction[0] == 1:
        result = "Diabetes Detected"
    else:
        result = "No Diabetes"

    return jsonify({
        "prediction": int(prediction[0]),
        "result": result,
        "probability": float(probability[0][1])
    })