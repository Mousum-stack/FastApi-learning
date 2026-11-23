from fastapi import FastAPI, Path, HTTPException, Query
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
    date_of_admission: date
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
    discharge_date: date
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


def add_patient_ids():

    data = load_data()

    for patient in data:
        if "patient_id" not in patient:
            patient["patient_id"] = str(uuid4())

    save_data(data)

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
def view_patient(medical_condition: str = Path(..., description='Name of the disease in database' , examples = ['Cancer'])):

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

@app.post("/create", status_code=201)
def create_patient(patient: Patient):

    data = load_data()

    # Check whether patient ID already exists
    if any(
        existing_patient.get("patient_id") == str(patient.patient_id)
        for existing_patient in data
    ):
        raise HTTPException(
            status_code=409,
            detail="Patient ID already exists"
        )

    # Add new patient
    new_patient = patient.model_dump(mode="json")
    data.append(new_patient)

    # Save updated data
    save_data(data)

    return {
        "message": "Patient created successfully",
        "patient": new_patient
    }