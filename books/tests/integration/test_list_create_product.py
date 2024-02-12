from utils.tests import APITestCase, mixer
from users.models import User
from django.urls import reverse
from utils import UserRoleChoices
from books.models import Product

class ListCreateProductsTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("products:get_create_products")
        self.buyerUser = mixer.blend(User, role=UserRoleChoices.BUYER)
        self.sellerUser = mixer.blend(User, role=UserRoleChoices.SELLER)
        self.product = mixer.blend(Product)

    def test_not_logged_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_create_product(self):
        self.client.force_authenticate(self.buyerUser) 
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_method_not_allowed(self):
        self.client.force_authenticate(self.sellerUser)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 405)

    def test_list_all_products(self):
        self.client.force_authenticate(self.buyerUser)
        response = self.client.get(self.url)
        exp_response = {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.product.id,
                        "product_name": self.product.product_name,
                        "cost": self.product.cost,
                        "amount_available": self.product.amount_available
                    }
                ]
            }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), exp_response)

    def test_create_product(self):
        self.client.force_authenticate(self.sellerUser)
        data = {
                "product_name" : "Spiro",
                "cost" : 20,
                "amount_available" : 150
            }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)