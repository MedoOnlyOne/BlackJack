import json
import os
from PIL import Image
from django.urls import reverse
from django.test import TestCase, Client
from users.models import User, Order, InCart, UserLogin
from shop.models import Shop
from products.models import Product
from users.models import User
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

BASE_DIR = Path(__file__).resolve().parent.parent

image_path = os.path.join(BASE_DIR,r'media\product_images\test.jpg')

class searchTestCase(TestCase):
    
    def setUp(self):
        #craete a product and add it to a shop
        shop1  = Shop.objects.create(name="ssss",description="sdadads",address="awd")
        shop2 = Shop.objects.create(name="eyewear shop",description="sdadads",address="awd")
        img = SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        product1 = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='other', image=img,shop=shop1)
        product2 = Product.objects.create(name='Red Jacket',price=100,description='aaafvdfvscd', remaininginstock=5, category='other', image=img,shop=shop2)
    def test_search_products(self):
        c = Client()
        response = c.get(reverse('search'),data={
            'search_name':'Jacket',
            'search_for':'products',
            'sort_by':'price'
        })
        self.assertContains(response,'Red Jacket' ,status_code=200) 
    
    def test_search_shops(self):
        c = Client()
        response = c.get(reverse('search'),data={
            'search_name':'Eyewear',
            'search_for':'shops'
        })
        self.assertContains(response,'eyewear shop' ,status_code=200) 
        