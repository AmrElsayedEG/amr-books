from utils.tests import APITestCase, mixer
from users.models import User
from django.urls import reverse
from utils import UserRoleChoices
from books.models import Product
import json

class BuyProductsTestCase(APITestCase):

    def setUp(self):
        self.sellerUser = mixer.blend(User, role=UserRoleChoices.SELLER)
        self.product = mixer.blend(Product, seller = self.sellerUser, amount_available=1, cost=30)
        self.url = reverse("products:buy_product")
        self.buyerUser = mixer.blend(User, role=UserRoleChoices.BUYER, deposit=20.0)

    def test_not_logged_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_buy_products(self):
        self.client.force_authenticate(self.sellerUser)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_buy_product_insufficient_amount(self):
        self.client.force_authenticate(self.buyerUser)
        data = {
                "products" : [
                        {
                        "product_id" : self.product.id,
                        "amount" : 2
                        }
                    ]
            }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Insufficient Amount: Please select a lower amount" in str(response.json()), True)

    def test_buy_product_insufficient_balance(self):
        self.client.force_authenticate(self.buyerUser)
        data = {
                "products" : [
                        {
                        "product_id" : self.product.id,
                        "amount" : 1
                        }
                    ]
            }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Insufficient Balance: Please Deposit more money or choose a lower amount" in str(response.json()), True)

    def test_buy_product_insufficient_balance(self):
        self.client.force_authenticate(self.buyerUser)
        self.product.cost = 10
        self.product.save()
        data = {
                "products" : [
                        {
                        "product_id" : self.product.id,
                        "amount" : 1
                        }
                    ]
            }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.product.refresh_from_db()
        exp_response = {
                "total_amount": 10,
                "purchased_products": [
                    {
                        "id": self.product.id,
                        "product_name": self.product.product_name,
                        "cost": self.product.cost,
                        "amount_available": self.product.amount_available
                    }
                ],
                "balance": float(10)
            }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), exp_response)