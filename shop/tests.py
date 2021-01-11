from django.test import TestCase, Client
from .models import Shop, Coupon
from products.models import Product
from users.models import User
# Create your tests here.

class searchTestCase(TestCase):
    
    def setUp(self):
        #create some shops
        s = Shop.objects.create(name="ssss",description="sdadads",address="awd")
        a = Shop.objects.create(name="aaaa",description="sdadads",address="awd")
        b = Shop.objects.create(name="bbbb",description="sdadads",address="awd")
        ab = Shop.objects.create(name="abab",description="sdadads",address="awd")

        #craete a coupone
        coupone = Coupon.objects.create(name='c1', code='ab2d3', activated=True, discount=30)

        #create a user
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

    def test_shop_get(self):
        # here we try to access the index page of each shop
        c = Client()
        shops = list(Shop.objects.all())
        for shop in shops:
            # print(f"###########     {shop.name}   #########")
            response = c.get(f"/shop/{shop.name}/")
            self.assertEqual(response.status_code, 200)

    def test_add_coupon(self):
        #login and access add coupone page
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get("/shop/addcoupon/")
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        #login and access add coupone page
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get("/shop/addproduct/")
        self.assertEqual(response.status_code, 200)

    def test_deactivate_coupone(self):
        #login and access deactivate coupone page
        
        #add coupone to a shop
        shop = Shop.objects.get(name='ssss')
        shop.coupons.add(Coupon.objects.get(name='c1'))
        shop.save()
        #add that shop to the user
        u = User.objects.get(username='testuser')
        u.shop = shop
        u.save()
        #login the user
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get(f"/shop/deactivatecoupon/{list(Coupon.objects.all())[0].id}")
        self.assertEqual(response.status_code, 200)

    