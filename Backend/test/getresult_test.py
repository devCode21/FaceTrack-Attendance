import sys
import os 
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


from src.utils.log import setup_logger
from src.components.gettingresults import GettingResults_for_image
import torch


logger=setup_logger()
if __name__ == "__main__":
    logger.info("====== SCRIPT STARTED ======")
    try:
        # --- UPDATE THESE VALUES ---
        image_path = r"C:\Users\KADAK SINGH\OneDrive\Desktop\VTMA-1\Backend\images\Dhanushya Bhaskar Shetty 1BM23EC03 IMG  (1).jpg"
        course_id = "6915ccc17a307f8baf3f7c2e" # Example Course ID
        
        # Check if image file exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found at: {image_path}")
            sys.exit(1)
            
        logger.info(f"Starting process for image: {image_path}")
        
        # Get the device that was set during model initialization
        device_to_use = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
        getting_results = GettingResults_for_image(image_path, course_id, device_to_use)
        results = getting_results.get_results()
        
        logger.info("====== FINAL RESULTS ======")
        logger.info(f"Marked Students (USNs): {results}")
        
    except Exception as e:
        logger.error(f"Main execution block error: {str(e)}", exc_info=True)
    finally:
        logger.info("====== SCRIPT FINISHED ======")