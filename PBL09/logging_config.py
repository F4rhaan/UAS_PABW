import logging
import uuid
from datetime import datetime
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = 'logs'

# Create log directory if it does not exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logging():
    # Setup the logging format
    formatter = logging.Formatter(
        '%(asctime)s | %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    
    # Setup file handler for saving logs to a file
    file_handler = RotatingFileHandler(os.path.join(LOG_DIR, 'app_actions.log'), maxBytes=1000000, backupCount=3)
    file_handler.setFormatter(formatter)

    # Setup the stream handler for console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Get the logger and apply handlers
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.INFO)  # You can change this to DEBUG for more verbose logging
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def log_action(action, request):
    logger = logging.getLogger('app_logger')  # Get the logger
    log_message = f'{str(uuid.uuid4())} | {datetime.now().strftime("%Y-%m-%dT%H:%M:%S")} | ACTION: {action} | IP: {request.remote_addr} | APP: {request.user_agent}'
    logger.info(log_message)  # Log the action message
