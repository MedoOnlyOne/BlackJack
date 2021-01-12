import json
import os
from PIL import Image
from django.urls import reverse
from django.test import TestCase, Client
from .models import Product 
from users.models import User, Order, InCart, UserLogin
from shop.models import Shop
from users.models import User
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

BASE_DIR = Path(__file__).resolve().parent.parent

image_path = os.path.join(BASE_DIR,r'media\product_images\test.jpg')

class searchTestCase(TestCase):
    
    def setUp(self):
        #craete a product and add it to a shop
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")
        img = SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='other', image=img,shop=s)


    def test_product_page(self):
        # access product page
        p = Product.objects.get(name='testproduct')
        c = Client()
        response = c.get(reverse('productpage', kwargs={'productid':p.id}))
        self.assertEqual(response.status_code, 200)  #ValueError: The 'image' attribute has no file associated with it.