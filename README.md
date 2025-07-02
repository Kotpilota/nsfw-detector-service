# nsfw-detector-service

Простой сервер для модерации изображений с использованием DeepAI NSFW API.

## Описание

Приложение принимает изображения и проверяет их на наличие нежелательного контента (NSFW) с помощью DeepAI API. Если `nsfw_score > 0.7`, изображение отклоняется.

## Важное примечание о DeepAI API

**Текущий статус:** В задании указано, что DeepAI API бесплатный, но бесплатные кредиты на новых аккаунтах отсутствуют. При попытке использования API возвращается ошибка:

```json
{
  "status": "Out of API credits - please enter payment info in your dashboard: https://deepai.org/dashboard"
}
```

**Что работает:**
- Полная архитектура приложения реализована
- Валидация файлов работает корректно
- Интеграция с DeepAI API настроена и готова к использованию
- Все эндпоинты функционируют, кроме фактического вызова внешнего API


## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Kotpilota/nsfw-detector-service.git
cd nsfw-detector-service
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

1. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Получите API ключ на [DeepAI](https://deepai.org/dashboard) и добавьте его в `.env`:
```
DEEPAI_API_KEY=your_actual_api_key_here
```

### 5. Запуск сервера

```bash
python app.py
```

Сервер будет доступен по адресу: `http://localhost:8000`

## API Endpoints

### POST /moderate

Проверяет изображение на наличие NSFW контента.

**Параметры:**
- `file` (multipart/form-data) - изображение в формате `.jpg` или `.png`

**Успешный ответ (безопасное изображение):**
```json
{
    "status": "OK",
    "nsfw_score": 0.123
}
```

**Ответ для NSFW контента:**
```json
{
    "status": "REJECTED",
    "reason": "NSFW content detected",
    "nsfw_score": 0.856
}
```

**Ошибка валидации:**
```json
{
    "error": "validation_error",
    "message": "Неподдерживаемый формат файла. Разрешены: jpg, png"
}
```

### GET /health

Проверка состояния сервиса.

**Ответ:**
```json
{
    "status": "healthy",
    "service": "Image Moderation API"
}
```

## Примеры запросов

### cURL

```bash
# Проверка безопасного изображения
curl -X POST -F "file=@safe_image.jpg" http://localhost:8000/moderate

# Проверка здоровья сервиса
curl http://localhost:8000/health
```

### Postman

1. Создайте POST запрос на `http://localhost:8000/moderate`
2. В разделе "Body" выберите "form-data"
3. Добавьте поле `file` типа "File" и выберите изображение
4. Отправьте запрос

## Технические детали

- **Framework:** Flask
- **API:** DeepAI NSFW Detector
- **Поддерживаемые форматы:** JPG, PNG
- **Максимальный размер файла:** 16MB

### Структура проекта

```
├── app/
│   ├── controllers/        # Контроллеры
│   ├── services/           # Бизнес-логика
│   ├── models/             # Модели данных
│   ├── utils/              # Утилиты и исключения
│   └── config.py           # Конфигурация
├── app.py                  # Точка входа
├── requirements.txt        # Зависимости
└── .env.example            # Пример переменных окружения
```