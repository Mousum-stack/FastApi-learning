from fastapi import FastAPI, Path
import json
from fastapi import HTTPException

app = FastAPI()

def load_data():
    with open('healthcare_dataset.json', 'r') as f:
        data = json.load(f)
        
    return data

@app.get("/")
def hello():
    return {"message" : "Patient Management Syatem API"}

@app.get("/about")
def about():
    return{"A Fully functional API to manage records"}

@app.get("/view")
def view():
    data = load_data()
    
    return data



@app.get("/patient/{medical_condition}")
def view_patient(medical_condition: str = Path(..., description='Name of the disease in database' , example = 'Cancer')):

    data = load_data()

    filtered_patients = [
        patient for patient in data
        if patient["Medical Condition"].lower() == medical_condition.lower()
    ]

    if not filtered_patients:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return filtered_patients