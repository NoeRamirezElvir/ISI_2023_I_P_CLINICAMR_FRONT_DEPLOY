import os
import logging
from datetime import datetime

def definir_log_info(name,folder):
    logs_folder = 'logs/'+folder
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(logs_folder, f"{name}_{timestamp}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(processName)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    for existing_handler in logger.handlers:
        logger.removeHandler(existing_handler)

    logger.addHandler(handler)

    return logger
