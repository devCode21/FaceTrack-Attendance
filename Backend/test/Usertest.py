
import os
from pathlib import Path
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
print(parent_dir)
from src.DataBase.pymong import Class_Embeddings, Course_info
from src.components.UserEmbedding import Class_embeddings_to_Database, ExtractEmbeddings, create_Course_Info



image_folder_path = Path("C:/Users/KADAK SINGH/OneDrive/Desktop/VTMA-1/Backend/images")
ClassName = "Semester5B"
Class_embeddings_to_Database_instance = Class_embeddings_to_Database(ExtractEmbeddings , ClassName , image_folder_path , Class_Embeddings)
class_embeddings_id =  Class_embeddings_to_Database_instance.save_embeddings()
print(f"Class Embeddings saved with ID: {class_embeddings_id}")
create_course_instance = create_Course_Info("DSP" ,"SUDHINDRA"  , "password123" , ClassName , Course_info , Class_Embeddings)
course_id = create_course_instance.save_course_info()
print(f"Course Info saved with ID: {course_id}")