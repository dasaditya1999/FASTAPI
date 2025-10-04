from fastapi import FastAPI, HTTPException, Query
import json
import pandas as pd
from DataValidation import DataValidation, DataValidationOptional
import random

app = FastAPI()

def load_patientData():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open("patients.json", 'w') as file:
            json.dump(data, file)

def generate_pid():
    return "P"+str(random.randint(100,999))

@app.get('/')
def landing_page():
    return {"hey user":"What is your thought?"}

@app.get("/aboutus")
def aboutCompany():
    return {"Hello":"we are a start up focused on building tiny computers!"}

@app.get("/displaypatients")
def display():
    return load_patientData()

@app.get("/patient/{id}")
def viewPatient(id):
    data = load_patientData()

    if id in data.keys():
        return data[id]
    
    raise HTTPException(status_code=404, detail="Not Found")

@app.get('/sort')
def sort(column:str = Query(..., description='column name only'), how:str=Query('asc', description='asc or dsc')):
    try:
        data = load_patientData()
        if column in ['bmi', 'age', 'height', 'weight']:
            if how == 'asc':
                sorted_data = dict(sorted(data.items(), key=lambda item: item[1][column]))
            elif how == 'dsc':
                sorted_data = dict(sorted(data.items(), reverse=True, key=lambda item: item[1][column]))
            else:
                raise HTTPException(status_code=404, detail='Not a valid ordering value!')
        else:
            raise HTTPException(status_code=404, detail='Not a valid column to do sort operation!')
        
        return sorted_data
    
    except:
        raise HTTPException(status_code=404, detail='something is not right')
    
@app.post('/addPatient')
def addPatient(payload:DataValidation):
    data = load_patientData()
    json_data = payload.model_dump()

    name=json_data["name"]
    age=json_data["age"]
    city=json_data["city"]
    for key, value in data.items():
        if value['city'] == city and value['age']==age and value['name']==name:
            print(value)
            raise HTTPException(status_code=403, detail="This patient already exist")
    pid = generate_pid()
    data[pid]=json_data
    save_data(data)
    
    return {"message": f'Data Added Successfully with Patient ID : {pid}'}
    
@app.put('/updateDetails')
def updateDetails(payload:DataValidationOptional):
    '''
    1. Check if the given customer already exist or not.
    2. If no, raise exception
    3. if yes, pull the data point/that customer key-values
    4. update the key which patient wants to update
    5. update the database
    '''
    data = load_patientData()
    json_payload = payload.model_dump(exclude_unset=True)
    p_id = json_payload["p_id"]

    if p_id in data.keys():
        for key, value in json_payload.items():
            if key != 'p_id':
                data[p_id][key] = value
        
        with open('patients.json', 'w') as file:
            json.dump(data, file)

        return {"Patient data updated successfuly":"200, OK"}
    else:
        raise HTTPException(status_code=404, detail="Patient does not exists. 404, Not Found")

@app.delete("/deleteEntry/{p_id}")
def deleteEntry(p_id):
    data = load_patientData()
    print(data)
    if p_id not in data.keys():
        raise HTTPException(status_code=404, detail="404, Patient Not Found")
    else:
        del data[p_id]
        with open('patients.json', 'w') as file:
            json.dump(data, file)
        return f"Patient with {p_id} deleted succesfully. 200, Ok."
