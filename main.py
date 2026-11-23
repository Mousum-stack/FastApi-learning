from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import json
from fastapi import HTTPException

app = FastAPI()

from pydantic import BaseModel

class Patient(BaseModel):
    name: Annotated[str, Field(..., description="Patient Name", examples='Raj')]
    age: Annotated[int, Field(..., description="Age should be Greater than 0", gt=0, lt=120)]
    gender: str
    blood_group: str
    medical_condition: str
    date_of_admission: str
    doctor: str
    hospital: str
    insurance_provider: str
    billing_amount: float
    room_number: int
    admission_type: str
    discharge_date: str
    medication: str
    test_results: str

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
def view_patient(medical_condition: str = Path(..., description='Name of the disease in database' , example = ['Cancer'])):

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

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Field to sort by: Age, Billing Amount, or Room Number"),
                  order: str = Query('asc', description = "Either Asc or Desc")):
    valid_fields = ['Age', 'Billing Amount', 'Room Number']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Invaild Field Select From valid Fields')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invaild order select brtween asc and desc')
    
    data = load_data()
    
    sort_order = True if order=='desc' else False
    
    sorted_data = sorted(
    data,
    key=lambda x: x.get(sort_by, 0),
    reverse=sort_order
)
    return sorted_data