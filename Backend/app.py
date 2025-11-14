from fastapi import FastAPI
from src.DataBase.pymong import Class_Embeddings , Course_info
from src.components.gettingresults import GettingResults, GettingResults_for_image 
from pydantic import BaseModel
import requests
from fastapi import UploadFile, File , Form
import torch
import json
import os
import pandas as pd


app = FastAPI()

class Course(BaseModel):
    course_name: str
    teacher_name: str
    class_name: str
    password: str
# DataBases

class LoginDetails(BaseModel):
    teacher_name: str
    course_name: str
    password: str

@app.post('/Create_New_Course')
def create_new_course(course: Course):
    Course_content = course.dict()
    print(Course_content.keys(), type(Course_content))
    course_name = Course_content['course_name']
    # get the course details from the Courses_Details database
    course_name_details = Course_info.find_one({'course_name': course_name , 'teacher_name': Course_content['teacher_name'], 'class_name': Course_content['class_name']})
    if course_name_details:
        return {'status': 'failed', 'message': 'Course already exists'}
    class_embeddings_id = Class_Embeddings.find_one({'class_name': Course_content['class_name']})
    if not class_embeddings_id:
        return {'status': 'failed', 'message': 'Wrong Class Name'}
    else:
        class_embeddings_id = class_embeddings_id['_id']
    Course_content['class_name'] = class_embeddings_id
    Course=Course_info.insert_one(Course_content)

    return {'status': 'success', 'message': 'Course created successfully' , "data":{'Course_id': str(Course.inserted_id), 'Class_Embeddings_id': str(class_embeddings_id)}}   


@app.post('/login_existing_course')
def login_existing_course(course: LoginDetails):
    course_content = course.dict()
    course_name = course_content['course_name']
    teacher_name = course_content['teacher_name']
    password = course_content['password']
    course_details = Course_info.find_one({'course_name': course_name, 'teacher_name': teacher_name, 'password': password})
    if not course_details:
        return {'status': 'failed', 'message': 'Invalid credentials'}
    return {'status': 'success', 'message': 'Login successful', 'data': {'Course_id': str(course_details['_id']), 'Class_Embeddings_id': str(course_details['class_name'])}}


import os
# Data 
@app.post('/attendance_data/{course_id}')
async def attendance_data(course_id: str, file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    
    # Save video in chunks (safe for large files)
    with open(file_path, "wb") as f:
        while chunk := await file.read(1024*1024):
            f.write(chunk)

    device_to_use = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    getting_results = GettingResults(file_path, course_id, device_to_use)
    results = getting_results.get_results()
    os.remove(file_path)
    df = pd.DataFrame()
    df['Names']=[k.keys() for k in results]
    df['Accuracy']= [k.values() for k in results]
    df.to_csv(f'uploads/attendance_{course_id}.csv', index=False)

    return {"filename": file.filename, "content_type": file.content_type, "results": results    }


@app.post('/attendance_image/{course_id}')

def get_attendance_from_image(course_id: str, file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        file_content = file.file.read()
        f.write(file_content)
    image_path = file_path
    device_to_use = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    getting_results = GettingResults_for_image(image_path, course_id, device_to_use)
    results = getting_results.get_results()
    os.remove(file_path)
    df = pd.DataFrame()
    df['Names']=results.keys()
    df['Accuracy']=results.values()
    df.to_csv(f'uploads/attendance_{course_id}.csv', index=False)
    return {"filename": file.filename, "content_type": file.content_type, "results": results}




