# --- IMPORTS ---
from src.components.header import os, sys, cv2, torch, YOLO, MTCNN, InceptionResnetV1, setup_logger , Yolo_Model_path, EDSR_Model_path
from src.components.helper_function import get_embeddings_from_database , detect_faces_from_frame, increase_resolution  ,retina_face_detect
from src.components.UserEmbedding import DB, Course_info, Class_Embeddings    




logger = setup_logger()

# --- MODEL & DB INITIALIZATION (Load once) ---
try:
    logger.info("Loading models...")
    yolo_model_path = Yolo_Model_path
    if not os.path.exists(yolo_model_path):
        logger.error(f"YOLO model not found at: {yolo_model_path}")
        sys.exit(1)
    Yolo = YOLO(yolo_model_path)

    edsr_model_path = EDSR_Model_path
    if not os.path.exists(edsr_model_path):
        logger.error(f"EDSR model not found at: {edsr_model_path}")
        sys.exit(1)
    # sr = cv2.dnn_superres.DnnSuperResImpl_create()
    # sr.readModel(edsr_model_path)
    # sr.setModel("edsr", 2)

    # Use 'cuda' if available, otherwise 'cpu'
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")

    MTCNN_model = MTCNN(image_size=224, margin=0, keep_all=False, device=device) # keep_all=False is faster
    ResNet_model = InceptionResnetV1(pretrained='vggface2', classify=False).eval().to(device)
    logger.info("All models loaded successfully.")

    Course_Collection = Course_info
    Embeddings_Collection = Class_Embeddings
    logger.info("Database collections initialized.")

except Exception as e:
    logger.error(f"Failed to load models or DB: {e}", exc_info=True)
    sys.exit(1)


# not used in our code 
# def increase_resolution(face_image):
#     """Upscales a face image using the pre-loaded EDSR model."""
#     # logger.debug("Upscaling face image...")
#     try:
#         # --- CRITICAL FIX 3: Use the pre-loaded 'sr' model ---
#         upscaled = sr.upsample(face_image)
#         # logger.debug(f"Image upscaled from {face_image.shape} to {upscaled.shape}")
#         return upscaled
#     except Exception as e:
#         logger.error(f"Failed to upscale image with shape {face_image.shape}: {e}")
#         return None # Return None on failure
     

def compare_with_embeddings(features_tensor, class_embeddings, device):
    similarity_threshold = 0.8 # Adjust as needed
    similarity = torch.nn.CosineSimilarity(dim=1)
    features_tensor = features_tensor / features_tensor.norm(dim=1, keepdim=True)
    scores=[]
    for usn, list_of_embedding_lists in class_embeddings.items():
        for db_embedding_list_name , db_embedding_list in list_of_embedding_lists.items():
            try:
                embedding_tensor = torch.tensor(db_embedding_list, dtype=torch.float32).to(device)
                if embedding_tensor.dim() == 1:
                    embedding_tensor = embedding_tensor.unsqueeze(0)
                
                if embedding_tensor.shape[1] != features_tensor.shape[1]:
                    logger.warning(f"Embedding shape mismatch for USN {usn}. DB: {embedding_tensor.shape}, Frame: {features_tensor.shape}. Skipping.")
                    continue
                
                embedding_tensor = embedding_tensor / embedding_tensor.norm(dim=1, keepdim=True)
                
                sim_score = similarity(features_tensor, embedding_tensor).item()
               
                logger.debug(f"Comparing with USN {usn}: similarity = {sim_score:.4f}")
                logger.info(f"Comparing with USN {usn} embedding {db_embedding_list_name}: similarity = {sim_score:.4f}")
                scores.append((usn, sim_score))
                
                    
            except Exception as e:
                logger.error(f"Error comparing embedding for USN {usn}: {e}. Embedding data (type {type(db_embedding_list)}): {str(db_embedding_list)[:50]}...")
    
    scores=sorted(scores, key=lambda x: x[1], reverse=True)[:7]
   
    if scores and scores[0][1] >= similarity_threshold:
        logger.debug(f"Match found: USN {scores[0][0]} with score {scores[0][1]:.4f}")
        return scores[0]  # Return the USN and score of the best match
    else:

        usn_count={}
        for usn, score in scores:
            if usn not in usn_count:
                usn_count[usn]=[0 ,0]
            usn_count[usn]=[usn_count[usn][0]+1 , usn_count[usn][1]+score]
            if usn_count[usn][0]>=3 and (usn_count[usn][1]/usn_count[usn][0])>=0.45: 
                logger.debug(f"Match found by majority voting: USN {usn} with score {score:.4f}")
                return usn, score
           
           
    
    logger.debug("No match found above threshold for this face")
    return None




def process_video(video_path, course_id, frame_count_device , device="cpu"):
    logger.info(f"Starting video processing: {video_path}")
    Marked_Students = []
    
    logger.info("Getting class embeddings from database...")
    CLass_Embeddings = get_embeddings_from_database(course_id , Course_Collection, Embeddings_Collection)
    logger.info(f"Retrieved embeddings for {len(CLass_Embeddings)} students.")
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        logger.error(f"Failed to open video file: {video_path}")
        return []  
    frame_count = 0
    
    try:
        while True:
            
            ret, frame = video.read()
            logger.info(f"started reading frame {frame_count}")
            if not ret:
                logger.info("End of video file reached.")
                break   
           
            
            frame_count += 1
            if frame_count % frame_count_device != 0: # Process 1 frame every 30 (adjust as needed)
                continue

            
            
            faces = detect_faces_from_frame(frame ,Yolo)
            logger.debug(f"Found {len(faces)} faces in frame {frame_count}")
            
            for i, face in enumerate(faces):
                if face.size == 0:
                    logger.warning(f"Skipping empty face crop in frame {frame_count}")
                    continue

                logger.debug(f"Processing Face {i+1} in frame {frame_count}")
                try:
                    
     
                   
                    aligned_face = MTCNN_model(face)
                    if aligned_face is None:
                        logger.warning(f"MTCNN failed to align face {i+1} in frame {frame_count}, skipping.")
                        continue
                    aligned_face_batch = aligned_face.unsqueeze(0).to(device) # Shape [1, 3, 160, 160]
                    with torch.no_grad(): # Disable gradient calculation for inference
                        features = ResNet_model(aligned_face_batch) # Shape [1, 512]
                    
                    matched_student = compare_with_embeddings(features, CLass_Embeddings, device)
                    
                    if matched_student:
                        usn, score = matched_student
                        logger.info(f"Found and marked student {usn} with confidence {score:.4f}")

                        if usn not in [list(d.keys())[0] for d in Marked_Students]:
                             os.makedirs("results", exist_ok=True)
                             cv2.imwrite(os.path.join("results", f"{usn}_{score}.jpg"), face)
                             Marked_Students.append({usn: score})
                        else:
                            # updae score if higher
                            for entry in Marked_Students:
                                if usn in entry and score > entry[usn]:
                                    entry[usn] = score
                                    cv2.imwrite(os.path.join("results", f"{usn}_{score}.jpg"), face)

                       
                except Exception as e:
                    logger.error(f"Error processing face {i+1} in frame {frame_count}: {e}", exc_info=True)
                    
    except Exception as e:
        logger.error(f"Error during video processing: {e}", exc_info=True)
    finally:
        video.release()
        logger.info("Video resource released.")
        
    logger.info(f"Total frames processed (at 1-in-5 rate): {frame_count // 5}")
    logger.info(f"Total unique students marked: {len(Marked_Students)}")
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
            results = process_video(self.video_path, self.course_id, 15 ,self.device)
            return results
        except Exception as e:
            logger.error(f"Critical error in GettingResults.get_results: {str(e)}", exc_info=True)
            raise




def process_image(image_path, course_id , device="cpu"):
    logger.info(f"Starting image processing: {image_path}")
    Marked_Students = []
    
    logger.info("Getting class embeddings from database...")
    CLass_Embeddings = get_embeddings_from_database(course_id , Course_Collection, Embeddings_Collection)
    logger.info(f"Retrieved embeddings for {len(CLass_Embeddings)} students.")
    image = cv2.imread(image_path)
    
    if image is None:
        logger.error(f"Failed to open image file: {image_path}")
        return []  
    
    try:
       
            
            faces = detect_faces_from_frame(image ,Yolo)
            logger.info(f"Found {len(faces)} faces in image {image_path}")
            for i, face in enumerate(faces):
                if face.size == 0:
                    logger.warning(f"Skipping empty face crop in image {image_path}")
                    continue

                logger.debug(f"Processing Face {i+1} in image {image_path}")
                try:
                    
                    cv2.imwrite(f"debug_face_{i+1}.jpg", face)  # Debug: Save the cropped face image
                    
                   
                    aligned_face = MTCNN_model(face)
                    if aligned_face is None:
                        logger.warning(f"MTCNN failed to align face {i+1} in image {image_path}, skipping.")
                        continue
                    aligned_face_batch = aligned_face.unsqueeze(0).to(device) # Shape [1, 3, 160, 160]
                    with torch.no_grad(): # Disable gradient calculation for inference
                        features = ResNet_model(aligned_face_batch) # Shape [1, 512]
                    
                    matched_student = compare_with_embeddings(features, CLass_Embeddings, device)
                    
                    if matched_student:
                        usn, score = matched_student
                        logger.info(f"Found and marked student {usn} with confidence {score:.4f}")

                        if usn not in [list(d.keys())[0] for d in Marked_Students]:
                             os.makedirs("results", exist_ok=True)
                             cv2.imwrite(os.path.join("results", f"{usn}_{score}.jpg"), face)
                             Marked_Students.append({usn: score})
                        else:
                            # updae score if higher
                            for entry in Marked_Students:
                                if usn in entry and score > entry[usn]:
                                    entry[usn] = score
                                    cv2.imwrite(os.path.join("results", f"{usn}_{score}.jpg"), face)

                       
                except Exception as e:
                    logger.error(f"Error processing face {i+1} in image {image_path}: {e}", exc_info=True)
                    
    except Exception as e:
        logger.error(f"Error during image processing: {e}", exc_info=True)
    finally:
        logger.info("Image processing completed.")
        
    
    logger.info(f"Total unique students marked: {len(Marked_Students)}")
    return list(Marked_Students)

# --- MAIN EXECUTION CLASS ---

class GettingResults_for_image:
    def __init__(self, image_path, course_id, device):
        self.image_path = image_path
        self.course_id = course_id
        self.device = device
        logger.info(f"GettingResults initialized for course {course_id} on device {device}")

    def get_results(self):
        try:
            results = process_image(self.image_path, self.course_id ,self.device)
            return results
        except Exception as e:
            logger.error(f"Critical error in GettingResults.get_results: {str(e)}", exc_info=True)
            raise




