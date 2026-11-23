from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, computed_field
from datetime import date
from typing import Annotated, Literal
import json
from fastapi import HTTPException

app = FastAPI()

from pydantic import BaseModel

from pydantic import BaseModel, Field
from typing import Annotated, Literal


class Patient(BaseModel):
    
    patient_id: UUID = Field(default_factory=uuid4)

    name: Annotated[
        str,
        Field(..., description="Patient Name", examples=["Raj"])
    ]

    age: Annotated[
        int,
        Field(..., description="Age should be greater than 0 and less than 120", gt=0, lt=120)
    ]

    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender of the patient")
    ]

    blood_group: Annotated[
        Literal["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        Field(..., description="Blood group of the patient")
    ]

    medical_condition: str
    date_of_admission: str
    doctor: str
    hospital: str
    insurance_provider: str

    billing_amount: Annotated[
        float,
        Field(..., description="Patient billing amount", ge=0)
    ]

    room_number: Annotated[
        int,
        Field(..., description="Patient room number", gt=0)
    ]

    admission_type: Literal["Emergency", "Urgent", "Elective"]
    discharge_date: str
    medication: str
    test_results: Literal["Normal", "Abnormal", "Inconclusive"]
    
    @computed_field
    @property
    def hospital_stay_days(self) -> int:
        return (self.discharge_date - self.date_of_admission).days
    
    
    @computed_field
    @property
    def billing_category(self) -> str:
        if self.billing_amount < 2000:
            return "Low"
        elif self.billing_amount <= 40000:
            return "Medium"
        else:
            return "High"

def load_data():
    with open('healthcare_dataset.json', 'r') as f:
        data = json.load(f)
        
    return data

def save_data(data):
    with open("healthcare_dataset.json", "w") as f:
        json.dump(data, f, indent=4)

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

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    #check if the patient already in the database
    # new patient added to the database
    
    data = load_data()
    
    if patient.patient_id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')
    
    #new patient add to the database
    
    data.append(patient.model_dump(mode="json"))
    
    save_data(data)
    
    
    return JSONResponse(status_code=201, content={'message':'patient Created successfully'})