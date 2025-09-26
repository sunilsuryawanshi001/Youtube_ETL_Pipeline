import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config.secrets import DB_CONFIG

# Table name
TABLE_NAME = "youtube_trendings_india"

# ----------------------------------
# Load Data Function
# ----------------------------------
@st.cache_data
def load_data():
    engine = create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db_name']}"
    )
    query = f"SELECT * FROM {TABLE_NAME};"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# ----------------------------------
# Streamlit App
# ----------------------------------
st.title("YouTube Trending Analytics Dashboard")
st.markdown("Explore trending YouTube videos with interactive analytics!")

# Sidebar Filters
st.sidebar.header("Filters")

# Dynamic date filter
available_dates = df['trending_date'].dropna().sort_values(ascending=False).unique()
if len(available_dates) > 0:
    selected_date = st.sidebar.selectbox("Select Trending Date", available_dates)
    filtered_df = df[df['trending_date'] == selected_date]
else:
    st.sidebar.write("No trending data available")
    filtered_df = df.copy()

# Category and Language filters
categories = st.sidebar.multiselect(
    "Select Categories",
    filtered_df['genres'].dropna().unique(),
    default=None
)
languages = st.sidebar.multiselect(
    "Select Languages",
    filtered_df['language'].dropna().unique(),
    default=None
)

if categories:
    filtered_df = filtered_df[filtered_df['genres'].isin(categories)]
if languages:
    filtered_df = filtered_df[filtered_df['language'].isin(languages)]

# Top Trending Videos
st.subheader("Top Trending Videos (by Views)")
top_videos = filtered_df.sort_values(by="view_count", ascending=False)
st.dataframe(top_videos[['title', 'channel_title', 'genres', 'view_count', 'like_count', 'comment_count', 'engagement_rate']])

# Top Creators by Engagement Rate
st.subheader("Top Creators by Engagement Rate")
top_creators = (
    filtered_df.groupby("channel_title")
    .agg({"engagement_rate": "mean", "video_id": "count"})
    .rename(columns={"video_id": "num_videos"})
    .sort_values(by="engagement_rate", ascending=False)
    .head(10)
)
st.bar_chart(top_creators["engagement_rate"])

# Category Trends
st.subheader("Top Categories by Average Views")
category_trends = (
    filtered_df.groupby("genres")
    .agg({"view_count": "mean"})
    .sort_values(by="view_count", ascending=False)
    .head(10)
)
st.bar_chart(category_trends)

# Upload Time Analysis
st.subheader("Best Upload Times (by Views)")
upload_times = (
    filtered_df.groupby("published_hour")
    .agg({"view_count": "mean"})
    .sort_values(by="published_hour")
)
st.line_chart(upload_times)

# Weekday Analysis
st.subheader("Views by Weekday")
weekday_views = (
    filtered_df.groupby("weekday")
    .agg({"view_count": "mean"})
    .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
)
st.bar_chart(weekday_views)

# Language Distribution
st.subheader("Language Distribution of Trending Videos")
lang_dist = filtered_df['language'].value_counts()
st.bar_chart(lang_dist)
