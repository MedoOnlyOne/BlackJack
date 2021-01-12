import json
import os
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
from django.urls import reverse
from django.test import TestCase, Client
from users.models import User, Order, InCart, UserLogin
from products.models import Product
from shop.models import Shop,Coupon
# Create your tests here.

BASE_DIR = Path(__file__).resolve().parent.parent

image_path = os.path.join(BASE_DIR,r'media\product_images\test.jpg')

class IntegrationTest(TestCase):
    def setUp(self):
        #create some shops
        shop1 = Shop.objects.create(name="shop1",description="sdadads",address="awd")
        shop2 = Shop.objects.create(name="shop2",description="sdadads",address="awd")
        shop3 = Shop.objects.create(name="shop3",description="sdadads",address="awd")
        shop4 = Shop.objects.create(name="shop4",description="sdadads",address="awd")

        #craete some coupons
        coupon1 = Coupon.objects.create(name='c1', code='kmsov', activated=True, discount=30)
        coupon2 = Coupon.objects.create(name='c2', code='dgdgq', activated=True, discount=30)
        #create a user
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        shopowner = User.objects.create(username='shopowner')
        shopowner.set_password('12345')
        shopowner.shop=shop1
        shopowner.save()
        #Craete a product and add it to shop1
        img = SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='other', image=img,shop=shop1)

    def test_scenario1(self):
        #Log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        #Create Shop
        response1 = c.post(reverse('create_shop'),data={
            'shopName':'Test Shop',
            'shopAddress' :'Testing City, Test',
            'shopDescription':'This a shop for testing only'
        })
        self.assertRedirects(response1, reverse('shopdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Add product
        response2 = c.post(reverse('addproduct'),data={
            'product':'Test Product',
            'cat' :'other',
            'price':100,
            'remaining_in_stock': 5,
            'discription': 'Test Product Discription',
            'image': SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        })
        self.assertRedirects(response2, reverse('shopdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Edit product
        product = Product.objects.get(name="Test Product")
        response3 = c.post(reverse('editproduct', kwargs={'productid':product.id}),data={
            'product':'Edit Test Product',
            'cat' :'other',
            'price':1000,
            'remaining_in_stock': 2,
            'description': 'Edit Test Product Discription'
        })
        self.assertRedirects(response3, reverse('shopdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

    def test_scenario2(self):
        #Add the shop to the user
        shop = Shop.objects.get(name="shop1")
        user = User.objects.get(username="testuser")
        user.shop = shop
        user.save()
        #Log the user in
        c = Client()
        c.login(username="testuser", password="12345")
        #Add coupon
        response1 = c.post(reverse('addcoupon'),data={
            'name':'Test_____Coupon',
            'discount':15
        })
        self.assertEqual(response1.status_code,200)
        #Deactivate coupon
        coupon = Coupon.objects.get(name='Test_____Coupon')
        response2 = c.get(reverse('deactivatecoupon',kwargs={'couponcode':coupon.code}))
        self.assertRedirects(response2, reverse('activecoupons'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

    def test_scenario3(self):
        #Log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        #Edit user info
        response1 = c.post(reverse('userdashboard'),data={
            'first':'Test_First_Name',
            'last' :'Test_Last_Name',
            'code':'+20',
            'num': '1164892031',
            'email':'Test@email.com',
            'address':'Test Address',
            'currency':'EGP'
        })
        self.assertRedirects(response1, reverse('userdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Visit product page
        product = Product.objects.get(name="testproduct")
        response2 = c.get(reverse('productpage', kwargs={'productid':product.id}))
        self.assertEqual(response2.status_code, 200)
        #Add product to wishlist
        response3 = c.post(reverse('productpage', kwargs={'productid':product.id}),data={
            'add_to_wishlist':'',
            'productid':product.id
        })
        self.assertRedirects(response3, reverse('productpage',args=[product.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)    
        #Get usre's wishlist
        response4 = c.get(reverse('wishlist'))
        self.assertContains(response4,'testproduct',status_code=200)
    
    def test_scenario4(self):
        c = Client()
        #Search porduct
        response1 = c.get(reverse('search'),data={
            'search_name':'testproduct',
            'search_for':'products',
            'sort_by':'price'
        })
        self.assertContains(response1,'testproduct' ,status_code=200) 
        #visit product page
        product = Product.objects.get(name='testproduct')
        response2 = c.get(reverse('productpage',args=[product.id]))
        self.assertEqual(response2.status_code,200)
        #Addd product to cart
        c.login(username="testuser", password="12345")
        response3 = c.post(reverse('productpage',args=[product.id]),data={
            'add_to_cart':'',
            'productid':product.id
        })
        self.assertRedirects(response3, reverse('productpage',args=[product.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #View the cart and check if it contains the product    
        response4 = c.get(reverse('cart'))
        self.assertContains(response4,'testproduct',status_code=200)

    def test_scenario5(self):
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        user = User.objects.get(username='testuser')
        #go to product page
        product = Product.objects.get(name='testproduct')
        response1 = c.get(reverse('productpage',args=[product.id]))
        self.assertEqual(response1.status_code,200)
        #add to cart
        response2 = c.post(reverse('productpage',args=[product.id]),data={
            'add_to_cart':'',
            'productid':product.id
        })
        self.assertRedirects(response2, reverse('productpage',args=[product.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #go to cart
        response3 = c.get(reverse('cart'))
        self.assertEqual(response3.status_code,200)
        response4 = c.post(reverse('create_transaction'),data={
            f'{product.id}_quantity':3,
            'coupon_code':'',
            'total':product.price*3
        })
        order=user.orders.all()[0]
        self.assertRedirects(response4, reverse('checkout',args=[order.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        response5 = c.post(reverse('finalcheck'),data={
            'order_id':order.id
        })
        self.assertRedirects(response5, reverse('userdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)