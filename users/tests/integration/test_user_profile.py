from utils.tests import APITestCase, mixer
from users.models import User
from django.urls import reverse
from utils import UserRoleChoices

class UserProfileUpdateTestCase(APITestCase):

    def setUp(self):
        self.profileUrl = reverse("users:get_update_profile")
        self.changePasswordUrl = reverse("users:change_password")
        self.user = mixer.blend(User, role=UserRoleChoices.BUYER)

    def test_unauthorized(self):
        response = self.client.post(self.profileUrl)
        self.assertEqual(response.status_code, 401)

    def test_method_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.profileUrl)
        self.assertEqual(response.status_code, 405)

    def test_retrieve_profile(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.profileUrl)
        exp_result = {
            "username": self.user.username,
            "role": UserRoleChoices.BUYER
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), exp_result)

    def test_update_profile(self):
        self.client.force_authenticate(self.user)
        data = {
            "username" : "NewUsername"
        }
        response = self.client.patch(self.profileUrl, data=data)
        exp_result = {
            "username": "NewUsername",
            "role": UserRoleChoices.BUYER
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), exp_result)

    def test_update_profile(self):
        self.client.force_authenticate(self.user)
        data = {
            "password" : "NewPassword"
        }
        response = self.client.patch(self.changePasswordUrl, data=data)
        exp_result = {
                    "success": "Password changed successfully"
                }
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), exp_result)
        self.assertEqual(self.user.check_password("NewPassword"), True)
        