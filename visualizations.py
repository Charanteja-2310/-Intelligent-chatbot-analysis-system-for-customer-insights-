import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# SENTIMENT PIE CHART
# =====================================================

def sentiment_distribution_chart(df):

    sentiment_counts = (
        df["Sentiment"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        "Sentiment",
        "Count"
    ]

    fig = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Customer Sentiment Distribution",
        hole=0.4
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# RATING DISTRIBUTION
# =====================================================

def rating_distribution_chart(df):

    fig = px.histogram(
        df,
        x="Rate",
        nbins=5,
        title="Rating Distribution"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# PRICE VS RATING
# =====================================================

def price_rating_chart(df):

    fig = px.scatter(
        df,
        x="product_price",
        y="Rate",
        color="Sentiment",
        hover_data=["product_name"],
        title="Price vs Rating Analysis"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# TOP PRODUCTS CHART
# =====================================================

def top_products_chart(top_products):

    fig = px.bar(
        top_products,
        x="Average_Rating",
        y="product_name",
        orientation="h",
        title="Top Recommended Products"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# WORST PRODUCTS CHART
# =====================================================

def worst_products_chart(worst_products):

    fig = px.bar(
        worst_products,
        x="Average_Rating",
        y="product_name",
        orientation="h",
        title="Worst Rated Products"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# MOST REVIEWED PRODUCTS
# =====================================================

def most_reviewed_chart(reviewed_products):

    fig = px.bar(
        reviewed_products,
        x="Total_Reviews",
        y="product_name",
        orientation="h",
        title="Most Reviewed Products"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# REVIEW LENGTH ANALYSIS
# =====================================================

def review_length_chart(df):

    fig = px.histogram(
        df,
        x="Review_Length",
        nbins=50,
        title="Review Length Analysis"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# POLARITY DISTRIBUTION
# =====================================================

def polarity_chart(df):

    fig = px.histogram(
        df,
        x="Polarity",
        nbins=50,
        title="Review Polarity Distribution"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# SUBJECTIVITY DISTRIBUTION
# =====================================================

def subjectivity_chart(df):

    fig = px.histogram(
        df,
        x="Subjectivity",
        nbins=50,
        title="Review Subjectivity Distribution"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# PRODUCT PRICE DISTRIBUTION
# =====================================================

def price_distribution_chart(df):

    fig = px.histogram(
        df,
        x="product_price",
        nbins=50,
        title="Product Price Distribution"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# SENTIMENT VS RATING
# =====================================================

def sentiment_rating_chart(df):

    avg_rating = (
        df.groupby("Sentiment")
        ["Rate"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        avg_rating,
        x="Sentiment",
        y="Rate",
        title="Average Rating by Sentiment"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# =====================================================
# DASHBOARD GAUGE
# =====================================================

def satisfaction_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={
                "text":
                "Customer Satisfaction Score"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                }
            }
        )
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig