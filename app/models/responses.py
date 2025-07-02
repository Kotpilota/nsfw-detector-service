from typing import Optional


class ModerationResponse:
    """Класс для стандартизации ответов модерации"""

    STATUS_OK = "OK"
    STATUS_REJECTED = "REJECTED"

    def __init__(self, status: str, reason: Optional[str] = None,
                 nsfw_score: Optional[float] = None):
        self.status = status
        self.reason = reason
        self.nsfw_score = nsfw_score

    def to_dict(self):
        """Преобразует объект в словарь для JSON ответа"""
        result = {"status": self.status}

        if self.reason:
            result["reason"] = self.reason

        if self.nsfw_score is not None:
            result["nsfw_score"] = round(self.nsfw_score, 3)

        return result

    @classmethod
    def ok(cls, nsfw_score: Optional[float] = None):
        """Создает ответ для безопасного контента"""
        return cls(cls.STATUS_OK, nsfw_score=nsfw_score)

    @classmethod
    def rejected(cls, reason: str, nsfw_score: Optional[float] = None):
        """Создает ответ для отклоненного контента"""
        return cls(cls.STATUS_REJECTED, reason=reason, nsfw_score=nsfw_score)


class ErrorResponse:
    """Класс для стандартизации ответов об ошибках"""

    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message

    def to_dict(self):
        """Преобразует объект в словарь для JSON ответа"""
        return {
            "error": self.error,
            "message": self.message
        }
