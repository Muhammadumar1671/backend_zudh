from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User_Model as get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class JWTTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
          email =  "john@example.com",
          password =  "your_password"
        )
        # Generate an access token and refresh token
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)

    def test_obtain_token(self):
        response = self.client.post('/login', {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Store tokens for later tests
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_refresh_token(self):
        response = self.client.post('token/refresh/', {
            'refresh': self.refresh,
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        # Verify new access token
        new_access_token = response.data['access']
        self.assertNotEqual(self.access_token, new_access_token)

    def test_access_protected_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_token_expiry(self):
        # Simulate token expiry
        expired_token = str(self.refresh.access_token)
        response = self.client.get('/protected', HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

