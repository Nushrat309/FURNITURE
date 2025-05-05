from django.shortcuts import render
from shop.models import Product

# Create your views here.
def shop(request):
    data=Product.objects.all()
    return render(request,'shop.html',{'data':data})
