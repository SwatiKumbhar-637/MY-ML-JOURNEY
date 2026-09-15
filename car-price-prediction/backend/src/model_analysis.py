import pandas as pd


def get_feature_importance(model):

    preprocessor = model.named_steps["preprocessor"]
    regressor = model.named_steps["regressor"]

    feature_names = preprocessor.get_feature_names_out()
    importance = regressor.feature_importances_

    feature_importance = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    })

    feature_importance["original_feature"] = (
        feature_importance["feature"]
        .str.replace("num__", "", regex=False)
        .str.replace("cat__", "", regex=False)
    )

    feature_importance["original_feature"] = (
        feature_importance["original_feature"]
        .apply(
            lambda x:
            "company"
            if x.startswith("company_")
            else "fuel_type"
            if x.startswith("fuel_type_")
            else x
        )
    )

    grouped_importance = (
        feature_importance
        .groupby("original_feature")["importance"]
        .sum()
        .sort_values(ascending=False)
    )

    return feature_importance, grouped_importance