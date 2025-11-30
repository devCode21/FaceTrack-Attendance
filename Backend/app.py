
from src.app_utils.fast_api_header import app ,UploadFile ,File
from src.app_utils.pydanatic_schemas import Course ,LoginDetails
from src.app_utils.user import create_new_course ,login_existing_course
from src.app_utils.result import get_attendance_from_image ,attendance_data ,get_csv_file


@app.post('/Create_New_Course')
def signnup_user(course:Course):
    return  create_new_course(course)


@app.post('/login_existing_course')
def login_user(login_details:LoginDetails):
    return login_existing_course(login_details)


@app.post('/attendance_data/{course_id}')
async def get_res_from_video(course_id:str , file :UploadFile= File(...)):
    return await attendance_data(course_id, file)




@app.post('/attendance_image/{course_id}')
def get_res_from_image(course_id:str , file:UploadFile=File(...)):
    return get_attendance_from_image(course_id, file)

@app.get('/csv_file/{course_id}')
def download_csv(course_id: str):
    return get_csv_file(course_id)







