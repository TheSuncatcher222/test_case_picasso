"""
Celery задачи приложения content.
"""

from src.content.models import File
from src.celery import app_celery
from src.content.utils import process_images, process_text
from src.logger import logger


@app_celery.task()
def process_file(file_type: str, file_path: str, instance_id: int):
    """Фоновая задача Celery по обработке загружаемых файлов."""
    if file_type.startswith('image'):
        logger.info(f'Начинается обработка изображения {file_path}')
        process_images(file_path=file_path)
    elif file_type.startswith('text'):
        logger.info(f'Начинается обработка текста {file_path}')
        process_text(file_path=file_path)
    else:
        logger.info(f'В обработку попал невалидный файл {file_path}')
        return

    # INFO: не вызовет событий (в т.ч. сигналов и обновления даты изменения!),
    #       не требует .save(), так как выполняется напрямую в БД.
    File.objects.filter(id=instance_id).update(processed=True)

    return
