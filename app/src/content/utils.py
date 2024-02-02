"""
Вспомогательные функции приложения content.
"""

from src.logger import logger


def process_images(file_path):
    """Производит обработку загружаемых изображений."""
    # INFO: строго говоря, изображения обрабатываются через специальные
    #       библиотеки, например, Pillow, и тогда код должен выглядеть так:
    #
    # from PIL import Image
    # with Image.open("original_image.jpg") as img:
    #     resized_img = img.resize((new_width, new_height))
    #     resized_img.save("resized_image.jpg")
    with open(file=file_path, mode='w+') as file:
        # Тут логика обработки
        logger.info(f'Файл {file} успешно обработан')
    return


def process_text(file_path):
    """Производит обработку загружаемых текстовых файлов."""
    with open(file=file_path, mode='w+') as file:
        # Тут логика обработки
        logger.info(f'Файл {file} успешно обработан')
    return
