from django.db import models

# Create your models here.
class Product(models.Model):
  images=models.ImageField(upload_to='Shop/media/uploads')
  title=models.CharField(max_length=50)
  price=models.DecimalField(max_digits=50, decimal_places=3)
