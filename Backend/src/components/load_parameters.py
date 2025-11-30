from src.utils.header import os, sys, cv2, torch, YOLO, MTCNN, InceptionResnetV1, logger , Yolo_Model_path
from src.DataBase.pymong import DB , Course_info , Class_Embeddings


# --- MODEL & DB INITIALIZATION (Load once) ---
try:
    logger.info("Loading models...")
    yolo_model_path = Yolo_Model_path
    if not os.path.exists(yolo_model_path):
        logger.error(f"YOLO model not found at: {yolo_model_path}")
        sys.exit(1)
    Yolo = YOLO(yolo_model_path)

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
