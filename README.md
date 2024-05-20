# Система бронирования отелей

## Обзор

Система бронирования отелей — это веб-приложение, предназначенное для упрощения процесса бронирования номеров в отелях. Система позволяет пользователям регистрироваться, входить в систему, управлять своими профилями и бронировать номера. Также предусмотрен административный интерфейс для управления пользователями и бронированиями. Проект разработан на языке Python с использованием фреймворка FastAPI для создания RESTful API.

## Функционал

- **Аутентификация пользователей:**
  - Регистрация пользователей
  - Вход в систему
  - Аутентификация на основе токенов (JWT)
  - Обновление токена доступа

- **Управление пользователями:**
  - Получение информации о текущем пользователе
  - Обновление информации о пользователе (методы PUT и PATCH)
  - Смена пароля
  - Удаление аккаунта пользователя
  - Получение списка всех пользователей (только для администраторов)

- **Управление бронированиями:**
  - Получение списка бронирований (для авторизованных пользователей)
  - Создание нового бронирования
  - Отправка уведомлений по электронной почте при создании бронирования
  - Удаление бронирования

- **Управление отелями:**
  - Получение списка всех отелей по локации и датам
  - Получение детальной информации об отеле
  - Получение списка всех комнат в отеле

## Стек технологий

- **Python:** Основной язык программирования для логики приложения.
- **FastAPI:** Используется для создания высокопроизводительных RESTful API.
- **PostgreSQL:** База данных для хранения информации о пользователях, бронированиях и отелях.
- **SQLAlchemy:** ORM для взаимодействия с базой данных.
- **Alembic:** Для управления миграциями базы данных.
- **Pytest:** Для написания и выполнения тестов.
- **Pydantic:** Для валидации и сериализации данных.
- **Celery:** Для обработки асинхронных задач, таких как отправка уведомлений по электронной почте.
- **Flower:** Для мониторинга задач Celery.
- **Redis:** В качестве брокера сообщений для Celery и для кэширования.
- **Docker & Docker Compose:** Для контейнеризации приложения и управления многоконтейнерными развертываниями.
- **SQLAdmin:** Административный интерфейс для управления данными.

## Установка

### Предварительные требования

- Python 3.8+
- Docker и Docker Compose

### Настройка

  1. Клонируйте репозиторий:

    git clone https://github.com/pavlechenk/BookingService.git
    cd BookingService
   

  2. Создайте и активируйте виртуальное окружение:

    python -m venv venv

    source venv/bin/activate # для Linux/MacOS
    venv/Scripts/activate # для Windows


  3. Установите зависимости:

    pip install -r requirements.txt


  4. Скачайте и установите PostgreSQL с официального сайта:

    https://www.postgresql.org/download/


  5. Создайте необходимые бд и пользователя при помощи следующих SQL запросов:

    CREATE DATABASE booking_db;
    CREATE DATABASE test_booking_db;

    CREATE ROLE name with password 'password'; # Укажите свое имя пользователя и пароль

    GRANT ALL PRIVILEGES ON DATABASE 'booking_db' to name;  # Вместо name укажите имя своего пользователя
    GRANT ALL PRIVILEGES ON DATABASE 'test_booking_db' to name;  # Вместо name укажите имя своего пользователя


  6. Переименуйте файл .env-example в .env в корневом каталоге и заполните переменные окружения необходимыми данными:

    MODE=DEV
    LOG_LEVEL=INFO

    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=
    DB_PASSWORD=
    DB_NAME=booking_db

    TEST_DB_HOST=localhost
    TEST_DB_PORT=5432
    TEST_DB_USER=
    TEST_DB_PASSWORD=
    TEST_DB_NAME=test_booking_db

    REDIS_HOST=localhost
    REDIS_PORT=6379

    SENTRY_DNS=

    ORIGINS=localhost;127.0.0.1

    EMAIL_HOST=smtp.google.com
    EMAIL_PORT=587
    EMAIL_USER=
    EMAIL_PASSWORD=


  7. Также созайте файл .env-docker для Docker compose и заполните его необходимыми данными:

    MODE=DEV
    LOG_LEVEL=INFO

    DB_HOST=db
    DB_PORT=5432
    DB_USER=
    DB_PASSWORD=
    DB_NAME=booking_db


    POSTGRES_DB=booking_db
    POSTGRES_USER=
    POSTGRES_PASSWORD=


    REDIS_HOST=redis
    REDIS_PORT=6379

    SENTRY_DNS=

    ORIGINS=localhost;127.0.0.1

    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USER=
    EMAIL_PASSWORD=


  8. Примените миграции с помощью следующей команды:
    
    alembic upgrade head


  9. Создайте Docker образ приложения FastAPI:

    docker build -t booking_image .


  10. Запуск приложения с помощью Docker Compose:

    docker compose up --build


## Запуск сервера Uvicorn

Если вы хотите запустить сервер Uvicorn без использования Docker, выполните следующие шаги:

    1. Убедитесь, что зависимости установлены и виртуальное окружение активировано.

    2. Запустите сервер Uvicorn:

      uvicorn app.main:app --reload

## Использование

    1. Документация API доступна по адресу http://localhost:8000/v2/docs

    2. Используйте предоставленные эндпоинты для регистрации, входа в систему, управления бронированиями и других операций.


## Сайт

    Приложение доступно по следующему адресу: [Hotel Booking System](https://api.bookings-service.online/v1/docs)


## Вклад

    Приглашаем к участию! Открывайте issue или отправляйте pull request для внесения изменений и улучшений.

## Лицензия

    Этот проект лицензирован под лицензией [MIT](LICENSE). Подробности смотрите в файле [LICENSE](LICENSE).


