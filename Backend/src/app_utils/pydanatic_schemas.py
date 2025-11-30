from src.app_utils.fast_api_header import BaseModel


# -----------------signup schema  --------------------------
class Course(BaseModel):
    course_name : str 
    teacher_name: str
    class_name: str
    password: str


#  -----------------------login schema ---------------------------

class LoginDetails(BaseModel):
    teacher_name: str
    course_name: str
    password: str