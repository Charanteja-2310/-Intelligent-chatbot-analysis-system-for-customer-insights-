## Project Structure

* `app.py` — Main Streamlit application
* `modules/chatbot.py` — AI chatbot and query response handling
* `modules/data_loader.py` — Dataset loading and preprocessing
* `modules/nlp_engine.py` — NLP processing and text analysis
* `modules/recommendation_engine.py` — Product recommendation engine
* `modules/reports.py` — Report generation and CSV exports
* `modules/sentiment_analysis.py` — Sentiment analysis using NLP techniques
* `modules/visualizations.py` — Dashboard charts and analytics visualizations
* `dataset/Dataset-SA.csv` — E-Commerce product reviews dataset
* `customer_insights.db` — SQLite database for storing project data
* `requirements.txt` — Required Python libraries

## Dataset Notice

This project uses the following dataset:

* `Dataset-SA.csv`

The dataset contains E-Commerce product reviews used for:

* Sentiment Analysis
* Customer Insights
* Product Recommendations
* Review Analytics

The dataset is not included in this repository due to file size limitations.

To run this project:

1. Obtain the dataset file:

   * `Dataset-SA.csv`

2. Place the file inside the `dataset` folder:

   ```
   dataset/
   └── Dataset-SA.csv
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:

   ```
   streamlit run app.py
   ```

## Features

* Sentiment Analysis using NLP
* Customer Review Analytics
* Product Recommendation Engine
* AI-Powered Query System
* Interactive Dashboard
* Data Visualization
* Export Reports
