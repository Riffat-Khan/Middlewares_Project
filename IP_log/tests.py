from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile
from .enum import RoleChoice
from django.utils import timezone

User = get_user_model()

class MiddlewareForLoggingDataTest(TestCase):

    @patch('logging.getLogger')
    def test_ip_logging(self, mock_get_logger):
        self.user = User.objects.create_user(email='aiza@gmail.com', password='Riffat@1100')
        self.profile = Profile.objects.create(user=self.user, role=RoleChoice.GOLD.value, count=0, last_access_time=timezone.now())

        client = Client()
        client.login(email='aiza@gmail.com', password='Riffat@1100')
        response = client.get('/ip_logging/')
        
        self.assertEqual(response.status_code, 200)
        mock_get_logger().info.assert_any_call('127.0.0.1') 

class RateLimitingTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='hamza@gmail.com', password='Riffat@1100')
        self.profile = Profile.objects.create(user=self.user, role=RoleChoice.GOLD.value, count=0, last_access_time=timezone.now())
    
        self.client = Client()
        self.client.login(email='hamza@gmail.com', password='Riffat@1100')
        
    def test_rate_limiting_gold_role(self):
        for _ in range(12): 
            response = self.client.get('/ip_logging/')
        self.assertEqual(response.status_code, 429)

    def test_rate_limiting_silver_role(self):
        self.profile.role = RoleChoice.SILVER.value
        self.profile.count = 0
        self.profile.save()
        for _ in range(7):
            response = self.client.get('/ip_logging/')
        self.assertEqual(response.status_code, 429)

    def test_rate_limiting_bronze_role(self):
        self.profile.role = RoleChoice.BRONZE.value
        self.profile.count = 0
        self.profile.save()
        for _ in range(3):
            response = self.client.get('/ip_logging/')
        self.assertEqual(response.status_code, 429)
        
class AccessControlTest(TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_access_control_unauthenticated(self):
        for _ in range(1):
            response = self.client.get('/ip_logging/')
        self.assertEqual(response.status_code, 429)

class SignupViewTest(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup') 

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html') 

    def test_signup_view_post_success(self):
        response = self.client.post(self.signup_url, {
            'email': 'khatija@gmail.com',
            'password1': 'Riffat@1100',
            'password2': 'Riffat@1100',
            'role' : 'silver'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(get_user_model().objects.filter(email='khatija@gmail.com').exists())

    def test_signup_view_post_failure(self):
        response = self.client.post(self.signup_url, {
            'email': 'khatija@gmail.com',
            'password1': 'Riffat@1100',
            'password2': 'Riffatjab@1100',
            'role' : 'silver'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter a correct email and password.', response.content.decode())


class LoginViewTest(TestCase):
    def setUp(self):
        self.email = 'wania@gmail.com'
        self.password = 'Riffat@1100'
        self.user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )
        self.login_url = reverse('login')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html') 

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {
            'email' : self.email,
            'password' : self.password
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_failure(self):
        response = self.client.post(self.login_url, {
            'email': self.email,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter a correct email and password.', response.content.decode())
