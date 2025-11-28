
const url ="https://facetrack-attendance.onrender.com"

const Get_course_id_Login_API = url+ "login_existing_course"
const Get_course_id_sigin_API=url+ "Create_New_Course"
const get_attendance_from_video =url +`attendance_data/` //define course id 
const get_attendance_from_image=url +`attendance_image/` //define cousre  id 
const get_downloadable_attendance =url +`csv_file/`

export {get_attendance_from_image ,get_attendance_from_video , get_downloadable_attendance ,Get_course_id_Login_API,Get_course_id_sigin_API}