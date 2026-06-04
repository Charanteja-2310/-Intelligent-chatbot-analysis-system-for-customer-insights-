import pandas as pd


def calculate_product_scores(df):

    product_stats = (
        df.groupby("product_name")
        .agg(
            Average_Rating=("Rate", "mean"),
            Review_Count=("Rate", "count"),
            Average_Price=("product_price", "mean")
        )
        .reset_index()
    )

    max_reviews = product_stats[
        "Review_Count"
    ].max()

    product_stats["Popularity_Score"] = (
        product_stats["Review_Count"]
        / max_reviews
    ) * 100

    product_stats["Recommendation_Score"] = (
        product_stats["Average_Rating"] * 0.7
        +
        (
            product_stats["Popularity_Score"]
            / 100
        ) * 5 * 0.3
    )

    product_stats = product_stats.sort_values(
        "Recommendation_Score",
        ascending=False
    )

    return product_stats


def get_top_products(df, top_n=10):

    products = calculate_product_scores(df)

    return products.head(top_n)


def get_worst_products(df, top_n=10):

    products = calculate_product_scores(df)

    return products.sort_values(
        "Recommendation_Score"
    ).head(top_n)


def get_most_reviewed_products(df, top_n=10):

    return (
        df.groupby("product_name")
        .size()
        .reset_index(name="Total_Reviews")
        .sort_values(
            "Total_Reviews",
            ascending=False
        )
        .head(top_n)
    )


def get_best_value_products(
    df,
    top_n=10
):

    temp = (
        df.groupby("product_name")
        .agg(
            Rating=("Rate", "mean"),
            Price=("product_price", "mean")
        )
        .reset_index()
    )

    temp = temp[
        temp["Price"] > 0
    ]

    temp["Value_Score"] = (
        temp["Rating"]
        / temp["Price"]
    ) * 10000

    return temp.sort_values(
        "Value_Score",
        ascending=False
    ).head(top_n)


def recommend_under_budget(
    df,
    budget
):

    products = (
        df.groupby("product_name")
        .agg(
            Rating=("Rate", "mean"),
            Price=("product_price", "mean")
        )
        .reset_index()
    )

    products = products[
        products["Price"] <= budget
    ]

    products = products.sort_values(
        "Rating",
        ascending=False
    )

    return products.head(10)


def product_search(
    df,
    keyword
):

    return df[
        df["product_name"]
        .astype(str)
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]