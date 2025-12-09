
from src.utils.header import cv2 , os
from src.components.compare_embeddings import compare_with_embeddings
from src.components.load_parameters import logger  ,Course_Collection ,Embeddings_Collection ,torch ,Yolo ,MTCNN_model ,ResNet_model
from src.utils.helper_function import get_embeddings_from_database , detect_faces_from_frame
output_path="outputvideo.mp4"



def outwrite_video(frame ,image_coordianates, fps=2 ):
    print("writing video frame with detected faces")
   
    
    if (image_coordianates!=[]) :
        for coord  in image_coordianates:

            cordinates , usn = coord
            print("coordinates are :" , cordinates)
            x1, y1, x2, y2 = cordinates
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, usn, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)   
    logger.info(f"Output video written to {output_path}")
   
    return frame
  
   
 



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
    
    ret, frame = video.read()
    if not ret:
        logger.error(f"Failed to read first frame from video file: {video_path}")
        return []
    
    fps = video.get(cv2.CAP_PROP_FPS)
    height, width, _ = frame.shape
    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )
    updated_frame=None
    try:
        while True:
            
            ret, frame = video.read()
            logger.info(f"started reading frame {frame_count}")
            if not ret:
                logger.info("End of video file reached.")
                break   
           
            
            frame_count += 1
            if frame_count % frame_count_device != 0:
                if updated_frame is not None:
                    out.write(updated_frame)
                else:
                    out.write(frame) # Process 1 frame every 30 (adjust as needed)
                continue

            
            
            faces , coordinates = detect_faces_from_frame(frame ,Yolo)
            logger.debug(f"Found {len(faces)} faces in frame {frame_count}")
            coordinates_list=[]
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
                            Marked_Students.append({usn: score})
                            
                            #  os.makedirs("results", exist_ok=True)
                            #  cv2.imwrite(os.path.join("results", f"{usn}_{score}.jpg"), face)
                            
                        else:
                            # updae score if higher
                            for entry in Marked_Students:
                                if usn in entry and score > entry[usn]:
                                    entry[usn] = score
                                    # cv2.imwrite(os.path.join("results", f"{usn}_{score}.jpg"), face)
                        
                        coordinates_list.append((coordinates[i] ,usn))
                       
           
                    
                except Exception as e:
                   logger.error(f"Error processing face {i+1} in frame {frame_count}: {e}", exc_info=True)
            if frame_count==360:
               break
                       
            updated_frame =outwrite_video(frame, coordinates_list , fps=fps)
            out.write(updated_frame)
            cv2.imwrite(f"debug_frame_{frame_count}.jpg", updated_frame)  #     Debug: Save the processed frame
    except Exception as e:
        logger.error(f"Error during video processing: {e}", exc_info=True)
    finally:
        video.release()
        out.release()
        logger.info("Video resource released.")
        
    logger.info(f"Total frames processed (at 1-in-5 rate): {frame_count // 5}")
    logger.info(f"Total unique students marked: {len(Marked_Students)}")
    return list(Marked_Students)
