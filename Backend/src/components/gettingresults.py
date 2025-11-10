# --- IMPORTS ---
import cv2 
import torch
from pathlib import Path
from ultralytics import YOLO
import numpy as np
import logging
from datetime import datetime
import os
import sys
from facenet_pytorch import MTCNN, InceptionResnetV1
from bson.objectid import ObjectId  # <-- CRITICAL FIX 1: For MongoDB query
from utils.log import setup_logger

from components.helper_function import get_embeddings_from_database , detect_faces_from_frame
# --- LOCAL IMPORTS (Make sure UserEmbedding.py is in the same folder) ---
try:
    # Make sure UserEmbedding.py is in the same directory or Python path
    from components.UserEmbedding import DB, Course_info, Class_Embeddings
    print("Successfully imported DB, Course_info, Class_Embeddings")
    print(f"Course_info Collection: {Course_info}")
    print(f"Class_Embeddings Collection: {Class_Embeddings}")
except ImportError as e:
    print(f"Error importing from UserEmbedding: {e}")
    print("Please ensure UserEmbedding.py is in the same directory.")
    sys.exit(1)



#
# Create logger instance
logger = setup_logger()


# --- MODEL & DB INITIALIZATION (Load once) ---
try:
    logger.info("Loading models...")
    # NOTE: Update this path to your YOLO model
    yolo_model_path = r'C:\Users\KADAK SINGH\OneDrive\Desktop\VTMA-1\Backend\yolov8n-face.pt'
    if not os.path.exists(yolo_model_path):
        logger.error(f"YOLO model not found at: {yolo_model_path}")
        sys.exit(1)
    Yolo = YOLO(yolo_model_path)
    
    # NOTE: Update this path to your EDSR model
    edsr_model_path = r"C:\Users\KADAK SINGH\OneDrive\Desktop\VTMA-1\Backend\EDSR_x2.pb"
    if not os.path.exists(edsr_model_path):
        logger.error(f"EDSR model not found at: {edsr_model_path}")
        sys.exit(1)
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(edsr_model_path)
    sr.setModel("edsr", 2)

    # Use 'cuda' if available, otherwise 'cpu'
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")

    MTCNN_model = MTCNN(image_size=160, margin=0, keep_all=False, device=device) # keep_all=False is faster
    ResNet_model = InceptionResnetV1(pretrained='vggface2', classify=False).eval().to(device)
    logger.info("All models loaded successfully.")

    Course_Collection = Course_info
    Embeddings_Collection = Class_Embeddings
    logger.info("Database collections initialized.")

except Exception as e:
    logger.error(f"Failed to load models or DB: {e}", exc_info=True)
    sys.exit(1)




# --- CORE FUNCTIONS ---        

def compare_with_embeddings(features_tensor, class_embeddings, device):
   
    # logger.info("Starting face comparison...")
    similarity_threshold = 0.7  # Cosine similarity. Tune this value as needed.
    similarity = torch.nn.CosineSimilarity(dim=1)
    
    # Normalize the input features tensor once
    features_tensor = features_tensor / features_tensor.norm(dim=1, keepdim=True)
    
    # --- CRITICAL FIX 5: Assuming this schema and loop ---
    # This iterates through each student USN in the class
    for usn, list_of_embedding_lists in class_embeddings.items():
        # This iterates through each stored embedding for that student
        for db_embedding_list_name , db_embedding_list in list_of_embedding_lists.items():
            try:
                # Convert list from DB to a 2D tensor [1, 512] and move to device
                embedding_tensor = torch.tensor(db_embedding_list, dtype=torch.float32).to(device)
                if embedding_tensor.dim() == 1:
                    embedding_tensor = embedding_tensor.unsqueeze(0)
                
                # Check for shape mismatch
                if embedding_tensor.shape[1] != features_tensor.shape[1]:
                    logger.warning(f"Embedding shape mismatch for USN {usn}. DB: {embedding_tensor.shape}, Frame: {features_tensor.shape}. Skipping.")
                    continue
                
                # Normalize the DB embedding
                embedding_tensor = embedding_tensor / embedding_tensor.norm(dim=1, keepdim=True)
                
                # Calculate similarity
                sim_score = similarity(features_tensor, embedding_tensor).item() # .item() to get float
                
                logger.debug(f"Comparing with USN {usn}: similarity = {sim_score:.4f}")
                
                if sim_score > similarity_threshold:
                    logger.info(f"Match found! USN: {usn}, Similarity: {sim_score:.4f}")
                    return usn, sim_score
                    
            except Exception as e:
                logger.error(f"Error comparing embedding for USN {usn}: {e}. Embedding data (type {type(db_embedding_list)}): {str(db_embedding_list)[:50]}...")
    
    logger.debug("No match found above threshold for this face")
    return None

def process_video(video_path, course_id, device):
    logger.info(f"Starting video processing: {video_path}")
    # --- CRITICAL FIX 4: Use a 'set' for unique students ---
    Marked_Students = []
    
    logger.info("Getting class embeddings from database...")
    CLass_Embeddings = get_embeddings_from_database(course_id , Course_Collection, Embeddings_Collection)
    
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        logger.error(f"Failed to open video file: {video_path}")
        return []
        
    frame_count = 0
    
    try:
        while True:
            ret, frame = video.read()
            if not ret:
                logger.info("End of video file reached.")
                break
                
            frame_count += 1
            
            # --- CRITICAL FIX 4: Process every Nth frame for performance ---
            if frame_count % 60 != 0: # Process 1 frame every 30 (adjust as needed)
                continue
            
            logger.info(f"Processing frame {frame_count}")
            
            faces = detect_faces_from_frame(frame ,Yolo)
            logger.debug(f"Found {len(faces)} faces in frame {frame_count}")
            
            for i, face in enumerate(faces):
                if face.size == 0:
                    logger.warning(f"Skipping empty face crop in frame {frame_count}")
                    continue

                logger.debug(f"Processing Face {i+1} in frame {frame_count}")
                try:
                    # --- CRITICAL FIX 4: Use cv2.resize ---
                    # Resize to 80x80 for EDSR to upscale to 160x160


                    high_res_face = cv2.resize(face, (160, 160))

                    # --- CRITICAL FIX 4: Check for 'None' on failure ---
                    if high_res_face is None:
                        logger.warning(f"Upscaling failed for face {i+1}, skipping.")
                        continue


                    # MTCNN auto-detects device; returns a [3, 160, 160] tensor or None
                    aligned_face = MTCNN_model(high_res_face)
                    
                    # --- CRITICAL FIX 4: Check for 'None' on failure ---
                    if aligned_face is None:
                        logger.warning(f"MTCNN failed to align face {i+1} in frame {frame_count}, skipping.")
                        continue
                        
                    # --- CRITICAL FIX 4: Add batch dimension and move to device ---
                    aligned_face_batch = aligned_face.unsqueeze(0).to(device) # Shape [1, 3, 160, 160]
                    
                    # Generate features on the correct device
                    with torch.no_grad(): # Disable gradient calculation for inference
                        features = ResNet_model(aligned_face_batch) # Shape [1, 512]
                    
                    matched_student = compare_with_embeddings(features, CLass_Embeddings, device)
                    
                    if matched_student:
                        usn, score = matched_student
                        logger.info(f"Found and marked student {usn} with confidence {score:.4f}")

                        if usn not in [list(d.keys())[0] for d in Marked_Students]: 
                             Marked_Students.append({usn: score})
                        cv2.imwrite(f"frame{frame_count}_face{i+1}_USN{usn}.jpg", face)
                    
                 
                except Exception as e:
                    logger.error(f"Error processing face {i+1} in frame {frame_count}: {e}", exc_info=True)
                    
    except Exception as e:
        logger.error(f"Error during video processing: {e}", exc_info=True)
    finally:
        video.release()
        logger.info("Video resource released.")
        
    logger.info(f"Total frames processed (at 1-in-5 rate): {frame_count // 5}")
    logger.info(f"Total unique students marked: {len(Marked_Students)}")
    
    # Convert set back to list for the final result
    return list(Marked_Students)

# --- MAIN EXECUTION CLASS ---

class GettingResults:
    def __init__(self, video_path, course_id, device):
        self.video_path = video_path
        self.course_id = course_id
        self.device = device
        logger.info(f"GettingResults initialized for course {course_id} on device {device}")

    def get_results(self):
        try:
            results = process_video(self.video_path, self.course_id, self.device)
            return results
        except Exception as e:
            logger.error(f"Critical error in GettingResults.get_results: {str(e)}", exc_info=True)
            raise




