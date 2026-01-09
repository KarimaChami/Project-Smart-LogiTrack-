import pandas as pd
from sqlalchemy import create_engine

silver_df = pd.read_parquet(
    "data/silver_taxi_data",
    engine="pyarrow",
    columns=[  
        "duration_minutes",
        "pickuphour",
        "dayof_week",
        "month",
        "congestion_surcharge",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "trip_distance",
        "PULocationID",
        "DOLocationID",
        "cbd_congestion_fee",
        "total_amount"
    ]
)

print(silver_df.head())
print(silver_df.shape)

engine = create_engine(
    "postgresql+psycopg2://postgres:root1234@localhost:5432/taxi_db"
)

silver_df.to_sql(
    name="silver_taxi_data",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000
)