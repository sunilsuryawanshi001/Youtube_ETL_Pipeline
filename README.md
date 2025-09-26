# YouTube Trending ETL Project 📊

## Overview
This project extracts trending YouTube videos using the YouTube API,
transforms the data (engagement metrics, categories, languages),
and loads it into PostgreSQL for analytics.

## Features
- Daily trending extraction
- Engagement rate calculation
- Streamlit dashboard
- PostgreSQL storage

## How to Run
1. Clone repo
2. Create `.env` with DB + API credentials
3. Install requirements: `pip install -r requirements.txt`
4. Run ETL: `python main.py`
5. Launch dashboard: `streamlit run App.py`
