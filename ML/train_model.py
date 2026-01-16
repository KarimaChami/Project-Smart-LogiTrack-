import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

engine = create_engine("postgresql+psycopg2://taxi:taxi@postgres:5432/taxi_db")

df = pd.read_sql("SELECT * FROM silver_taxi_trips", engine)

target = "duration_minutes"
features = [
    "duration_minutes",
    "pickuphour",
    "dayof_week",
    "month",
    "congestion_surcharge",
    "trip_distance",
    "PULocationID",
    "DOLocationID",
    "cbd_congestion_fee"
]

# X = df[features]
# y = df[target]

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# model = RandomForestRegressor(
#     n_estimators=200,
#     max_depth=None,
#     random_state=42,
#     n_jobs=-1
# )
# model.fit(X_train, y_train)

# y_pred = model.predict(X_test)
# print("MAE:", mean_absolute_error(y_test, y_pred))
# print("R2:", r2_score(y_test, y_pred))

# joblib.dump(model, "/app/model.pkl")
