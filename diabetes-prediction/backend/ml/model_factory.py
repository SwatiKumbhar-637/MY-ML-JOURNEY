import pickle
import os

from config.model_config import MODEL_CONFIG


def load_models():

    models = {}

    for model_name, config in MODEL_CONFIG.items():

        model_path = config["file"]

        with open(model_path, "rb") as file:
            model = pickle.load(file)

        models[model_name] = model

    return models


def load_scalers():

    scalers = {}

    for model_name, config in MODEL_CONFIG.items():

        scaler_path = config["scaler"]

        if scaler_path is not None:

            with open(scaler_path, "rb") as file:
                scaler = pickle.load(file)

            scalers[model_name] = scaler

    return scalers