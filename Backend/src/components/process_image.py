
from src.utils.header import cv2 , os
from src.components.compare_embeddings import compare_with_embeddings
from src.components.load_parameters import logger  ,Course_Collection ,Embeddings_Collection ,torch ,Yolo ,MTCNN_model ,ResNet_model
from src.utils.helper_function import get_embeddings_from_database , detect_faces_from_frame





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
                            
                             Marked_Students.append({usn: score})
                        else:
                            # updae score if higher
                            for entry in Marked_Students:
                                if usn in entry and score > entry[usn]:
                                    entry[usn] = score
                                  

                       
                except Exception as e:
                    logger.error(f"Error processing face {i+1} in image {image_path}: {e}", exc_info=True)
                    
    except Exception as e:
        logger.error(f"Error during image processing: {e}", exc_info=True)
    finally:
        logger.info("Image processing completed.")
        
    
    logger.info(f"Total unique students marked: {len(Marked_Students)}")
    return list(Marked_Students)
