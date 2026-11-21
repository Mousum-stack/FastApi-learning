from pydantic import BaseModel
from typing import List
from typing import Dict
from typing import Optional

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: bool = False
    alergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.alergies)
    print('Inserted into database')

patient = Patient(name='Rahul', age='20',weight=80, married=True, alergies= ['pollen', 'dust', 'cinus'], contact_details= {'email':'akku123@gmail.com', 'phn':'1234567891'})

insert_patient_data(patient)

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.alergies)
    print('Updated into database')

patient = Patient(name='Rahul', age='20',weight=80, married=True, alergies= ['pollen', 'dust', 'cinus'], contact_details= {'email':'akku123@gmail.com', 'phn':'1234567891'})

update_patient_data(patient)



        