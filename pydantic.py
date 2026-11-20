from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('Inserted into database')

patient = Patient(name='Nitish', age=30)

insert_patient_data(patient)