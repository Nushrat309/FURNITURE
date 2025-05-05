from django.shortcuts import render
def home(request):
    return render(request,'index.html')
    
def about(request):
    return render(request, 'about.html')
    
def blog(request):
    return render(request, 'blog.html')
    
def services(request):
    return render(request, 'services.html')
