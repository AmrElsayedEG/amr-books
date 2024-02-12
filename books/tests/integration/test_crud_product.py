from utils.tests import APITestCase, mixer
from users.models import User
from django.urls import reverse
from utils import UserRoleChoices
from books.models import Product

class CRUDProductTestCase(APITestCase):

    def setUp(self):
        self.sellerUser = mixer.blend(User, role=UserRoleChoices.SELLER)
        self.product = mixer.blend(Product, seller = self.sellerUser)
        self.url = reverse("products:crud_product", kwargs={'pk' : self.product.id})
        self.buyerUser = mixer.blend(User, role=UserRoleChoices.BUYER)
        self.sellerUserTwo = mixer.blend(User, role=UserRoleChoices.SELLER)
        self.wrongProduct = reverse("products:crud_product", kwargs={'pk' : 1000000})

    def test_not_logged_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_create_product(self):
        self.client.force_authenticate(self.buyerUser)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_not_found_product(self):
        self.client.force_authenticate(self.buyerUser)
        response = self.client.get(self.wrongProduct)
        exp_response = {
                    "detail": "Not found."
                }
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), exp_response)

    def test_get_one_product(self):
        self.client.force_authenticate(self.buyerUser)
        response = self.client.get(self.url)
        exp_response = {
                        "id": self.product.id,
                        "product_name": self.product.product_name,
                        "cost": self.product.cost,
                        "amount_available": self.product.amount_available
                    }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), exp_response)

    def test_update_one_product_another_seller(self):
        self.client.force_authenticate(self.sellerUserTwo)
        data = {
            "product_name" : "New"
        }
        response = self.client.patch(self.url, data=data)
        exp_response = {
                    "error": "You are not the seller of this product"
                }
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), exp_response)

    def test_update_one_product_success(self):
        self.client.force_authenticate(self.sellerUser)
        data = {
            "product_name" : "New"
        }
        response = self.client.patch(self.url, data=data)
        exp_response = {
                    "id": self.product.id,
                    "product_name": "New",
                    "cost": self.product.cost,
                    "amount_available": self.product.amount_available
                }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), exp_response)

    def test_delete_one_product_another_seller(self):
        self.client.force_authenticate(self.sellerUserTwo)
        response = self.client.delete(self.url)
        exp_response = {
                    "error": "You are not the seller of this product"
                }
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), exp_response)

    def test_update_one_product_success(self):
        self.client.force_authenticate(self.sellerUser)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)