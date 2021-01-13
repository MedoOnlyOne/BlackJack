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

class IntegrationAndSystemTesting(TestCase):
    def setUp(self):
        #create a shop
        shop = Shop.objects.create(name="shop",description="sdadads",address="awd")

        #craete some coupons
        coupon = Coupon.objects.create(name='c1', code='kmsov', activated=True, coupon_type='shop' ,discount=30)
        #create a user
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        shopowner = User.objects.create(username='shopowner')
        shopowner.set_password('12345')
        shopowner.shop=shop
        shopowner.save()
        #Craete a product and add it to shop
        img = SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='other', image=img,shop=shop)

    def test_IntegrationTesting1(self):
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

    def test_IntegrationTesting2(self):
        #Add the shop to the user
        shop = Shop.objects.get(name="shop")
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

    def test_IntegrationTesting3(self):
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
    
    def test_IntegrationTesting4(self):
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

    def test_IntegrationTesting5(self):
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
        #Go to cart
        response3 = c.get(reverse('cart'))
        self.assertEqual(response3.status_code,200)
        #Choose the quntity of product in the cart and continue to checkout page
        response4 = c.post(reverse('create_transaction'),data={
            f'{product.id}_quantity':3,
            'coupon_code':'kmsov',
            'total':product.price*3
        })
        order=user.orders.all()[0]
        self.assertRedirects(response4, reverse('checkout',args=[order.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Go to checkout pgae to order the products
        response5 = c.post(reverse('finalcheck'),data={
            'order_id':order.id
        })
        self.assertRedirects(response5, reverse('userdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_SystenTesting(self):
        #Login the user in
        c = Client()
        c.login(username='testuser', password='12345')
        user = User.objects.get(username='testuser')
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
        
        response2= c.get(reverse('userdashboard'))
        self.assertContains(response2,'Test_First_Name',status_code=200)
        self.assertContains(response2,'Test_Last_Name',status_code=200)
        self.assertContains(response2,'+20',status_code=200)
        self.assertContains(response2,'1164892031',status_code=200)
        self.assertContains(response2,'Test@email.com',status_code=200)
        self.assertContains(response2,'Test Address',status_code=200)
        self.assertContains(response2,'EGP',status_code=200)

        #Search porduct
        response3 = c.get(reverse('search'),data={
            'search_name':'testproduct',
            'search_for':'products',
            'sort_by':'price'
        })
        self.assertContains(response3,'testproduct' ,status_code=200) 
        #visit product page
        product = Product.objects.get(name='testproduct')
        response4 = c.get(reverse('productpage',args=[product.id]))
        self.assertEqual(response4.status_code,200)
        #Add product to wishlist
        response5 = c.post(reverse('productpage', kwargs={'productid':product.id}),data={
            'add_to_wishlist':'',
            'productid':product.id
        })
        self.assertRedirects(response5, reverse('productpage',args=[product.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Addd product to cart
        c.login(username="testuser", password="12345")
        response6 = c.post(reverse('productpage',args=[product.id]),data={
            'add_to_cart':'',
            'productid':product.id
        })
        self.assertRedirects(response6, reverse('productpage',args=[product.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Get usre's wishlist and check if it contains the product
        response7 = c.get(reverse('wishlist'))
        self.assertContains(response7,'testproduct',status_code=200)
        #View user's cart and check if it contains the product    
        response8 = c.get(reverse('cart'))
        self.assertContains(response8,'testproduct',status_code=200)
        #Go to cart
        response9 = c.get(reverse('cart'))
        self.assertContains(response9,'testproduct',status_code=200)
        #Choose the quntity of product in the cart and continue to checkout page
        response10 = c.post(reverse('create_transaction'),data={
            f'{product.id}_quantity':3,
            'coupon_code':'',
            'total':product.price*3
        })
        order=user.orders.all()[0]
        self.assertRedirects(response10, reverse('checkout',args=[order.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Go to checkout pgae to order the products
        response11 = c.post(reverse('finalcheck'),data={
            'order_id':order.id
        })
        self.assertRedirects(response11, reverse('userdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Check if product is in order page
        response12 = c.get(reverse('orders'))
        self.assertContains(response12,'testproduct',status_code=200)
        #Create Shop
        response13 = c.post(reverse('create_shop'),data={
            'shopName':'Test Shop',
            'shopAddress' :'Testing City, Test',
            'shopDescription':'This a shop for testing only'
        })
        self.assertRedirects(response13, reverse('shopdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Add product
        response14 = c.post(reverse('addproduct'),data={
            'product':'Test Product',
            'cat' :'other',
            'price':100,
            'remaining_in_stock': 5,
            'discription': 'Test Product Discription',
            'image': SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        })
        self.assertRedirects(response14, reverse('shopdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #Edit product
        product = Product.objects.get(name="Test Product")
        response15 = c.post(reverse('editproduct', kwargs={'productid':product.id}),data={
            'product':'Edit Test Product',
            'cat' :'other',
            'price':1000,
            'remaining_in_stock': 2,
            'description': 'Edit Test Product Discription'
        })
        self.assertRedirects(response15, reverse('shopdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        #see if product is edited
        response16 = c.get(reverse('shopdashboard'))
        self.assertContains(response16,'Edit Test Product',status_code=200)
        #Add coupon
        response17 = c.post(reverse('addcoupon'),data={
            'name':'Test_____Coupon',
            'discount':15
        })
        self.assertEqual(response17.status_code,200)
        self.assertContains(response17,'Entered succesfully',status_code=200)
        #see if coupon is in activecoupons page
        response18 = c.get(reverse('activecoupons'))
        self.assertContains(response18,'Test_____Coupon',status_code=200)
        #Deactivate coupon
        coupon = Coupon.objects.get(name='Test_____Coupon')
        response19 = c.get(reverse('deactivatecoupon',kwargs={'couponcode':coupon.code}))
        self.assertRedirects(response19, reverse('activecoupons'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        # check if coupon is deactivated
        response20 = c.get(reverse('activecoupons'))
        self.assertNotContains(response20,'Test_____Coupon',status_code=200)