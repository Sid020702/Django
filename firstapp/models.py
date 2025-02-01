from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import CustomUserManager
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _



class CustomUser(AbstractUser):
    username = None
    email=models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length = 255)
    price = models.FloatField()

    def __str__(self):
        return self.product_name
    
    @classmethod
    def updateprice(cls, product_id,  price):
        product = cls.objects.filter(product_id = product_id)
        product=product.first()
        product.price = price
        product.save()
        return product
    
    @classmethod
    def create(cls,product_name, price):
        product = Product(product_name = product_name, price=price)
        product.save()
        return product

class CartManager(models.Manager):
    def create_cart(self,user):
        cart=self.create(user = user)
        return cart


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on=models.DateTimeField(default=timezone.now)

    objects = CartManager()



class ProductInCart(models.Model):
    class Meta:
        unique_together = (('cart','product'))
    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    status_choices={
        (1,'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=status_choices, default=1)

class Deal(models.Model):
    user = models.ManyToManyField(User)
    deal_name = models.CharField(max_length=255)
# Create your models here.