import numpy as np
import pandas as pd


INVALID_ZERO_COLUMNS = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI"
]


def load_data():
    return pd.read_csv("data/diabetes.csv")


def preprocess_data(df):

    df = df.copy()

    for column in INVALID_ZERO_COLUMNS:
        df[column] = df[column].replace(0, np.nan)
        df[column] = df[column].fillna(df[column].median())

    return df