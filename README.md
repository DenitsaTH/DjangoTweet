# DjangoTweet

Twitter clone, implemented with Django and Django REST Framework.

## Table of contents

* [Technologies](#technologies-used)
* [Setup](#installation-and-setup)
* [Features](#features)
* [Background tasks](#background-tasks)
* [Structure](#project-structure)
* [Try it out](#try-it-out)

---

## Technologies Used

**Framework:** Django

**API:** Django Rest Framework

**Authentication**: Token-based authentication with `rest_framework.authtoken`

**Database:** SQLite

**Background Tasks Queue:** Celery

**Tasks Scheduler**: Celery Beat

**Message Broker**: RabbitMQ

---

## Installation and setup

### 1. Install the project dependencies

```
pip install -r requirements.txt
```

## 2. Run Migrations to create the database

```
python manage.py makemigrations
python manage.py migrate
```

### 3. Open a new terminal, make sure your .venv (if using one) is active and run the below command to start the server

```
python manage.py runserver
```

### 5. Swagger docs available at: [Link](http://127.0.0.1:8000/api/v1/swagger/schema/)

---

## Features

- **Public endpoints** - accessible without authentication
    * Register user
    * Login
    * Logout


- **Authentication Endpoints** - require login with email and password

    - **Features, related to users:**
        * Edit profile information (names and description only)
        * Upload or change profile picture
        * Retrieve user's posts and accumulated likes of all user's posts
  
    - **Features, related to posts:**
        * Submit a post
        * Retrieve all posts (shows last 20 posts by default)
        * Like/unlike a post
        * Delete a post (owner required)

---

## Background Tasks

To activate background tasks, follow these steps:

### 1. Install RabbitMQ

Follow the official instructions for installation (Windows): [Link](https://www.rabbitmq.com/docs/install-windows)

### 2. Start RabbitMQ Server:

Ensure RabbitMQ is running. You can start RabbitMQ with:

```
.\rabbitmq-service.bat start
```

### 3. Start Celery Worker:

In one terminal window, start the Celery worker:

```
celery -A django_project worker -l info --pool=solo
```

### 4. Start Celery Beat:

In another terminal window, start Celery Beat:

```
celery -A django_project beat --loglevel=info
```

With these steps, the background tasks will be activated and your Celery worker along with Celery Beat will handle the scheduling and execution of tasks such as hard deleting posts that were marked as `is_deleted` over a specified amount of time (can be changed in the `posts/tasks.py` module).

The tasks are currently set to run every 30 seconds. You can change this in `celery.py`.

---

## Project Structure

```
django_project/                             - core project folder
├─ celery.py                                - celery settings
├─ serializers.py                           - model serializers
├─ settings.py                              - project settings
├─ urls.py                                  - url patterns
media/                                    - media uploads
posts/                                    - posts app
├─ migrations/                              - db migrations
├─ api.py                                   - api logic
├─ admin.py                                 - admin features
├─ core.py                                  - core app module
├─ models.py                                - posts models
├─ services.py                              - crud logic
├─ tasks.py                                 - background tasks
users/                                    - users app (structure similar to posts)
README.md                                 - project decription
exceptions.py                             - custom exceptions
manage.py                                 - main module
requirements.txt                          - project requirements
```

---

## Try it out

### 1. Create a superuser with `python manage.py createsuperuser` or use this already created admin:

- Email: admin@somedomain.com
- Password: admin

### 2. Access the admin page:

- [Link](http://127.0.0.1:8000/admin/)

From the admin page, you can:

- see recently registered and sandboxed users
- mark users as active
- see deleted posts
- restore delete posts

### 3. Access Swagger documentation to test the API:

- [Link](http://127.0.0.1:8000/api/v1/swagger/schema/)


### 4. Register an user using the dedicated public endpoint or login with an already created user account:

- Email: user1@somedomain.com
- Pass: pass


### 5. For Swagger to remember your authentication Token:

- Click on *Authorize* button
- Example for *Value* field: Token 18ef4d413eb691df11c6f60719e3617fce1adb4a (since user1 is logged in)

### 6. Refer to the API documentation for each endpoint for more information.
