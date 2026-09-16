import os
import json
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from ml.preprocessing import load_data, preprocess_data


def train_models():

    df = load_data()
    df = preprocess_data(df)

    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {
        "logistic": LogisticRegression(),
        "decision_tree": DecisionTreeClassifier(
            max_depth=4,
            random_state=42
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ),
        "knn": KNeighborsClassifier(
            n_neighbors=5
        ),
        "svm": SVC(
            kernel="rbf",
            probability=True,
            random_state=42
        ),
        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        ),
        "xgboost": XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42,
            eval_metric="logloss"
        )
    }

    scaled_models = [
        "logistic",
        "knn",
        "svm"
    ]

    os.makedirs("models", exist_ok=True)
    os.makedirs("performance", exist_ok=True)

    metrics = {}

    for model_name, model in models.items():

        if model_name in scaled_models:

            scaler = StandardScaler()

            X_train_model = scaler.fit_transform(X_train)
            X_test_model = scaler.transform(X_test)

            with open(
                f"models/{model_name}_scaler.pkl",
                "wb"
            ) as file:
                pickle.dump(scaler, file)

        else:

            X_train_model = X_train
            X_test_model = X_test

        model.fit(X_train_model, y_train)

        y_pred = model.predict(X_test_model)

        metrics[model_name] = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred)
        }

        with open(
            f"models/{model_name}_model.pkl",
            "wb"
        ) as file:
            pickle.dump(model, file)

        print(f"{model_name} trained successfully!")

    with open(
        "performance/metrics.json",
        "w"
    ) as file:
        json.dump(metrics, file, indent=4)

    print("\nAll models trained successfully!")
    print("Models saved in models/")
    print("Metrics saved in performance/metrics.json")


if __name__ == "__main__":
    train_models()