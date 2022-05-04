from turtle import end_fill
from django.shortcuts import render

# Create your views here.
def home (request):
    return render(request, 'home.html')

def input (request):
    return render(request, 'input.html')