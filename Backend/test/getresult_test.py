import sys
import os 
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


from src.utils.log import setup_logger
from src.components.gettingresults import GettingResults
import torch


logger=setup_logger()
if __name__ == "__main__":
    logger.info("====== SCRIPT STARTED ======")
    try:
        # --- UPDATE THESE VALUES ---
        video = r"C:\Users\KADAK SINGH\OneDrive\Desktop\VTMA-1\Backend\20251016_140704.mp4"
        course_id = "69174e704b2e968c865b1105" # Example Course ID
        
        # Check if image file exists
        if not os.path.exists(video):
            logger.error(f"Image file not found at: {video}")
            sys.exit(1)
            
        logger.info(f"Starting process for image: {video} and course ID: {course_id}")
        
        # Get the device that was set during model initialization
        device_to_use = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
        getting_results = GettingResults(video, course_id, device_to_use)
        results = getting_results.get_results()
        
        logger.info("====== FINAL RESULTS ======")
        logger.info(f"Marked Students (USNs): {results}")
        
    except Exception as e:
        logger.error(f"Main execution block error: {str(e)}", exc_info=True)
    finally:
        logger.info("====== SCRIPT FINISHED ======")