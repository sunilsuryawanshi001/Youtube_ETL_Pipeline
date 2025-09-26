import pandas as pd
import os
from sqlalchemy import create_engine, types
from config.secrets import DB_CONFIG
from scripts.transform import transformation


# POSTGRESQL TABLE NAME
TABLE_NAME = "youtube_trendings_india_copy"


# ----------------------------------
# LOAD INTO POSTGRESQL
def load_to_postgres():
    print("Loading data into PostgreSQL...")

    # Load transformed data
    transformed_data = transformation()
    df = pd.DataFrame(transformed_data)

    # Create connection 
    engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db_name']}")

    # Push DataFrame to PostgreSQL with explicit column types
    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="append",  
        index=False,
        dtype={
            "video_id": types.String(50),
            "title": types.Text(),
            "channel_title": types.String(150),
            "published_at": types.DateTime(),
            "published_date": types.Date(),
            "published_time": types.Time(),
            "weekday": types.String(20),
            "published_hour": types.Integer(),
            "view_count": types.BigInteger(),
            "like_count": types.BigInteger(),
            "comment_count": types.BigInteger(),
            "duration": types.Float(),
            "duration_minutes": types.Float(),
            "category_id": types.Integer(),
            "genres": types.String(50),
            "language": types.String(50),
            "engagement_count": types.BigInteger(),
            "engagement_rate": types.Float(),
            "trending_date": types.Date()
        }
    )
    print("Data loaded successfully into PostgreSQL.")
