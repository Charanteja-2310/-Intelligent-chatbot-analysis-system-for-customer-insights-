import pandas as pd
import re

from modules.nlp_engine import detect_intent


def chatbot_response(query, df):

    query = str(query).lower().strip()

    intents = {

        "best_products": [
            "best products",
            "top rated products",
            "highest rated products",
            "recommend products",
            "good products"
        ],

        "worst_products": [
            "worst products",
            "bad products",
            "lowest rated products"
        ],

        "most_reviewed": [
            "most purchased products",
            "most reviewed products",
            "popular products",
            "trending products"
        ],

        "average_rating": [
            "average rating",
            "overall rating",
            "rating score"
        ],

        "customer_satisfaction": [
            "customer satisfaction",
            "satisfaction rate",
            "are customers happy"
        ],

        "positive_reviews": [
            "positive reviews",
            "happy customers",
            "satisfied customers"
        ],

        "negative_reviews": [
            "negative reviews",
            "unhappy customers",
            "bad reviews",
            "complaints"
        ],

        "dataset_summary": [
            "dataset summary",
            "business insights",
            "executive summary",
            "generate insights"
        ],

        "complaints": [
            "top complaints",
            "common complaints",
            "customer complaints"
        ]
    }

    intent = detect_intent(query, intents)

    # ====================================
    # TOTAL REVIEWS
    # ====================================

    if any(x in query for x in [
        "total reviews",
        "how many reviews",
        "review count"
    ]):
        return f"Total Reviews: {len(df)}"

    # ====================================
    # TOTAL PRODUCTS
    # ====================================

    if any(x in query for x in [
        "total products",
        "how many products"
    ]):
        return f"Total Products: {df['product_name'].nunique()}"

    # ====================================
    # PRODUCT SEARCH
    # ====================================

    if query.startswith("search"):

        keyword = query.replace(
            "search",
            ""
        ).strip()

        return df[
            df["product_name"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
        ][[
            "product_name",
            "product_price",
            "Rate",
            "Summary"
        ]].head(20)

    # ====================================
    # PRODUCT COMPARISON
    # ====================================

    if "compare" in query and "vs" in query:

        parts = query.replace(
            "compare",
            ""
        ).split("vs")

        if len(parts) == 2:

            p1 = parts[0].strip()
            p2 = parts[1].strip()

            product1 = df[
                df["product_name"]
                .astype(str)
                .str.contains(
                    p1,
                    case=False,
                    na=False
                )
            ]

            product2 = df[
                df["product_name"]
                .astype(str)
                .str.contains(
                    p2,
                    case=False,
                    na=False
                )
            ]

            if len(product1) > 0 and len(product2) > 0:

                return pd.DataFrame({

                    "Metric": [
                        "Average Rating",
                        "Average Price",
                        "Review Count"
                    ],

                    p1: [
                        round(product1["Rate"].mean(), 2),
                        round(product1["product_price"].mean(), 2),
                        len(product1)
                    ],

                    p2: [
                        round(product2["Rate"].mean(), 2),
                        round(product2["product_price"].mean(), 2),
                        len(product2)
                    ]
                })

    # ====================================
    # PRODUCTS UNDER BUDGET
    # ====================================

    budget_match = re.search(
        r'under\s+(\d+)',
        query
    )

    if budget_match:

        budget = int(
            budget_match.group(1)
        )

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

        return (
            products
            .sort_values(
                "Rating",
                ascending=False
            )
            .head(20)
        )

    # ====================================
    # BEST PRODUCTS
    # ====================================

    if intent == "best_products":

        return (
            df.groupby("product_name")
            .agg(
                Rating=("Rate", "mean"),
                Reviews=("Rate", "count"),
                Price=("product_price", "mean")
            )
            .sort_values(
                "Rating",
                ascending=False
            )
            .head(10)
            .reset_index()
        )

    # ====================================
    # WORST PRODUCTS
    # ====================================

    if intent == "worst_products":

        return (
            df.groupby("product_name")
            .agg(
                Rating=("Rate", "mean"),
                Reviews=("Rate", "count")
            )
            .sort_values(
                "Rating"
            )
            .head(10)
            .reset_index()
        )

    # ====================================
    # MOST REVIEWED
    # ====================================

    if intent == "most_reviewed":

        return (
            df.groupby("product_name")
            .size()
            .reset_index(
                name="Reviews"
            )
            .sort_values(
                "Reviews",
                ascending=False
            )
            .head(10)
        )

    # ====================================
    # AVERAGE RATING
    # ====================================

    if intent == "average_rating":

        return (
            f"Average Rating: "
            f"{round(df['Rate'].mean(), 2)}"
        )

    # ====================================
    # POSITIVE REVIEWS
    # ====================================

    if intent == "positive_reviews":

        return df[
            df["Sentiment"] == "Positive"
        ][[
            "product_name",
            "Rate",
            "Summary"
        ]].head(20)

    # ====================================
    # NEGATIVE REVIEWS
    # ====================================

    if intent == "negative_reviews":

        return df[
            df["Sentiment"] == "Negative"
        ][[
            "product_name",
            "Rate",
            "Summary"
        ]].head(20)

    # ====================================
    # CUSTOMER SATISFACTION
    # ====================================

    if intent == "customer_satisfaction":

        positive = (
            df["Sentiment"]
            .astype(str)
            .str.lower()
            .eq("positive")
            .sum()
        )

        score = round(
            (positive / len(df)) * 100,
            2
        )

        return (
            f"Customer Satisfaction "
            f"Rate: {score}%"
        )

    # ====================================
    # COMPLAINT ANALYSIS
    # ====================================

    if intent == "complaints":

        return df[
            df["Sentiment"]
            .astype(str)
            .str.lower()
            .eq("negative")
        ][[
            "product_name",
            "Summary"
        ]].head(20)

    # ====================================
    # AI BUSINESS INSIGHTS
    # ====================================

    if intent == "dataset_summary":

        positive = (
            df["Sentiment"]
            .astype(str)
            .str.lower()
            .eq("positive")
            .sum()
        )

        negative = (
            df["Sentiment"]
            .astype(str)
            .str.lower()
            .eq("negative")
            .sum()
        )

        avg_rating = round(
            df["Rate"].mean(),
            2
        )

        satisfaction = round(
            (positive / len(df)) * 100,
            2
        )

        return f"""
AI BUSINESS INSIGHTS

Total Reviews: {len(df)}

Total Products:
{df['product_name'].nunique()}

Average Rating:
{avg_rating}

Positive Reviews:
{positive}

Negative Reviews:
{negative}

Customer Satisfaction:
{satisfaction}%

Recommendation:
Focus on highly rated products
and investigate recurring
negative reviews.
"""

    # ====================================
    # HELP
    # ====================================

    return """
Try questions like:

• Which products are best?
• Recommend good products
• Most purchased products
• Average rating
• Customer satisfaction
• Search Samsung
• Search iPhone
• Products under 3000
• Products under 5000
• Compare Samsung vs iPhone
• Top complaints
• Positive reviews
• Negative reviews
• Business insights
• Executive summary
"""