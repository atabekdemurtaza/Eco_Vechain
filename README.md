# Eco Vechain API

## Русский (Russian)

Этот проект представляет собой API для приложения Eco Vechain.

### Установка

1. Клонируйте репозиторий:

```
git clone <URL репозитория>
cd eco-vechain
```

2. Установите зависимости:

```
pip install -r requirements/requirements.txt
```

3. Примените миграции:

```
python manage.py migrate
```

### Запуск сервера

Запустите сервер с помощью следующей команды:

```
python manage.py runserver
```

Сервер будет доступен по адресу [http://localhost:8000/](http://localhost:8000/).

### Доступ к API

#### Swagger UI

Документация API доступна в Swagger UI:

[http://localhost:8000/swagger/](http://localhost:8000/swagger/)

#### ReDoc

Документация API также доступна в ReDoc:

[http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### Эндпоинты

#### Аутентификация

- `auth/register/`: Регистрация нового пользователя.
- `auth/login/`: Вход пользователя.
- `auth/refresh/`: Обновление токена доступа.
- `auth/logout/`: Выход пользователя.

#### Пользователи

- `user/`: Получение списка пользователей и создание нового пользователя.


## English (Английский)

This project is an API for the Eco Vechain application.

### Installation

1. Clone the repository:

```
git clone <repository URL>
cd eco-vechain
```

2. Install dependencies:

```
pip install -r requirements/requirements.txt
```

3. Apply migrations:

```
python manage.py migrate
```

### Running the Server

Run the server using the following command:

```
python manage.py runserver
```

The server will be available at [http://localhost:8000/](http://localhost:8000/).

### Accessing the API

#### Swagger UI

The API documentation is available in Swagger UI:

[http://localhost:8000/swagger/](http://localhost:8000/swagger/)

#### ReDoc

The API documentation is also available in ReDoc:

[http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### Endpoints

#### Authentication

- `auth/register/`: Register a new user.
- `auth/login/`: User login.
- `auth/refresh/`: Refresh access token.
- `auth/logout/`: User logout.

#### Users

- `user/`: Get a list of users and create a new user.
