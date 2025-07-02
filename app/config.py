import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Конфигурация приложения"""
    DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    NSFW_THRESHOLD = 0.7

    ALLOWED_EXTENSIONS = {'jpg', 'png'}

    @staticmethod
    def is_valid_extension(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
