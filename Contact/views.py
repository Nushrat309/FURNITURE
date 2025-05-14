from django.shortcuts import render,redirect
from . models import Contact

# Create your views here.

def contact(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            message = message,
        )
        return render(request,'contact.html',{"success":True})
    return render(request,'contact.html')
