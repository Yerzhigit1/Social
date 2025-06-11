import pytest
from rest_framework.test import APIClient
from .factories import *

@pytest.mark.django_db
class AuthTest:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory(is_active=True)
        # self.client.force_authenticate(user=self.user)
        
    def test_user_authenticate(self):
        response = self.client.post('api/auth/users/', {
            "email": self.user.email,
            "full_name": self.user.full_name,
            "password": "password.1234"
        })
        
        assert response.status_code == 201
        assert 'email' in response.data
        assert 'date_joined' in response.data