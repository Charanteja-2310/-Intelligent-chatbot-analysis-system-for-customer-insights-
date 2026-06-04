import pandas as pd

def load_data():

    df = pd.read_csv(
        "dataset/Dataset-SA.csv"
    )

    df["Rate"] = pd.to_numeric(
        df["Rate"],
        errors="coerce"
    )

    df["product_price"] = pd.to_numeric(
        df["product_price"],
        errors="coerce"
    )

    # Fill missing review text

    df["Summary"] = (
        df["Summary"]
        .fillna("")
        .astype(str)
    )

    df["Review"] = (
        df["Review"]
        .fillna("")
        .astype(str)
    )

    # Review Length

    df["Review_Length"] = (
        df["Summary"]
        .str.len()
    )

    df = df.dropna(
        subset=["Rate"]
    )

    return df