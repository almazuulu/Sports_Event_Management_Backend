import os
import sys
from pathlib import Path

# Получаем корневую директорию проекта
BASE_DIR = Path(__file__).resolve().parent

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, str(BASE_DIR))

# Устанавливаем путь к модулям Python
os.environ['PYTHONPATH'] = str(BASE_DIR)

# Убеждаемся, что Django settings корректно установлены
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def all_users(db, admin_user, team_captain_user, scorekeeper_user, public_user):
    """
    Fixture that creates all user types and returns them as a list
    """
    return [admin_user, team_captain_user, scorekeeper_user, public_user]

@pytest.fixture
def api_client():
    """
    Fixture that returns a Django REST framework API client
    """
    return APIClient()

@pytest.fixture
def admin_user(db):
    """
    Fixture that creates and returns an admin user
    """
    admin = User.objects.create_user(
        email='admin@example.com',
        username='admin',
        password='password123',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_staff=True,
        is_superuser=True
    )
    return admin

@pytest.fixture
def team_captain_user(db):
    """
    Fixture that creates and returns a team captain user
    """
    captain = User.objects.create_user(
        email='captain@example.com',
        username='captain',
        password='password123',
        first_name='Team',
        last_name='Captain',
        role='team_captain'
    )
    return captain

@pytest.fixture
def scorekeeper_user(db):
    """
    Fixture that creates and returns a scorekeeper user
    """
    scorekeeper = User.objects.create_user(
        email='scorekeeper@example.com',
        username='scorekeeper',
        password='password123',
        first_name='Score',
        last_name='Keeper',
        role='scorekeeper'
    )
    return scorekeeper

@pytest.fixture
def public_user(db):
    """
    Fixture that creates and returns a regular user
    """
    user = User.objects.create_user(
        email='user@example.com',
        username='publicuser',
        password='password123',
        first_name='Public',
        last_name='User',
        role='public'
    )
    return user

@pytest.fixture
def admin_client(admin_user, api_client):
    """
    Fixture that returns an API client authenticated as an admin
    """
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.fixture
def team_captain_client(team_captain_user, api_client):
    """
    Fixture that returns an API client authenticated as a team captain
    """
    refresh = RefreshToken.for_user(team_captain_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.fixture
def scorekeeper_client(scorekeeper_user, api_client):
    """
    Fixture that returns an API client authenticated as a scorekeeper
    """
    refresh = RefreshToken.for_user(scorekeeper_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.fixture
def public_client(public_user, api_client):
    """
    Fixture that returns an API client authenticated as a regular user
    """
    refresh = RefreshToken.for_user(public_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client