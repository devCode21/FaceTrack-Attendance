# required library 
import PIL
from PIL import Image
import torch
import torchvision 
from torch import nn 
from dataclasses import dataclass
from facenet_pytorch import MTCNN, InceptionResnetV1
image_size=160
from pathlib import Path 
import cv2 as cv


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=image_size, margin=0)
# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2' , classify=False).eval()


# image folder path 
# image_file_name should be in format of Name_USN_id.jpg 
def get_info_from_image(image_path):
    # Ensure we work with string filename
    image_path = str(image_path)
    
    # Extract filename without folder
    filename = Path(image_path).name
    
    # Split by underscore
    values = filename.split(' ')  # [Name, USN, id.jpg]
    
    # Extract fields
    name = [a for a in values if len(a)>5 ][0]
    usn = [v for v in values if v.startswith('1BM23')][0]  # safely assumes USN starts with 1BM23
    img_id = Path(values[-1]).stem  # removes extension
    
    # Open image
    img = Image.open(image_path)
    
    return img, name, usn, img_id
class ExtractEmbeddings:
    def __init__(self, image_folder_path, mtcnn, resnet, get_info_from_image):
        self.image_folder_path = image_folder_path
        self.mtcnn = mtcnn
        self.resnet = resnet
        self.get_info_from_image = get_info_from_image
        self.Img_path = list(Path(image_folder_path).glob("*.jpg"))
        self.DataBase = {}
        self.usn_to_name = {}

    def embeddings(self):
        for i in self.Img_path:
            Img, Name, USN, id = self.get_info_from_image(i)
            
            if Img is None:
                continue
            Img=Img.resize((160,160))

            self.usn_to_name[USN] = Name

          
            img_cropped = self.mtcnn(Img)

            if img_cropped is None:
                continue

            with torch.inference_mode():
                img_probs = self.resnet(img_cropped.unsqueeze(0))

            # L2 normalize embeddings
            img_probs_normalised = img_probs 

            if USN not in self.DataBase:
                self.DataBase[USN] = {}
            self.DataBase[USN][id] = img_probs_normalised.cpu().numpy().tolist()

    def return_Databases(self):
        self.embeddings()
        return self.DataBase, self.usn_to_name

    
# just storing embeddings to DataBase (Studens right ) just image folder path  , differnt page
# create new Course info in DataBase => Course Name , Teacher Name , Password , Class Name  . different page hai 
#  video  path , different page hai

class Class_embeddings_to_Database:
    def __init__(self ,ExtractEmbeddings ,ClassName , Image_folder_path , Class_collection): 
        self.image_folder_path = Image_folder_path
        self.Embeddings , self.usn_mapping = ExtractEmbeddings(self.image_folder_path , mtcnn , resnet , get_info_from_image).return_Databases()
        self.ClassName = ClassName
        self.Class_collection = Class_collection
    
    def save_embeddings(self):
        data = {
            'class_name': self.ClassName,
            'embeddings': self.Embeddings,
            'usn_mapping': self.usn_mapping
        }
        result = self.Class_collection.insert_one(data)
        return result.inserted_id


class create_Course_Info:
    def __init__(self , Course_Name , Teacher_Name , Password , Class_Name  , Course_collection , class_collection ):
        self.Course_Name = Course_Name
        self.Teacher_Name = Teacher_Name
        self.Password = Password
        self.ClassName = Class_Name
        self.Course_collection =Course_collection
        self.Class_collection = class_collection

    def save_course_info(self):
        try :
            self.ClassName_embeddings_id = self.Class_collection.find_one({'class_name': self.ClassName})['_id']
        except :
            self.ClassName_embeddings_id = None
        if not self.ClassName_embeddings_id:
            raise ValueError("Class embeddings not found")
        data = {
            'course_name': self.Course_Name,
            'teacher_name': self.Teacher_Name,
            'password': self.Password,
            'class_name': self.ClassName_embeddings_id
        }
        result = self.Course_collection.insert_one(data)
        return result.inserted_id

        
    



password=quote_plus('Kadak21@')

uri = f"mongodb+srv://gwkadak:{password}@cluster0.h93js.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


DB =client['Database']










import os 
Img_path =r'C:\Users\KADAK SINGH\OneDrive\Desktop\VTMA-1\Backend\images'
print(list(os.walk(Img_path)))

ClassName =''
Teacher_Name ='Sudhindra'
password='DSP123'
Class_Embeddings=DB['Class_Embeddings']
Course_info =DB['Course_info']
usn_Collection =DB['USN_TO_NAME']




    


# # .run Class embeddings to Database
# Class_embeddings_id = Class_embeddings_to_Database(ExtractEmbeddings ,ClassName , Img_path , Class_Embeddings).save_embeddings()
# print("Class Embeddings ID:", Class_embeddings_id)


# run create Course Info
# Course_info_id = create_Course_Info( 'Digital Signal Processing' , Teacher_Name , password , "ABC" , Course_info , Class_Embeddings).save_course_info()
# print("Course Info ID:", Course_info_id)

