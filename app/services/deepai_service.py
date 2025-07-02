import requests

from app.config import Config
from app.utils.exceptions import DeepAIException


class DeepAIService:
    """Сервис для работы с DeepAI NSFW API"""

    BASE_URL = "https://api.deepai.org/api/nsfw-detector"

    def __init__(self):
        self.api_key = Config.DEEPAI_API_KEY
        if not self.api_key:
            raise DeepAIException(
                "DEEPAI_API_KEY не найден в переменных окружения")

    def check_image(self, image_file):
        """
        Проверяет изображение на NSFW контент

        Args:
            image_file: файл изображения

        Returns:
            dict: результат проверки с полями nsfw_score и output_url

        Raises:
            DeepAIException: если произошла ошибка при обращении к API
        """
        try:
            files = {'image': image_file}
            headers = {'api-key': self.api_key}

            response = requests.post(
                self.BASE_URL,
                files=files,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                raise DeepAIException(
                    f"DeepAI API вернул код {response.status_code}: {response.text}"
                )

            result = response.json()

            if 'nsfw_score' not in result:
                raise DeepAIException("Некорректный ответ от DeepAI API")

            return result

        except requests.exceptions.RequestException as e:
            raise DeepAIException(
                f"Ошибка при обращении к DeepAI API: {str(e)}")
        except Exception as e:
            raise DeepAIException(f"Неожиданная ошибка: {str(e)}")

    def is_nsfw(self, nsfw_score):
        """
        Определяет, является ли контент NSFW на основе score

        Args:
            nsfw_score (float): оценка NSFW от 0 до 1

        Returns:
            bool: True если контент NSFW, False иначе
        """
        return nsfw_score > Config.NSFW_THRESHOLD
