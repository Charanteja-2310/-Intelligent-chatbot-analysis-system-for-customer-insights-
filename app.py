import streamlit as st
import pandas as pd

from modules.data_loader import load_data
from modules.sentiment_analysis import apply_sentiment_analysis
from modules.recommendation_engine import (
    get_top_products,
    get_worst_products,
    get_most_reviewed_products,
    get_best_value_products,
    recommend_under_budget
)
from modules.chatbot import chatbot_response
from modules.visualizations import (
    sentiment_distribution_chart,
    rating_distribution_chart,
    price_rating_chart,
    top_products_chart,
    worst_products_chart,
    most_reviewed_chart,
    review_length_chart,
    polarity_chart,
    subjectivity_chart,
    price_distribution_chart,
    sentiment_rating_chart,
    satisfaction_gauge
)
from modules.reports import export_csv

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI-Powered E-Commerce Product Review Intelligence & Recommendation System",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 Intelligent Chatbot Analysis System for Customer Insights using Data Analytics and AI"
)

# =====================================================
# LOAD & PROCESS DATA
# =====================================================

@st.cache_data
def get_processed_data():
    df = load_data()
    df = apply_sentiment_analysis(df)
    return df

df = get_processed_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

products = ["All Products"] + sorted(df["product_name"].astype(str).unique().tolist())
selected_product = st.sidebar.selectbox("Select Product", products)

if selected_product != "All Products":
    df = df[df["product_name"] == selected_product]

rating_filter = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 1.0)
df = df[df["Rate"] >= rating_filter]

# =====================================================
# METRICS
# =====================================================

total_reviews = len(df)
positive     = int((df["Sentiment"].astype(str).str.lower() == "positive").sum())
negative     = int((df["Sentiment"].astype(str).str.lower() == "negative").sum())
neutral      = int((df["Sentiment"].astype(str).str.lower() == "neutral").sum())
avg_rating   = round(df["Rate"].mean(), 2) if len(df) else 0
satisfaction = round((positive / total_reviews) * 100, 2) if total_reviews else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Reviews",    total_reviews)
c2.metric("Positive",   positive)
c3.metric("Negative",   negative)
c4.metric("Neutral",    neutral)
c5.metric("Avg Rating", avg_rating)

st.plotly_chart(satisfaction_gauge(satisfaction), use_container_width=True)

# =====================================================
# TABS
# =====================================================

tabs = st.tabs([
    "Dashboard",
    "Recommendations",
    "Analytics",
    "Chatbot",
    "Exports"
])

# =====================================================
# TAB 0 — DASHBOARD
# =====================================================

with tabs[0]:

    st.subheader("Dashboard Overview")

    st.plotly_chart(sentiment_distribution_chart(df), use_container_width=True)
    st.plotly_chart(rating_distribution_chart(df),    use_container_width=True)

    if "product_price" in df.columns:
        st.plotly_chart(price_rating_chart(df), use_container_width=True)

# =====================================================
# TAB 1 — RECOMMENDATIONS
# =====================================================

with tabs[1]:

    st.subheader("Recommendation Engine")

    top_products      = get_top_products(df, 10)
    worst_products    = get_worst_products(df, 10)
    reviewed_products = get_most_reviewed_products(df, 10)
    value_products    = get_best_value_products(df, 10)

    st.plotly_chart(top_products_chart(top_products),       use_container_width=True)
    st.dataframe(top_products,                              use_container_width=True)

    st.plotly_chart(worst_products_chart(worst_products),   use_container_width=True)
    st.dataframe(worst_products,                            use_container_width=True)

    st.plotly_chart(most_reviewed_chart(reviewed_products), use_container_width=True)
    st.dataframe(reviewed_products,                         use_container_width=True)

    st.subheader("Best Value Products")
    st.dataframe(value_products, use_container_width=True)

    budget = st.number_input("Budget Recommendation", min_value=100, value=5000)
    st.dataframe(recommend_under_budget(df, budget), use_container_width=True)

# =====================================================
# TAB 2 — ANALYTICS
# =====================================================

with tabs[2]:

    st.subheader("Advanced Analytics")

    st.plotly_chart(review_length_chart(df),     use_container_width=True)
    st.plotly_chart(polarity_chart(df),          use_container_width=True)
    st.plotly_chart(subjectivity_chart(df),      use_container_width=True)
    st.plotly_chart(price_distribution_chart(df),use_container_width=True)
    st.plotly_chart(sentiment_rating_chart(df),  use_container_width=True)

# =====================================================
# TAB 3 — CHATBOT
# =====================================================

with tabs[3]:

    st.subheader("🤖 AI Product Review Intelligence Assistant")
    st.subheader("💬 Custom NLP Query")

    suggested_queries = [
        "Which products are best?",
        "Recommend good products",
        "Most purchased products",
        "Average rating",
        "Customer satisfaction",
        "Positive reviews",
        "Negative reviews",
        "Products under 3000",
        "Products under 5000",
        "Search Samsung",
        "Search iPhone",
        "Business insights",
        "Dataset summary"
    ]

    query = st.selectbox(
        "Ask your own question",
        suggested_queries,
        key="chatbot_query"
    )

    if st.button(
        "Submit Query",
        key="chatbot_submit"
    ):

        result = chatbot_response(
            query,
            df
        )

        if isinstance(result, pd.DataFrame):

            st.dataframe(
                result,
                use_container_width=True
            )

        elif isinstance(result, pd.Series):

            st.dataframe(
                result.reset_index(),
                use_container_width=True
            )

        else:

            st.info(
                str(result)
            )

# =====================================================
# TAB 4 — EXPORTS
# =====================================================

with tabs[4]:

    st.subheader("Exports")

    csv_data = export_csv(df)

    st.download_button(
        "Download CSV Report",
        csv_data,
        "analytics_report.csv",
        "text/csv"
    )

    st.success("Report ready for download")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.success("✅ Professional Product Review Intelligence System Running Successfully")
