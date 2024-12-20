
# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from datetime import datetime
from my_app.authentication import TimeRestrictedBackend
from my_app.models import MyUser
from rest_framework.test import APIClient
from unittest import mock
from rest_framework import status



User = get_user_model()

@pytest.fixture
def create_users():
    """Fixture to create test users."""
    users = [
        User.objects.create_user(email="admin@test.com", password="adminpass", role="admin"),
        User.objects.create_user(email="manager@test.com", password="managerpass", role="manager"),
        User.objects.create_user(email="employee@test.com", password="employeepass", role="employee"),
    ]
    return users

@pytest.fixture
def api_client():
    """Fixture to create an API test client."""
    return APIClient()

# Unit Tests
@mock.patch('datetime.datetime')
@pytest.mark.django_db
def test_authenticate_valid_time(mock_datetime, create_users):
    """Test authentication with valid time ranges."""
    backend = TimeRestrictedBackend()

    # Mock datetime to simulate a valid login time
    mock_datetime.now.return_value = datetime(2024, 12, 15, 10)  # 10 AM
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)  # Handle other datetime calls

    # Call the authenticate method with valid time for the manager role
    user = backend.authenticate(None, email="manager@test.com", password="managerpass")

    # Assertions to verify that the user is authenticated successfully
    assert user is not None
    assert user.email == "manager@test.com"


@pytest.mark.django_db
def test_authenticate_invalid_credentials(create_users):
    """Test authentication with invalid credentials."""
    backend = TimeRestrictedBackend()
    user = backend.authenticate(None, email="manager@test.com", password="wrongpass")
    assert user is None

@pytest.mark.django_db
def test_get_user(create_users):
    """Test the get_user method."""
    backend = TimeRestrictedBackend()
    user = create_users[0]  # admin@test.com
    fetched_user = backend.get_user(user.id)
    assert fetched_user == user

@pytest.mark.django_db
def test_get_user_nonexistent():
    """Test get_user with a nonexistent user ID."""
    backend = TimeRestrictedBackend()
    user = backend.get_user(9999)  # Nonexistent user ID
    assert user is None

# Integration Tests
@pytest.mark.django_db
def test_register_user(api_client):
    """Test the user registration endpoint."""
    payload = {
        "email": "newuser@test.com",
        "password": "newpassword",
        "role": "employee",
    }
    response = api_client.post("/register/", payload)
    assert response.status_code == 201
    assert response.data["message"] == "User Registered Successfully"

import pytest
from unittest import mock
from datetime import datetime
from my_app.models import MyUser
from rest_framework import status

@pytest.mark.django_db
@mock.patch('datetime.datetime')
def test_login_user_valid_time(mock_datetime, api_client):
    """Test the user login endpoint with a valid time."""

    # Mock datetime to simulate a valid login time
    mock_datetime.now.return_value = datetime(2024, 12, 15, 13)  # 1 PM, valid time for employee
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)  # Handle other datetime calls

    # Create an employee user with a unique email for testing
    user = MyUser.objects.create_user(
        email="employee_1@test.com",
        password="employeepass",
        role="employee"
    )

    payload = {
        "email": "employee_1@test.com",
        "password": "employeepass",
    }
    response = api_client.post("/login/", payload)
    
    # Assert the response status code and message
    assert response.status_code == status.HTTP_200_OK
    assert response.data["msg"] == "Login Succesful"


@pytest.mark.django_db
@mock.patch('datetime.datetime')
def test_login_user_invalid_time(mock_datetime, api_client):
    """Test the user login endpoint with an invalid time."""

    # Mock datetime to simulate an invalid login time
    mock_datetime.now.return_value = datetime(2024, 12, 15, 21)  # 9 PM, outside allowed time for employee (12 PM - 8 PM)
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)  # Handle other datetime calls

    # Create an employee user with a unique email for testing
    user = MyUser.objects.create_user(
        email="employee_2@test.com",
        password="employeepass",
        role="employee"
    )

    payload = {
        "email": "employee_2@test.com",
        "password": "employeepass",
    }
    response = api_client.post("/login/", payload)
    
    # Assert the response status code and message for time restriction
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "User Time Out" in response.data["msg"]


@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    """Test the user login endpoint with invalid credentials."""

    # Create an employee user for testing
    MyUser.objects.create_user(
        email="employee@test.com",
        password="employeepass",
        role="employee"
    )

    payload = {
        "email": "employee@test.com",
        "password": "wrongpass",  # Invalid password
    }
    response = api_client.post("/login/", payload)
    
    # Assert the response status code and error message
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid login credentials" in str(response.data)


@pytest.mark.django_db
def test_login_nonexistent_user(api_client):
    """Test the user login endpoint with a nonexistent user."""

    payload = {
        "email": "nonexistent@test.com",  # Non-existent email
        "password": "doesntmatter",  # Doesn't matter, since the user does not exist
    }
    response = api_client.post("/login/", payload)
    
    # Assert the response status code and error message
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Email Not Found, Please Register first" in str(response.data)

