
from src.app_utils.fast_api_header import os, app ,Course_info, Class_Embeddings,UploadFile ,GettingResults ,GettingResults_for_image ,torch ,File ,pd
from src.app_utils.pydanatic_schemas import Course,LoginDetails
from src.app_utils.Api_resposne import ErrorResponse ,API_respone
from fastapi.responses import FileResponse

# ---------------- video ->result -----------------------
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

    return { "results": results  , "status":"successfully sent the attendance"  }



# --------------image to result -------------------------------------------

def get_attendance_from_image(course_id: str, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return {"status": "failed", "message": "Invalid file type. Please upload an image file."}
    if not file:
        return {"status": "failed", "message": "No file uploaded."}
    
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
    df['Names']= [list(res.keys())[0] for res in results]
    df['Accuracy']= [list(res.values())[0] for res in results]
    df.to_csv(f'uploads/attendance_{course_id}.csv', index=False)
    return {"filename": file.filename, "content_type": file.content_type, "results": results , "status" : "success"}



#  --------------download csv ---------------------------------------------

def get_csv_file(course_id: str):
    file_path = f'uploads/attendance_{course_id}.csv'
    
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=f"attendance_{course_id}.csv",
            media_type="text/csv"
        )
    else:
        return {"status": "failed", "message": "File not found"}
