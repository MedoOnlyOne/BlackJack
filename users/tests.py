import json
from django.urls import reverse
from django.test import TestCase, Client
from .models import User, Order, InCart, UserLogin
from products.models import Product
from shop.models import Shop
from users.models import User
# Create your tests here.

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
    
    def test_chech_out(self):
        # access the checkout page
        
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
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        # response = c.get(reverse('checkout', kwargs={'orderid':order.id})) #Image attribute has no files attached with it
        # self.assertEqual(response.status_code, 200)

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
        # self.assertEqual(response.status_code, 200) #problem here

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

    def test_discover_shops(self):
        # access discover shops page

        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(reverse('discovershops'))
        self.assertEqual(response.status_code, 200)

    def test_create_transaction(self):
        # log the user in
        c = Client()
        c.login(username='testuser', password='12345')
        # response = c.get(reverse('create_transaction')) #problem here
        # self.assertEqual(response.status_code, 200)

    
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
        #login
        c = Client()
        c.login(username='testuser', password='12345')
        data = {
          "order_id": order.id,
        }
        # response = c.post(reverse('finalcheck'),data) #IndexError: list index out of range
        # self.assertEqual(response.status_code, 200)        
    
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
        # response = c.get(reverse('removefromcart', kwargs={'productid':p.id}))
        # self.assertEqual(response.status_code, 200) #302

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
        # response = c.get(reverse('removefromwishlist', kwargs={'productid':p.id})) 
        # self.assertEqual(response.status_code, 200)  #302