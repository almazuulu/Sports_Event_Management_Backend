import pytest
from django.urls import reverse
from rest_framework import status
from users.models import User

pytestmark = pytest.mark.user  # Mark all tests in this file as user tests

@pytest.mark.django_db
class TestUserAPI:
    """
    User API tests
    """
    
    def test_user_registration(self, api_client):
        """
        Test registration of a new user
        """
        url = reverse('users:user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecureP@ssw0rd',
            'password_confirm': 'SecureP@ssw0rd',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'public'
        }
    
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['email'] == 'newuser@example.com'
        assert response.data['username'] == 'newuser'
        assert response.data['role'] == 'public'
        
    
    def test_change_password_success(self, public_client, public_user):
        """
        Test successful password change
        """
        url = reverse('users:change-password')
        data = {
            'old_password': 'password123',  # Current password from fixture
            'new_password': 'NewSecureP@ssw0rd',
            'new_password_confirm': 'NewSecureP@ssw0rd'
        }
        
        response = public_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'password set'
        
        # Verify that the password has indeed changed
        user = User.objects.get(id=public_user.id)
        assert user.check_password('NewSecureP@ssw0rd')

    def test_change_password_wrong_old_password(self, public_client):
        """
        Test password change with incorrect old password
        """
        url = reverse('users:change-password')
        data = {
            'old_password': 'wrong_password',  # Incorrect current password
            'new_password': 'NewSecureP@ssw0rd',
            'new_password_confirm': 'NewSecureP@ssw0rd'
        }
        
        response = public_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'old_password' in response.data

    def test_change_password_mismatch(self, public_client):
        """
        Test password change with mismatched new passwords
        """
        url = reverse('users:change-password')
        data = {
            'old_password': 'password123',  # Current password from fixture
            'new_password': 'NewSecureP@ssw0rd',
            'new_password_confirm': 'DifferentP@ssw0rd'  # Does not match new_password
        }
        
        response = public_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in str(response.data).lower()  # Check that the error is related to the password
        
    def test_change_password_unauthenticated(self, api_client):
        """
        Test that unauthenticated users cannot change password
        """
        url = reverse('users:change-password')
        data = {
            'old_password': 'password123',
            'new_password': 'NewSecureP@ssw0rd',
            'new_password_confirm': 'NewSecureP@ssw0rd'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_get_profile(self, public_client):
        """
        Test retrieving the profile of the current user
        """
        url = reverse('users:profile')
        response = public_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'user@example.com'
        assert response.data['username'] == 'publicuser'
        assert response.data['role'] == 'public'
        
    def test_admin_can_list_users(self, admin_client, all_users):
        """
        Test that an admin can retrieve the list of all users
        """
        url = reverse('users:user-list')
        response = admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        
        # Ensure that we see at least as many users as we created
        user_count = len(all_users)
        result_count = len(response.data['results'])
        assert result_count >= user_count, f"Expected at least {user_count} users, got {result_count}"
        
    def test_non_admin_cannot_list_users(self, public_client):
        """
        Test that a regular user cannot retrieve the list of all users
        """
        url = reverse('users:user-list')
        response = public_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_create_user_success(self, api_client):
        """
        Test successful user creation
        """
        url = reverse('users:user-list')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecureP@ssw0rd123',
            'password_confirm': 'SecureP@ssw0rd123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'public'
        }

        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'testuser'
        assert response.data['email'] == 'test@example.com'

    def test_create_user_invalid_data(self, api_client):
        """
        Test user creation with invalid data
        """
        url = reverse('users:user-list')
        data = {
            'username': 'testuser',
            'email': 'invalid-email',  # Invalid email
            'password': '123',  # Weak password
            'password_confirm': '123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'public'
        }

        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
            
    def test_retrieve_user_as_admin(self, admin_client, public_user):
        """
        Test retrieving a user's details as an admin
        """
        url = reverse('users:user-detail', kwargs={'pk': public_user.id})
        response = admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == public_user.username

    def test_retrieve_user_as_owner(self, public_client, public_user):
        """
        Test retrieving own user details
        """
        url = reverse('users:user-detail', kwargs={'pk': public_user.id})
        response = public_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == public_user.username

    def test_update_user_partial(self, public_client, public_user):
        """
        Test partial update of user profile
        """
        url = reverse('users:user-detail', kwargs={'pk': public_user.id})
        data = {
            'first_name': 'Updated First Name'
        }
        
        response = public_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated First Name'

    def test_delete_user_as_admin(self, admin_client, public_user):
        """
        Test deleting a user as an admin
        """
        url = reverse('users:user-detail', kwargs={'pk': public_user.id})
        
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Проверяем, что пользователь действительно удален
        with pytest.raises(User.DoesNotExist):
            User.objects.get(pk=public_user.id)
            
    # Tests for ProfileView
    def test_update_profile_full(self, public_client, public_user):
        """
        Test full profile update
        """
        url = reverse('users:profile')
        data = {
            'email': public_user.email,  # Текущий email
            'username': public_user.username,  # Текущий username
            'first_name': 'Updated',
            'last_name': 'Profile'
        }
        
        response = public_client.put(url, data, format='json')
        
        # Отладочная информация
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Profile'
        
    # Tests for Roles
    def test_roles_list_admin_access(self, admin_client):
        """
        Test that an admin can access roles list
        """
        url = reverse('users:roles-list')
        response = admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4  # Количество ролей в системе
        
    def test_roles_list_non_admin_forbidden(self, public_client):
        """
        Test that a non-admin user cannot access roles list
        """
        url = reverse('users:roles-list')
        response = public_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN