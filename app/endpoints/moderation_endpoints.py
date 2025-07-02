from flask import Blueprint, request, jsonify

from app.services.deepai_service import DeepAIService
from app.services.validation_service import ValidationService
from app.models.responses import ModerationResponse, ErrorResponse
from app.utils.exceptions import ValidationException, DeepAIException

moderation_bp = Blueprint('moderation', __name__)


@moderation_bp.route('/moderate', methods=['POST'])
def moderate_image():
    """
    Эндпоинт для модерации изображений

    Принимает изображение в формате multipart/form-data
    и возвращает результат модерации
    """
    try:
        if 'file' not in request.files:
            return jsonify(
                ErrorResponse(
                    "validation_error",
                    "Файл не найден в запросе"
                ).to_dict()
            ), 400

        file = request.files['file']

        ValidationService.validate_file(file)

        deepai_service = DeepAIService()

        result = deepai_service.check_image(file)
        nsfw_score = result.get('nsfw_score', 0)

        if deepai_service.is_nsfw(nsfw_score):
            response = ModerationResponse.rejected(
                "NSFW content detected",
                nsfw_score=nsfw_score
            )
        else:
            response = ModerationResponse.ok(nsfw_score=nsfw_score)

        return jsonify(response.to_dict()), 200

    except ValidationException as e:
        return jsonify(
            ErrorResponse("validation_error", str(e)).to_dict()
        ), 400

    except DeepAIException as e:
        return jsonify(
            ErrorResponse("deepai_error", str(e)).to_dict()
        ), 500

    except Exception as e:
        return jsonify(
            ErrorResponse(
                "internal_error",
                f"Внутренняя ошибка сервера: {str(e)}"
            ).to_dict()
        ), 500


@moderation_bp.route('/health', methods=['GET'])
def health_check():
    """Эндпоинт для проверки здоровья сервиса"""
    return jsonify(
        {"status": "healthy", "service": "Image Moderation API"}), 200
