import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Формат сообщения лога

file_handler = logging.FileHandler('logs/app.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
