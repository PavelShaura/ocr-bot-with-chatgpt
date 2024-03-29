import logging

import aiohttp

from ocrbot.config import config


async def extract_text(file_path: str, language: str) -> str:
    """
    Извлекает текст из изображения, используя API для распознавания текста.

    :param file_path: Путь к файлу изображения.
    f"https://api.telegram.org/file/bot{config.tg_bot.token}/{file.file_path}"
    :type file_path: str
    :param language: Язык текста на изображении.
    :type language: str
    :return: Извлеченный текст или сообщение об ошибке.
    :rtype: str
    """
    async with aiohttp.ClientSession() as session:
        url = (
            f"https://api.ocr.space/parse/imageurl?apikey={config.ocr_api}&url={file_path}&language={language}"
            f"&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True"
        )
        async with session.get(url) as response:
            data = await response.json()
            if not data["IsErroredOnProcessing"]:
                return data["ParsedResults"][0]["ParsedText"]
            else:
                logging.info(
                    f"Something went wrong when extracting text from an image using the text recognition API."
                )
                return "Что-то пошло не так ..."
