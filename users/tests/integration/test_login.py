from utils.tests import APITestCase, mixer
from users.models import User
from django.urls import reverse
from utils import UserRoleChoices

class LoginTestCase(APITestCase):

    def setUp(self):
        self.loginUrl = reverse("users:user_login")

    def test_method_not_allowed(self):
        response = self.client.get(self.loginUrl)
        self.assertEqual(response.status_code, 405)

    def test_invalid_data(self):
        response = self.client.post(self.loginUrl)
        data = {
                "username": [
                    "This field is required."
                ],
                "password": [
                    "This field is required."
                ]
            }
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), data)

    def test_wrong_cred(self):
        # Init User
        user = User.objects.create(username="admin")
        user.set_password("password")
        user.save()

        data = {
                "username": "admin",
                "password": "Wrongpassword"
            }
        response = self.client.post(self.loginUrl, data=data)

        result = {
                "error": [
                    "Invalid Username or Password"
                ]
            }
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), result)

    def test_success_login(self):
        # Init User
        user = User.objects.create(username="admin", role=UserRoleChoices.BUYER)
        user.set_password("password")
        user.save()
        data = {
                "username": "admin",
                "password": "password"
            }
        response = self.client.post(self.loginUrl, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_id'], user.id)
        self.assertEqual(response.json()['role'], "Buyer")