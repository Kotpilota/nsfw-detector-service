from PIL import Image
from werkzeug.datastructures import FileStorage
from app.config import Config
from app.utils.exceptions import ValidationException


class ValidationService:
    """Сервис для валидации загружаемых файлов"""

    @staticmethod
    def validate_file(file):
        """
        Валидирует загружаемый файл

        Args:
            file: объект файла из Flask request

        Raises:
            ValidationException: если файл не прошел валидацию
        """
        if not file:
            raise ValidationException("Файл не был загружен")

        if not isinstance(file, FileStorage):
            raise ValidationException("Некорректный тип файла")

        if file.filename == '':
            raise ValidationException("Имя файла пустое")

        if not Config.is_valid_extension(file.filename):
            raise ValidationException(
                f"Неподдерживаемый формат файла. "
                f"Разрешены: {', '.join(Config.ALLOWED_EXTENSIONS)}"
            )

        ValidationService._validate_image_format(file)
        file.seek(0)

    @staticmethod
    def _validate_image_format(file):
        """
        Проверяет, что файл действительно является корректным изображением

        Args:
            file: объект файла

        Raises:
            ValidationException: если файл не является корректным изображением
        """
        try:
            with Image.open(file) as img:
                img.verify()
        except Exception as e:
            raise ValidationException(
                f"Файл не является корректным изображением: {str(e)}")
        finally:
            file.seek(0)
