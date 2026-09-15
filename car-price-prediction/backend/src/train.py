import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from src.data_cleaning import clean_data
from src.preprocessing import create_preprocessor
from src.model_analysis import get_feature_importance


# =========================================================
# LOAD AND PREPARE DATA
# =========================================================

def load_and_prepare_data():

    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data" / "quikr_car.csv"

    df = pd.read_csv(DATA_PATH)

    # Clean data
    df = clean_data(df)

    # Features
    X = df[
        [
            "car_age",
            "kms_driven",
            "company",
            "fuel_type"
        ]
    ]

    # Target
    y = df["price"]

    return X, y


# =========================================================
# CREATE MODELS
# =========================================================

def create_models():

    # Linear Regression
    linear_model = Pipeline([
        ("preprocessor", create_preprocessor()),
        ("regressor", LinearRegression())
    ])

    # Baseline Random Forest
    random_forest_model = Pipeline([
        ("preprocessor", create_preprocessor()),
        ("regressor", RandomForestRegressor(
            n_estimators=200,
            random_state=42
        ))
    ])

    return linear_model, random_forest_model


# =========================================================
# MODEL EVALUATION
# =========================================================

def evaluate_model(model, X_test, y_test):

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

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2
    }


# =========================================================
# TRAIN MODELS
# =========================================================

def train_models():

    # -----------------------------------------------------
    # 1. Load data
    # -----------------------------------------------------

    X, y = load_and_prepare_data()


    # -----------------------------------------------------
    # 2. Train-Test Split
    # -----------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    # -----------------------------------------------------
    # 3. Create models
    # -----------------------------------------------------

    linear_model, random_forest_model = create_models()


    # -----------------------------------------------------
    # 4. Train Linear Regression
    # -----------------------------------------------------

    linear_model.fit(
        X_train,
        y_train
    )


    # -----------------------------------------------------
    # 5. Train Baseline Random Forest
    # -----------------------------------------------------

    random_forest_model.fit(
        X_train,
        y_train
    )


    # =====================================================
    # 6. RANDOM FOREST HYPERPARAMETER TUNING
    # =====================================================

    param_grid = {

        "regressor__n_estimators": [
            100,
            200,
            300
        ],

        "regressor__max_depth": [
            5,
            10,
            15
        ],

        "regressor__min_samples_split": [
            2,
            5
        ],

        "regressor__min_samples_leaf": [
            1,
            2
        ]
    }


    grid_search = GridSearchCV(

        estimator=random_forest_model,

        param_grid=param_grid,

        cv=5,

        scoring="r2",

        n_jobs=-1
    )


    grid_search.fit(
        X_train,
        y_train
    )


    # -----------------------------------------------------
    # Best parameters
    # -----------------------------------------------------

    print("\nBest Hyperparameters")
    print("--------------------")

    print(
        grid_search.best_params_
    )


    # -----------------------------------------------------
    # Best cross-validation score
    # -----------------------------------------------------

    print("\nBest Cross-Validation R2")
    print("------------------------")

    print(
        grid_search.best_score_
    )


    # -----------------------------------------------------
    # Get best tuned model
    # -----------------------------------------------------

    tuned_random_forest = (
        grid_search.best_estimator_
    )


    # =====================================================
    # 7. MODEL EVALUATION
    # =====================================================

    # Linear Regression
    linear_results = evaluate_model(
        linear_model,
        X_test,
        y_test
    )


    # Baseline Random Forest
    rf_results = evaluate_model(
        random_forest_model,
        X_test,
        y_test
    )


    # Tuned Random Forest
    tuned_rf_results = evaluate_model(
        tuned_random_forest,
        X_test,
        y_test
    )


    # =====================================================
    # 8. RESIDUAL ANALYSIS
    # =====================================================

    tuned_predictions = (
        tuned_random_forest.predict(X_test)
    )

    residuals = (
        y_test - tuned_predictions
    )


    print("\nResidual Analysis")
    print("-----------------")

    print(
        "Mean Residual:",
        residuals.mean()
    )

    print(
        "Minimum Residual:",
        residuals.min()
    )

    print(
        "Maximum Residual:",
        residuals.max()
    )


    # =====================================================
    # 9. FEATURE IMPORTANCE
    # =====================================================

    feature_importance, grouped_importance = (
        get_feature_importance(
            random_forest_model
        )
    )


    # =====================================================
    # 10. SAVE MODELS
    # =====================================================

    BASE_DIR = Path(__file__).resolve().parent.parent

    MODEL_DIR = BASE_DIR / "models"

    MODEL_DIR.mkdir(
        exist_ok=True
    )


    # Linear Regression
    joblib.dump(
        linear_model,
        MODEL_DIR / "linear_regression.pkl"
    )


    # Baseline Random Forest
    joblib.dump(
        random_forest_model,
        MODEL_DIR / "random_forest.pkl"
    )


    # Tuned Random Forest
    joblib.dump(
        tuned_random_forest,
        MODEL_DIR / "random_forest_tuned.pkl"
    )


    print("\nModels saved successfully!")


    # =====================================================
    # RETURN EVERYTHING
    # =====================================================

    return (

        linear_model,

        random_forest_model,

        tuned_random_forest,

        linear_results,

        rf_results,

        tuned_rf_results,

        feature_importance,

        grouped_importance
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    (
        linear_model,

        random_forest_model,

        tuned_random_forest,

        linear_results,

        rf_results,

        tuned_rf_results,

        feature_importance,

        grouped_importance

    ) = train_models()


    # =====================================================
    # LINEAR REGRESSION RESULTS
    # =====================================================

    print("\nLinear Regression")
    print("-----------------")

    print(
        "MAE :",
        linear_results["mae"]
    )

    print(
        "RMSE:",
        linear_results["rmse"]
    )

    print(
        "R2  :",
        linear_results["r2"]
    )


    # =====================================================
    # RANDOM FOREST RESULTS
    # =====================================================

    print("\nRandom Forest")
    print("-----------------")

    print(
        "MAE :",
        rf_results["mae"]
    )

    print(
        "RMSE:",
        rf_results["rmse"]
    )

    print(
        "R2  :",
        rf_results["r2"]
    )


    # =====================================================
    # TUNED RANDOM FOREST RESULTS
    # =====================================================

    print("\nTuned Random Forest")
    print("-------------------")

    print(
        "MAE :",
        tuned_rf_results["mae"]
    )

    print(
        "RMSE:",
        tuned_rf_results["rmse"]
    )

    print(
        "R2  :",
        tuned_rf_results["r2"]
    )


    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    print("\nGrouped Feature Importance")
    print("--------------------------")

    print(
        grouped_importance
    )