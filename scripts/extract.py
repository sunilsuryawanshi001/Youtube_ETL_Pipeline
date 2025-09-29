import requests
import pandas as pd
import os
import json
from config.secrets import API_KEY
from datetime import datetime

# Configuration
REGION_CODE = "IN"
MAX_RESULTS = 50
TOTAL_RESULTS = 200

# Extract From YouTube Data v3 API
def fetch_trending_videos():
    all_videos = []
    url = "https://www.googleapis.com/youtube/v3/videos"
    next_page_token = None
    fetched = 0

    while fetched < TOTAL_RESULTS:
        results_to_fetch = min(MAX_RESULTS, TOTAL_RESULTS - fetched)
        params = {
            'part': 'snippet,statistics,contentDetails',
            'chart': 'mostPopular',
            'regionCode': REGION_CODE,
            'maxResults': results_to_fetch,
            'pageToken': next_page_token,
            'key': API_KEY
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.text}")
            break

        data = response.json()
        for item in data.get('items', []):
            video = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'channel_title': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'duration': item['contentDetails']['duration'],
                'category_id': item['snippet']['categoryId'],
                'language': item['snippet'].get('defaultAudioLanguage', 'unknown')
            }
            all_videos.append(video)

        fetched += len(data.get('items', []))
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return all_videos


def extract_data():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print("Fetching data from YouTube API...")

    videos = fetch_trending_videos()
    data = pd.DataFrame(videos)

    if not data.empty:
        # Ensure output folder exists
        output_dir = r"youtube_etl_pipeline\data\raw"
        os.makedirs(output_dir, exist_ok=True)

        # File paths
        csv_file = os.path.join(output_dir, f"yt_trendings_{timestamp}.csv")
        json_file = os.path.join(output_dir, f"yt_trendings_{timestamp}.json")

        # Save as CSV
        data.to_csv(csv_file, index=False, encoding="utf-8")

        # Save as JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(videos, f, indent=4, ensure_ascii=False)

        print(f"Data saved to CSV: {csv_file}")
        print(f"Data saved to JSON: {json_file}")
    else:
        print("No data fetched.")

