from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql import Row
from sqlalchemy import text
from datetime import datetime
from fastapi import Depends
from auth import get_current_user
from db import engine


# 1. Spark session
spark = SparkSession.builder.appName("TaxiPredictionAPI").getOrCreate()

# 2. Charger le modèle
model = PipelineModel.load("../models/taxi_duration_model")
MODEL_VERSION = "1.0.0"
# 3. FastAPI app
app = FastAPI()

# 4. Schéma des données d'entrée
class TaxiTrip(BaseModel):
    pickuphour: int
    dayof_week: int
    month: int
    trip_distance: float
    PULocationID: int
    DOLocationID: int
    congestion_surcharge: float
    cbd_congestion_fee: float

# 5. Endpoint de prédiction
@app.post("/predict")
# def predict_eta(payload: dict, user=Depends(get_current_user)):
def predict_eta(payload: dict):


    spark_df = spark.createDataFrame([Row(**payload)])
    prediction = model.transform(spark_df).collect()[0]["prediction"]

    # Logging en DB
    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO eta_predictions
            (prediction, model_version, created_at)
            VALUES (:pred, :version, :ts)
            """),
            {
                "pred": float(prediction),
                "version": MODEL_VERSION,
                "ts": datetime.utcnow()
            }
        )

    return {
        "estimated_duration": round(prediction, 2)
    }



# @app.get("/analytics/avg-duration-by-hour")
# def avg_duration_by_hour(user=Depends(get_current_user)):
#     query = text("""
#         WITH hourly_stats AS (
#             SELECT
#                 pickuphour,
#                 AVG(duration_minutes) AS avgduration
#             FROM silver_taxi_data
#             GROUP BY pickuphour
#         )
#         SELECT * FROM hourly_stats
#         ORDER BY pickuphour
#     """)

#     with engine.connect() as conn:
#         result = conn.execute(query)
#         rows = result.fetchall()

#     return [
#         {
#             "pickuphour": row.pickuphour,
#             "avgduration": round(row.avgduration, 2)
#         }
#         for row in rows
#     ]

# @app.get("/analytics/payment-analysis")
# def payment_analysis(user=Depends(get_current_user)):
#     query = text("""
#         SELECT
#             payment_type,
#             COUNT(*) AS total_trips,
#             AVG(duration_minutes) AS avg_duration
#         FROM silver_taxi_data
#         GROUP BY payment_type
#         ORDER BY total_trips DESC
#     """)

#     with engine.connect() as conn:
#         result = conn.execute(query)
#         rows = result.fetchall()

#     return [
#         {
#             "payment_type": row.payment_type,
#             "total_trips": row.total_trips,
#             "avg_duration": round(row.avg_duration, 2)
#         }
#         for row in rows
#     ]