import pandas as pd


def clean_data(df):
    """
    Clean the raw car dataset and return a cleaned DataFrame.
    """

    clean_df = df.copy()

    # 1. Standardize column names
    clean_df.columns = (
        clean_df.columns
        .str.strip()
        .str.lower()
    )

    # 2. Remove duplicate rows
    clean_df = clean_df.drop_duplicates()

    # 3. Clean price
    clean_df["price"] = (
        clean_df["price"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"(\d+(?:\.\d+)?)")[0]
    )

    clean_df["price"] = pd.to_numeric(
        clean_df["price"],
        errors="coerce"
    )

    # Price is the target, so rows without price
    # cannot be used for supervised training
    clean_df = clean_df.dropna(subset=["price"])

    # 4. Clean year
    clean_df["year"] = pd.to_numeric(
        clean_df["year"],
        errors="coerce"
    )

    # 5. Clean kilometres driven
    clean_df["kms_driven"] = (
        clean_df["kms_driven"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"(\d+(?:\.\d+)?)")[0]
    )

    clean_df["kms_driven"] = pd.to_numeric(
        clean_df["kms_driven"],
        errors="coerce"
    )

    # 6. Clean categorical columns
    clean_df["company"] = (
        clean_df["company"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    clean_df["fuel_type"] = (
        clean_df["fuel_type"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # 7. Feature engineering
    current_year = 2026

    clean_df["car_age"] = (
        current_year - clean_df["year"]
    )

    return clean_df 