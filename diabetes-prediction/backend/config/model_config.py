MODEL_CONFIG = {
    "logistic": {
        "file": "models/logistic_model.pkl",
        "scaler": "models/logistic_scaler.pkl"
    },

    "decision_tree": {
        "file": "models/decision_tree_model.pkl",
        "scaler": None
    },

    "random_forest": {
        "file": "models/random_forest_model.pkl",
        "scaler": None
    },

    "knn": {
        "file": "models/knn_model.pkl",
        "scaler": "models/knn_scaler.pkl"
    },

    "svm": {
        "file": "models/svm_model.pkl",
        "scaler": "models/svm_scaler.pkl"
    },

    "gradient_boosting": {
        "file": "models/gradient_boosting_model.pkl",
        "scaler": None
    },

    "xgboost": {
        "file": "models/xgboost_model.pkl",
        "scaler": None
    }
}