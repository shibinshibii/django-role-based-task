from django.test import TestCase
from .models import CustomUser, Role
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your tests here.


# class CustomUserTest(TestCase):
#     def setUp(self):
#         self.role = Role.objects.create(id=1,name="Project Coordinator")
#     def test_create_user(self):
#         user = CustomUser.objects.create_user(
#             username="c4", password="123", email="pitijoy528@obirah.com", role=self.role)
#         self.assertEqual(user.username, "c4")
#         self.assertEqual(user.email, "pitijoy528@obirah.com")
#         self.assertTrue(user.check_password("123"))

class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Employee")
        self.user = CustomUser.objects.create_user(
            username="testuser", password="oldpass123", email="testemail@.com", role=self.role)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("change-password")

    def test_change_password_success(self):
        data = {
            "oldPassword": "oldpass123",
            "newPassword": "newpass456",
            "confirmPassword": "newpass456"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass456"))

    def test_change_password_wrong_old(self):
        data = {
            "oldPassword": "wrongpass",
            "newPassword": "newpass456",
            "confirmPassword": "newpass456"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("oldpass123"))


class ForgotAndResetPasswordViewTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Employee")
        self.user = CustomUser.objects.create_user(
            username="testuser", password="test123", email="test@email.com", role=self.role)

        self.client = APIClient()
        self.forgot_url = reverse('forgot-password')
        self.reset_url = reverse('reset-password')

    @patch("core.views.send_mail")
    def test_forgot_password_valid_email(self, mock_send_mail):
        data = {"email": "test@email.com"}
        response = self.client.post(self.forgot_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Password reset link sent to email",
                      response.json()["detail"])
        mock_send_mail.assert_called_once()

    def test_forgot_password_invalid_mail(self):
        data = {"email": "invalid@mail.com"}
        response = self.client.post(self.forgot_url, data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("No user with this email", response.json()["detail"])

    def test_reset_password_success(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = PasswordResetTokenGenerator().make_token(self.user)
        data = {"uid": uid,
                "token": token,
                "newPassword": "newpass123",
                "confirmPassword": "newpass123"}
        response = self.client.post(self.reset_url, data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass123"))

    def test_reset_password_fail(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = PasswordResetTokenGenerator().make_token(self.user)
        data = {"uid": uid,
                "token": token,
                "newPassword": "newpass123",
                "confirmPassword": "wrongpass"}
        response = self.client.post(self.reset_url,data)
        self.assertIn("The passwords do not match", response.json()["detail"])

    def test_reset_password_wrong_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        data = {"uid":uid,
                "token":"wrongtoken",
                "newPassword":"newpass123",
                "confirmPassword":"newpass123"}
        response = self.client.post(self.reset_url, data)
        self.assertIn("Invalid or expired token", response.json()["detail"])
