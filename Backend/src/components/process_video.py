
from src.utils.header import cv2 , os
from src.components.compare_embeddings import compare_with_embeddings
from src.components.load_parameters import logger  ,Course_Collection ,Embeddings_Collection ,torch ,Yolo ,MTCNN_model ,ResNet_model
from src.utils.helper_function import get_embeddings_from_database , detect_faces_from_frame




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
