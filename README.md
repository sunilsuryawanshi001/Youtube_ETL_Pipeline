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
1. Install requirements: `pip install -r requirements.txt`
2. Run ETL: `python main.py`
3. Launch dashboard: `streamlit run App.py`
