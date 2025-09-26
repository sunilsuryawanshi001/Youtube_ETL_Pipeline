from scripts.extract import extract_data, fetch_trending_videos
from scripts.transform import transformation
from scripts.load_to_pgsql import load_to_postgres

if __name__=="__main__":
   fetch_trending_videos()     # Extract data from api
   extract_data()              # Save raw data to local csv or json
   transformation()            # Treansforn raw data into usuful insights
   load_to_postgres()          # Load transformed data into postgresql
