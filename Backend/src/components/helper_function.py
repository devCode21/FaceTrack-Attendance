from src.utils.log import setup_logger
from retinaface import RetinaFace
logger = setup_logger()
from src.components.header import  ObjectId
 # For MongoDB queries
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
    usn_mapping = course.get('usn_mapping')
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
    return Embeddings , usn_mapping


# get the frames from the video and detect faces using YOLO model
def detect_faces_from_frame(frame ,Yolo):
    model = Yolo
    results = model(frame, verbose=False) # verbose=False to silent YOLO logs
    faces = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            face_crop = frame[y1:y2, x1:x2]
            faces.append(face_crop)
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





def retina_face_detect(frame):
    if frame is None:
        logger.error("Input frame is None")
        return []
    try:
        detections = RetinaFace.detect_faces(frame)
        faces = []
        if isinstance(detections, dict):
            for key in detections:
                face_info = detections[key]
                x1, y1, x2, y2 = map(int, face_info['facial_area'])
                face_crop = frame[y1:y2, x1:x2]
                faces.append(face_crop)
        return faces
    except Exception as e:
        logger.error(f"RetinaFace detection failed: {e}")
        return []