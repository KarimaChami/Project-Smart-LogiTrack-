import os
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import joblib
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql import Row
from sqlalchemy import text
from datetime import datetime
from fastapi import Depends
from api.auth import authenticate_user, authenticate_user, create_access_token, get_current_user
from sqlalchemy import create_engine
import pandas as pd



DATABASE_URL = "postgresql+psycopg2://silver_user:root123@localhost:5432/silver_db"
engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 1. Spark session
spark = SparkSession.builder.appName("Taxi_api").getOrCreate()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR,"..","models","taxi_duration_model"))
print("MODEL_PATH =", MODEL_PATH)  # debug once

# # 2. Charger le modèle
model = PipelineModel.load(MODEL_PATH)
MODEL_VERSION = "1.0.0"

# 3. FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message":"salam"}
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
    total_amount: float



@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# 5. Endpoint de prédiction
@app.post("/predict")
def predict_eta(payload: TaxiTrip, user=Depends(get_current_user)):

    pdf = pd.DataFrame([payload.dict()])
    sdf = spark.createDataFrame(pdf)
    # Prediction
    pred_df = model.transform(sdf)
    prediction = pred_df.select("prediction").collect()[0]["prediction"]
    # Logging en DB
    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO silver.eta_predictions
            (prediction, model_version, created_at)
            VALUES (:pred, :version, :ts)
            """),
            {
                "pred": float(prediction),
                "version": MODEL_VERSION,
                "ts": datetime.utcnow()
            }
        )
    return {"estimated_duration": round(float(prediction), 2)}



@app.get("/analytics/avg-duration-by-hour")
def avg_duration_by_hour(user=Depends(get_current_user)):
    query = text("""
        SELECT
            pickuphour,
            AVG(duration_minutes) AS avgduration
        FROM silver.silver_taxi_data
        GROUP BY pickuphour
        ORDER BY pickuphour
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    return [
        {
            "pickuphour": row.pickuphour,
            "avgduration": round(row.avgduration, 2)
        }
        for row in rows
    ]

@app.get("/analytics/payment-analysis")
def payment_analysis(user=Depends(get_current_user)):
    query = text("""
        SELECT
            payment_type,
            COUNT(*) AS total_trips,
            AVG(duration_minutes) AS avg_duration
        FROM silver.silver_taxi_data
        GROUP BY payment_type
        ORDER BY total_trips DESC
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    return [
        {
            "payment_type": row.payment_type,
            "total_trips": row.total_trips,
            "avg_duration": round(row.avg_duration, 2)
        }
        for row in rows
    ]
