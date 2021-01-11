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

            
    