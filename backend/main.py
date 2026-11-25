from fastapi import FastAPI
from pathlib import Path
import joblib
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
import sqlite3

# Load the artifacts 

BASE_DIR = Path(__file__).resolve().parent.parent

ARTIFACT_PATH = BASE_DIR / "mobile_addiction_artifacts.pkl"

artifacts = joblib.load(ARTIFACT_PATH)

model = artifacts["model"]
scaler = artifacts["scaler"]
feature_names = artifacts["feature_names"]
clip_values = artifacts.get("clip_values", {})

print("Saved artifact keys:", artifacts.keys())
print("Clip values:", clip_values)

#backend wants to know,what are coming in the request body, so we define a pydantic model for that  


class MobileWellInput(BaseModel):

    age: int = Field(ge=1)

    daily_screen_time_hours: float = Field(ge=0)
    social_media_hours: float = Field(ge=0)
    gaming_hours: float = Field(ge=0)
    work_study_hours: float = Field(ge=0)
    sleep_hours: float = Field(ge=0)

    notifications_per_day: int = Field(ge=0)
    app_opens_per_day: int = Field(ge=0)

    weekend_screen_time: float = Field(ge=0)

    gender: Literal["Female", "Male", "Other"]

    stress_level: Literal["Low", "Medium", "High"]

    academic_work_impact: Literal["Yes", "No"]

app = FastAPI()
# Database setup
DB_PATH = BASE_DIR / "mobilewell.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            daily_screen_time_hours REAL,
            social_media_hours REAL,
            gaming_hours REAL,
            work_study_hours REAL,
            sleep_hours REAL,
            notifications_per_day INTEGER,
            app_opens_per_day INTEGER,
            weekend_screen_time REAL,
            stress_level TEXT,
            academic_work_impact TEXT,
            prediction INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

create_database()

@app.get("/")
def home():
    return {"message": "Welcome to MobileWell Backend!"}


@app.post("/predict")
def predict(data: MobileWellInput):

    input_data = data.model_dump()

    gender = input_data.pop("gender")
    stress = input_data.pop("stress_level")
    academic = input_data.pop("academic_work_impact")

    input_data["gender_Male"] = 1 if gender == "Male" else 0
    input_data["gender_Other"] = 1 if gender == "Other" else 0

    input_data["stress_level_Low"] = 1 if stress == "Low" else 0
    input_data["stress_level_Medium"] = 1 if stress == "Medium" else 0

    input_data["academic_work_impact_Yes"] = 1 if academic == "Yes" else 0

    input_df = pd.DataFrame([input_data])

    input_df = input_df[feature_names]
    for column, rules in clip_values.items():

        if input_df[column].iloc[0] > rules["limit"]:
           input_df[column] = rules["replacement"]
        
    scaled_data = scaler.transform(input_df)
    prediction = model.predict(scaled_data)
    
    result = int(prediction[0])
    status = "Addicted" if result == 1 else "Not Addicted"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            age, gender, daily_screen_time_hours, social_media_hours,
            gaming_hours, work_study_hours, sleep_hours,
            notifications_per_day, app_opens_per_day,
            weekend_screen_time, stress_level, academic_work_impact,
            prediction, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
       data.age,
       gender,
       data.daily_screen_time_hours,
       data.social_media_hours,
       data.gaming_hours,
       data.work_study_hours,
       data.sleep_hours,
       data.notifications_per_day,
       data.app_opens_per_day,
       data.weekend_screen_time,
       stress,
       academic,
       result,
       status
    ))

    conn.commit()
    conn.close()

    return {"prediction": result, "status": status}




@app.get("/history")
def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM predictions
        ORDER BY created_at DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return [dict(record) for record in records]    