from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI()

model = joblib.load("models/model.pkl")

readme_path = Path("README.md")

class InputData(BaseModel):
    Residence_city: str
    Socioeconomic_level: int
    Civil_status: str
    Age: int
    State: str
    Province: str
    Vulnerable_group: int
    Desired_program: str
    Family_income: int
    Father_level: str
    Mother_level: str
    STEM_subjects: float
    H_subjects: float
    MIN_subject: float

@app.post("/predict")
def predict(data: InputData):
    input_dict = data.dict()
    df = pd.DataFrame([input_dict])
    prediction = model.predict(df)[0]

    log_entry = (
        f"\n\n###  Napoved\n"
        f"**Vhodni podatki:** `{input_dict}`\n"
        f"**Napovedan razred:** `{prediction}`\n"
    )

    readme_path.write_text(readme_path.read_text() + log_entry, encoding="utf-8")

    return {"prediction": prediction}
