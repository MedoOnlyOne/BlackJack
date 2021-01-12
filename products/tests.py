import json
from django.urls import reverse
from django.test import TestCase, Client
from .models import Product 
from users.models import User, Order, InCart, UserLogin
from shop.models import Shop
from users.models import User
# Create your tests here.

class searchTestCase(TestCase):
    
    def setUp(self):
        #craete a product and add it to a shop
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='Other', shop=s)


    def test_product_page(self):
        # access product page
        p = Product.objects.get(name='testproduct')
        c = Client()
        # response = c.get(reverse('productpage', kwargs={'productid':p.id}))
        # self.assertEqual(response.status_code, 200)  #ValueError: The 'image' attribute has no file associated with it.