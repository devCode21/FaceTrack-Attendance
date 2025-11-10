import sys
import os 
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(parent_dir, "src"))

from utils.log import setup_logger
from components.gettingresults import GettingResults
import torch


logger=setup_logger()
if __name__ == "__main__":
    logger.info("====== SCRIPT STARTED ======")
    try:
        # --- UPDATE THESE VALUES ---
        video_path = r"C:\Users\KADAK SINGH\OneDrive\Desktop\VTMA-1\Backend\20251016_140704.mp4"
        course_id = "68fb892b4d3868846b27d08d" # Example Course ID
        
        # Check if video file exists
        if not os.path.exists(video_path):
            logger.error(f"Video file not found at: {video_path}")
            sys.exit(1)
            
        logger.info(f"Starting process for video: {video_path}")
        
        # Get the device that was set during model initialization
        device_to_use = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
        getting_results = GettingResults(video_path, course_id, device_to_use)
        results = getting_results.get_results()
        
        logger.info("====== FINAL RESULTS ======")
        logger.info(f"Marked Students (USNs): {results}")
        
    except Exception as e:
        logger.error(f"Main execution block error: {str(e)}", exc_info=True)
    finally:
        logger.info("====== SCRIPT FINISHED ======")