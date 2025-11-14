

from src.components.header import os, Path, Image, torch , MTCNN, InceptionResnetV1
from src.DataBase.pymong import DB , Course_info , Class_Embeddings
import numpy as np
mtcnn = MTCNN(image_size=224, margin=0)
resnet = InceptionResnetV1(pretrained='vggface2' , classify=False).eval()
 
def get_info_from_image(image_path):
    image_path = str(image_path)
    filename = Path(image_path).name
    values = filename.split(' ')  
    name = values[0]
    usn = name
    img_id = str(np.random.randint(1000000))  # removes extension
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
            Img=Img.resize((224,224))
            img_cropped = self.mtcnn(Img)
            
            if img_cropped is None:
                print(f"Face not detected in image: {i} {Img.size}")

                continue
                # img_cropped=Img.to(torch.FloatTensor).permute(2,0,1)/255.0
                # img_cropped.squeeze_()
            
            with torch.inference_mode():
                img_probs = self.resnet(img_cropped.unsqueeze(0))
            if Name not in self.DataBase:
                self.DataBase[Name] = {}
            self.DataBase[Name][id] = img_probs.cpu().numpy().tolist()

    def return_Databases(self):
        self.embeddings()
        return self.DataBase

    


class Class_embeddings_to_Database:
    def __init__(self ,ExtractEmbeddings ,ClassName , Image_folder_path , Class_collection): 
        self.image_folder_path = Image_folder_path
        self.Embeddings  = ExtractEmbeddings(self.image_folder_path , mtcnn , resnet , get_info_from_image).return_Databases()
        self.ClassName = ClassName
        self.Class_collection = Class_collection   #class collection database hai 
    
    def save_embeddings(self):
        data = {
            'class_name': self.ClassName,
            'embeddings': self.Embeddings,
        }
        result = self.Class_collection.insert_one(data)
        return result.inserted_id  




class create_Course_Info:
    def __init__(self , Course_Name , Teacher_Name , Password , Class_Name  , Course_collection , class_collection ):
        self.Course_Name = Course_Name
        self.Teacher_Name = Teacher_Name
        self.Password = Password
        self.ClassName = Class_Name
        self.Course_collection =Course_collection  #Cousrse Database
        self.Class_collection = class_collection   #class Database

    def save_course_info(self):
        try :
            ClassName_embeddings_id = self.Class_collection.find_one({'class_name': self.ClassName})['_id']
        except :
            raise ValueError("Class embeddings not found")
        data = {
            'course_name': self.Course_Name,
            'teacher_name': self.Teacher_Name,
            'password': self.Password,
            'class_name': ClassName_embeddings_id
        }
        result = self.Course_collection.insert_one(data)
        return result.inserted_id

        

# # storing class embeddings to database
# image_folder_path = Path("C:/Users/KADAK SINGH/OneDrive/Desktop/VTMA-1/Backend/images")
# ClassName = "Semester 5 B"
# Class_Embeddings.delete_many({})
# Class_embeddings_to_Database_instance = Class_embeddings_to_Database(ExtractEmbeddings , ClassName , image_folder_path , Class_Embeddings)
# class_embeddings_id = Class_embeddings_to_Database_instance.save_embeddings()