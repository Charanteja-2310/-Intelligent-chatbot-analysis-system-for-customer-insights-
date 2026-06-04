import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import colors


# =====================================================
# CSV EXPORT
# =====================================================

def export_csv(df):

    return df.to_csv(
        index=False
    )


# =====================================================
# PDF REPORT GENERATOR
# =====================================================

def generate_pdf_report(df):

    file_name = (
        "Product_Analytics_Report.pdf"
    )

    pdf = SimpleDocTemplate(
        file_name
    )

    styles = (
        getSampleStyleSheet()
    )

    content = []

    # =================================================
    # TITLE
    # =================================================

    content.append(
        Paragraph(
            "AI-Powered E-Commerce Product Review Intelligence & Recommendation System",
            styles["Title"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    # =================================================
    # SUMMARY
    # =================================================

    total_reviews = len(df)

    positive_reviews = int(
        (
            df["Sentiment"]
            .astype(str)
            .str.lower()
            .eq("positive")
        ).sum()
    )

    negative_reviews = int(
        (
            df["Sentiment"]
            .astype(str)
            .str.lower()
            .eq("negative")
        ).sum()
    )

    neutral_reviews = int(
        (
            df["Sentiment"]
            .astype(str)
            .str.lower()
            .eq("neutral")
        ).sum()
    )

    avg_rating = round(
        df["Rate"].mean(),
        2
    )

    total_products = (
        df["product_name"]
        .nunique()
    )

    summary_text = f"""

    <b>Project Summary</b><br/><br/>

    Total Reviews: {total_reviews}<br/>
    Total Products: {total_products}<br/>
    Average Rating: {avg_rating}<br/>
    Positive Reviews: {positive_reviews}<br/>
    Negative Reviews: {negative_reviews}<br/>
    Neutral Reviews: {neutral_reviews}<br/>

    """

    content.append(
        Paragraph(
            summary_text,
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    # =================================================
    # CUSTOMER INSIGHTS
    # =================================================

    content.append(
        Paragraph(
            "Customer Insights",
            styles["Heading1"]
        )
    )

    satisfaction_score = round(
        (
            positive_reviews
            /
            total_reviews
        ) * 100,
        2
    )

    insight_text = f"""

    Customer Satisfaction Score:
    {satisfaction_score}%<br/><br/>

    Most customers expressed positive sentiment
    towards products available on the platform.
    Negative reviews indicate potential
    opportunities for quality improvements
    and customer service enhancement.

    """

    content.append(
        Paragraph(
            insight_text,
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    # =================================================
    # TOP PRODUCTS
    # =================================================

    content.append(
        Paragraph(
            "Top Rated Products",
            styles["Heading1"]
        )
    )

    top_products = (
        df.groupby("product_name")
        ["Rate"]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    for product, rating in top_products.items():

        content.append(
            Paragraph(
                f"{product} : {round(rating,2)} ⭐",
                styles["BodyText"]
            )
        )

    content.append(
        PageBreak()
    )

    # =================================================
    # AI RECOMMENDATIONS
    # =================================================

    content.append(
        Paragraph(
            "AI Recommendations",
            styles["Heading1"]
        )
    )

    recommendation_text = """

    • Focus marketing efforts on highly rated products.<br/>
    • Analyze negative reviews to identify product issues.<br/>
    • Improve product quality for low-rated products.<br/>
    • Promote products with high ratings and review volume.<br/>
    • Continuously monitor customer sentiment trends.<br/>

    """

    content.append(
        Paragraph(
            recommendation_text,
            styles["BodyText"]
        )
    )

    # =================================================
    # BUILD PDF
    # =================================================

    pdf.build(
        content
    )

    return file_name