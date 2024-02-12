from utils.tests import APITestCase, mixer
from users.models import User
from django.urls import reverse
from utils import UserRoleChoices

class RegisterTestCase(APITestCase):

    def setUp(self):
        self.registerUrl = reverse("users:user_register")

    def test_method_not_allowed(self):
        response = self.client.get(self.registerUrl)
        self.assertEqual(response.status_code, 405)

    def test_invalid_data(self):
        response = self.client.post(self.registerUrl)
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

    def test_existing_username(self):
        user = User.objects.create(username="admin")
        data = {
                "username": "admin",
                "password": "anyPassword"
            }
        response = self.client.post(self.registerUrl, data=data)
        result = {
                "username": [
                    "A user with that username already exists."
                ]
            }
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), result)

    def test_success_register(self):
        data = {
                "username": "Newadmin",
                "password": "anyPassword",
                "role" : UserRoleChoices.SELLER
            }
        response = self.client.post(self.registerUrl, data=data)
        result = {
                    "success": "User has been created"
                }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), result)