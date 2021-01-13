import json
import os
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
from django.urls import reverse
from django.test import TestCase, Client
from .models import User, Order, InCart, UserLogin
from products.models import Product
from shop.models import Shop
from users.models import User
# Create your tests here.

BASE_DIR = Path(__file__).resolve().parent.parent

image_path = os.path.join(BASE_DIR,r'media\product_images\test.jpg')

class searchTestCase(TestCase):
    
    def setUp(self):
        #create a user
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()


    def test_home(self):
        # access home page
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_check_out(self):
        # access the checkout page
        
        # Create a shop
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")

        #craete a product and add it to shop s
        s = Shop.objects.get(name='ssss')
        img = SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='other', image=img,shop=s)

        #create incart object
        incart = InCart.objects.create(product=p, quantity=2)
        #create order
        order = Order.objects.create()
        order.products.add(incart)
        order.save()
        #add the order to the user
        u = User.objects.get(username='testuser')
        u.orders.add(order)
        u.save()
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('checkout', kwargs={'orderid':order.id}))
        self.assertEqual(response.status_code, 200)

    def test_log_in(self):
        # access login page
        c = Client()
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_log_out(self):
        # access logout page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
    def test_sign_up(self):
        # access signup page
        c = Client()
        response = c.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        # access change password page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('changepassword'))
        self.assertEqual(response.status_code, 200)

    def test_create_shop(self):
        # access craete shop page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('create_shop'))
        self.assertEqual(response.status_code, 200)

    def test_wishlist(self):
        # access wishlist page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)

    def test_cart(self):
        # access cart page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)


    def test_orders(self):
        # access orders page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)

    def test_create_transaction(self):
        # Create a shop
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")

        #craete a product and add it to shop s
        s = Shop.objects.get(name='ssss')
        img = SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='other', image=img,shop=s)

        # #create incart object
        u = User.objects.get(username='testuser')
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.post(reverse('create_transaction'),data={'{p.id}_quantity':2,'total':p.price*2})
        order=u.orders.all()[0]
        self.assertRedirects(response, reverse('checkout',args=[order.id]), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)    
    
    def test_final_check(self):
        # access final check page

        # Create a shop
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")

        #craete a product and add it to shop s
        s = Shop.objects.get(name='ssss')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='Other', shop=s)

        #create incart object
        incart = InCart.objects.create(product=p, quantity=2)
        #create order
        order = Order.objects.create()
        order.products.add(incart)
        order.save()
        #add the order to the user
        u = User.objects.get(username='testuser')
        u.orders.add(order)
        u.save()
        # give the shop to the user
        u.shop = s
        u.save()
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        data = {
          "order_id": order.id,
        }
        response = c.post(reverse('finalcheck'),data=data)
        self.assertRedirects(response, reverse('userdashboard'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)    
    def test_contact_us(self):
        # access contact us page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('contactus'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        # access dashboard page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('userdashboard'))
        self.assertEqual(response.status_code, 200)


    def test_remove_from_cart(self):
        # access remove from cart

        # Create a shop
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")

        #craete a product and add it to shop s
        s = Shop.objects.get(name='ssss')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='Other', shop=s)
        #add product to user's cart
        u = User.objects.get(username='testuser')
        u.cart.add(p)
        u.save()
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('removefromcart', kwargs={'productid':p.id}))
        self.assertRedirects(response, reverse('cart'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
    def test_remove_from_wishlist(self):
        # access remove from wishlist

        # Create a shop
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")

        #craete a product and add it to shop s
        s = Shop.objects.get(name='ssss')
        p = Product.objects.create(name='testproduct',price=100,description='aaafvdfvscd', remaininginstock=5, category='Other', shop=s)
        #add product to user's wishlist
        u = User.objects.get(username='testuser')
        u.wishlist.add(p)
        u.save()
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('removefromwishlist', kwargs={'productid':p.id})) 
        self.assertRedirects(response, reverse('wishlist'), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)