# --- IMPORTS ---
from src.components.process_image import logger ,process_image
from src.components.process_video import logger ,process_video

# --- Video pipeline  ---

class GettingResults:
    def __init__(self, video_path, course_id, device):
        self.video_path = video_path
        self.course_id = course_id
        self.device = device
        logger.info(f"GettingResults initialized for course {course_id} on device {device}")

    def get_results(self):
        try:
            results = process_video(self.video_path, self.course_id, 1 ,self.device)
            return results
        except Exception as e:
            logger.error(f"Critical error in GettingResults.get_results: {str(e)}", exc_info=True)
            raise






# --- Image pipline  ---




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




