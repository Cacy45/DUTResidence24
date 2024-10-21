from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')  # Render the home.html template

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')
