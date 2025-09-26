import pandas as pd
import isodate
from datetime import date
from scripts.extract import fetch_trending_videos
from config.languages import category_codes, youtube_language_codes

def transformation():
    # Load raw data
    Videos = fetch_trending_videos()
    df = pd.DataFrame(Videos)

    print("Transformation Started...")
    # Map categories & languages (with fallback)
    df['genres'] = df['category_id'].astype(str).map(category_codes).fillna("Unknown")
    df['language'] = df['language'].astype(str).map(youtube_language_codes).fillna("Unknown")

    # Convert duration (ISO 8601 → seconds + minutes)
    df['duration'] = df['duration'].apply(lambda x: isodate.parse_duration(x).total_seconds() if pd.notnull(x) else 0)
    df['duration_minutes'] = df['duration'] / 60

    # Convert to datetime and extract parts
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
    df['published_date'] = df['published_at'].dt.date
    df['published_time'] = df['published_at'].dt.time
    df['weekday'] = df['published_at'].dt.day_name()
    df['published_hour'] = df['published_at'].dt.hour

    # Ensure counts are numeric
    df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce').fillna(0).astype(int)
    df['comment_count'] = pd.to_numeric(df['comment_count'], errors='coerce').fillna(0).astype(int)
    df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce').fillna(0).astype(int)

    # Engagement metrics
    df['engagement_count'] = df['like_count'] + df['comment_count']
    df['engagement_rate'] = df['engagement_count'] / df['view_count'].replace(0, 1)

    # Add trending date column
    specific_date = date(2025, 9, 20)
    df['trending_date'] = date.today()  # replce with specific date

    print("Transformation Completed")
    return df
