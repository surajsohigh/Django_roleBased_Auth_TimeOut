# Django Custom Authentication Backend

This project demonstrates a custom authentication backend for a Django application, including time-based access control for users based on their roles. It includes models, serializers, views, and test cases to ensure proper functionality.

---

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [How to Run](#how-to-run)
- [Running Tests](#running-tests)
- [Folder Structure](#folder-structure)
- [Endpoints](#endpoints)

---

## Features
1. **Custom Authentication Backend**:
   - Role-based time-restricted login.
   - User roles: `admin`, `manager`, `employee`.
2. **User Management**:
   - User registration and login.
   - Password validation.
3. **Token-based Authentication**:
   - (Optional) JWT authentication for secure user sessions.
4. **Unit and Integration Tests**:
   - Comprehensive test cases for all core functionalities.

---

## Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Django 3.2+
- PostgreSQL or SQLite (for database)

### Installation Steps

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up the database:
   Update the `DATABASES` configuration in `settings.py` to match your environment.

   Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```

---

## How to Run

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000/`.

3. Use the following endpoints for testing:
   - `/register/`: Register a new user.
   - `/login/`: Login as an existing user.
   - `/`: Simple test home view.

---

## Running Tests

This project uses `pytest` for testing.

### Steps:
1. Install testing dependencies:
   ```bash
   pip install pytest pytest-django
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. Run a specific test file:
   ```bash
   pytest path/to/test_auth_backend.py
   ```

4. Add `-v` for verbose output:
   ```bash
   pytest -v
   ```

---

## Folder Structure

```
my_app/
├── models.py          # Custom user model
├── authentication.py  # Custom authentication backend
├── serializers.py     # DRF serializers for user registration and login
├── views.py           # API views for registration and login
├── tests/             # Test cases
│   └── test_auth_backend.py
└── ...
```

---

## Endpoints

### 1. Register User
**POST** `/register/`
- **Payload**:
  ```json
  {
      "email": "newuser@test.com",
      "password": "password123",
      "role": "employee"
  }
  ```
- **Response**:
  ```json
  {
      "message": "User Registered Successfully"
  }
  ```

### 2. Login User
**POST** `/login/`
- **Payload**:
  ```json
  {
      "email": "employee@test.com",
      "password": "password123"
  }
  ```
- **Response (Success)**:
  ```json
  {
      "msg": "Login Succesful"
  }
  ```
- **Response (Failure)**:
  ```json
  {
      "msg": "Time Out"
  }
  ```

### 3. Home
**GET** `/`
- **Response**:
  ```text
  Your Test response
  ```

---

## Author
Feel free to reach out if you have any questions or need help with this project!

