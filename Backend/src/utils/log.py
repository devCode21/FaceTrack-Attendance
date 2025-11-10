import logging
import os
import sys
from datetime import datetime
def setup_logger():
    """
    Sets up a robust logger that saves to a 'logs' directory 
    relative to this script's location.
    """
    try:
        # Get the directory where this script is located
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            # This assumes the script is being run directly
            script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Fallback if __file__ is not defined (e.g., in interactive shell/notebook)
        print("Warning: __file__ is not defined. Using current working directory for logs.")
        script_dir = os.getcwd()
        
    log_dir = os.path.join(script_dir, 'logs')
    
    try:
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'face_recognition_{timestamp}.log')
        
        # Setup logger
        logger = logging.getLogger('gettingresults')
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        if logger.hasHandlers():
            logger.handlers.clear()
        
        # File handler
        fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(fh)
        
        # Stream (console) handler
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(sh)
        
        logger.info(f"Logger setup complete. Logging to: {log_file}")
        return logger
        
    except Exception as e:
        print(f"Error setting up logger in {log_dir}: {str(e)}")
        raise
