from textblob import TextBlob
import pandas as pd


def get_polarity(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0


def get_subjectivity(text):
    try:
        return TextBlob(str(text)).sentiment.subjectivity
    except:
        return 0


def get_sentiment_label(polarity):

    if polarity > 0.1:
        return "Positive"

    elif polarity < -0.1:
        return "Negative"

    else:
        return "Neutral"


def apply_sentiment_analysis(df):

    review_column = "Summary"

    if review_column not in df.columns:

        if "Review" in df.columns:
            review_column = "Review"

        else:
            review_column = df.columns[0]

    df["Polarity"] = (
        df[review_column]
        .astype(str)
        .apply(get_polarity)
    )

    df["Subjectivity"] = (
        df[review_column]
        .astype(str)
        .apply(get_subjectivity)
    )

    df["Sentiment"] = (
        df["Polarity"]
        .apply(get_sentiment_label)
    )

    return df


def sentiment_summary(df):

    positive = int(
        (df["Sentiment"] == "Positive").sum()
    )

    negative = int(
        (df["Sentiment"] == "Negative").sum()
    )

    neutral = int(
        (df["Sentiment"] == "Neutral").sum()
    )

    return {
        "total_reviews": len(df),
        "positive_reviews": positive,
        "negative_reviews": negative,
        "neutral_reviews": neutral
    }