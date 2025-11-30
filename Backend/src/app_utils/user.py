

from src.app_utils.fast_api_header import Course_info, Class_Embeddings
from src.app_utils.pydanatic_schemas import Course,LoginDetails
from src.app_utils.Api_resposne import ErrorResponse ,API_respone


# ---------- create the course and signup the user  --------------------------
def create_new_course(course: Course):
    Course_content = course.dict()
    if 'course_name' not in Course_content or 'teacher_name' not in Course_content or 'class_name' not in Course_content or 'password' not in Course_content:
        return  ErrorResponse(404 , "Course Name not found " ).send()
    print(Course_content.keys(), type(Course_content))
    course_name = Course_content['course_name']
    # get the course details from the Courses_Details database
    course_name_details = Course_info.find_one({'course_name': course_name , 'teacher_name': Course_content['teacher_name'], 'class_name': Course_content['class_name']})
    if course_name_details:
        return ErrorResponse(400 , "Course Name already exist  " ).send()
    class_embeddings_id = Class_Embeddings.find_one({'class_name': Course_content['class_name']})
    if not class_embeddings_id:
        return ErrorResponse(400 , "wrong class name  " ).send()
    else:
        class_embeddings_id = class_embeddings_id['_id']
    Course_content['class_name'] = class_embeddings_id
    Course=Course_info.insert_one(Course_content)

    return API_respone(200 , "Create succesfully " ,{'Course_id': str(Course.inserted_id), 'Class_Embeddings_id': str(class_embeddings_id)}  ).api_respone()



# ---------login the user ----------------------------------------

def login_existing_course(course: LoginDetails):
    course_content = course.dict()
    course_name = course_content['course_name']
    teacher_name = course_content['teacher_name']
    password = course_content['password']
    course_details = Course_info.find_one({'course_name': course_name, 'teacher_name': teacher_name, 'password': password})
    if not course_details:
        return {'status': 'failed', 'message': 'Invalid credentials'}
    return {'status': 'success', 'message': 'Login successful', 'data': {'Course_id': str(course_details['_id']), 'Class_Embeddings_id': str(course_details['class_name'])}}

