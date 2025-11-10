from utils.log import setup_logger
logger = setup_logger()
from bson.objectid import ObjectId  # For MongoDB queries
def get_embeddings_from_database(course_id , Course_Collection, Embeddings_Collection  ):
    logger.info(f"Searching for course ID: {course_id}")
    try:
        # --- CRITICAL FIX 2: Convert string ID to ObjectId for query ---
        course = Course_Collection.find_one({'_id': ObjectId(course_id)})
    except Exception as e:
        logger.error(f"Invalid Course ID format: {course_id}. Error: {e}")
        raise ValueError("Invalid Course ID format")

    if not course:
        logger.error(f"Course not found in database for ID: {course_id}")
        raise ValueError("Course not found")

    logger.info(f"Found course: {course.get('course_name', 'N/A')}")
    
    # Assuming 'class_name' in 'Course_info' stores the 'id' for 'Class_Embeddings'
    class_id = course.get('class_name') 
    if not class_id:
        logger.error(f"Course {course_id} has no 'class_name' field to link to embeddings.")
        raise ValueError("Course has no embedding link")
        
    logger.info(f"Looking for embeddings with class ID: {class_id}")
    embeddings_doc = Embeddings_Collection.find_one({'_id': class_id})
    
    if not embeddings_doc or 'embeddings' not in embeddings_doc:
        logger.error(f"No embeddings document found for class ID: {class_id}")
        raise ValueError("Embeddings not found for this class")

    Embeddings = embeddings_doc['embeddings']
    # ASSUMED SCHEMA: Embeddings = {'usn1': [ [emb1_list], [emb2_list] ], 'usn2': [ [emb3_list] ]}
    logger.info(f"Found embeddings for {len(Embeddings)} students")
    return Embeddings


# get the frames from the video and detect faces using YOLO model
def detect_faces_from_frame(frame ,Yolo):
    # This function is fast, so logging every call is too noisy.
    # logger.debug("Processing frame for face detection")
    model = Yolo
    results = model(frame, verbose=False) # verbose=False to silent YOLO logs
    faces = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Add a small check for valid crop
            if y2 > y1 and x2 > x1:
                face_crop = frame[y1:y2, x1:x2]
                faces.append(face_crop)
                # logger.debug(f"Detected face at coordinates: ({x1}, {y1}, {x2}, {y2})")

    # logger.debug(f"Total faces detected in frame: {len(faces)}")
    return faces



def increase_resolution(face_image):
    """Upscales a face image using the pre-loaded EDSR model."""
    # logger.debug("Upscaling face image...")
    try:
        # --- CRITICAL FIX 3: Use the pre-loaded 'sr' model ---
        upscaled = sr.upsample(face_image)
        # logger.debug(f"Image upscaled from {face_image.shape} to {upscaled.shape}")
        return upscaled
    except Exception as e:
        logger.error(f"Failed to upscale image with shape {face_image.shape}: {e}")
        return None # Return None on failure