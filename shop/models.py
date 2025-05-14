from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    image = models.ImageField(upload_to='Shop/media/uploads')
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.title
    


class Cart(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'Cart of {self.user.username}' 
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f'{self.product.title}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    billing_address = models.CharField(max_length=250)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=54)
    phone = models.CharField(max_length=15,default = '+8801')
    note = models.TextField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)


    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'Order of {self.user.username}' 
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price

    
    
    def __str__(self):
        return f'{self.product.title}'
    