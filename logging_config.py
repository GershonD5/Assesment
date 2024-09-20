import logging

def configure_logging():
    logging.basicConfig(filename='process_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
