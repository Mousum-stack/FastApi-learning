from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Annotated, Dict, Optional

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient less than 50 characters', example=['Nitish', 'Amit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    height: Annotated[float, Field(gt=0, strict=True)]
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=False, description='Is the patient married or not')]
    alergies: Optional[List[str]] = None
    contact_details: Dict[str, str]
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    
    @field_validator('age', mode= 'after')
    @classmethod
    def validate_age(cls,value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age should be in between 0 and 100")
        
        
    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patient older than 60 must have an emergency contact")
        return model
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    
    
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.alergies)
    print(patient.email)
    print('BMI', patient.bmi)
    print('Inserted into database')

patient = Patient(name='Rahul', email='raj123@icici.com', linkedin_url='https://linkedin.com/1322', age='80',height=1.72, weight=80, married=True, alergies=['pollen', 'dust', 'cinus'], contact_details={'email': 'akku123@gmail.com', 'phn': '1234567891', 'emergency':'123455'})

insert_patient_data(patient)