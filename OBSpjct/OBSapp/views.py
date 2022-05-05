import re
from turtle import end_fill
from django.shortcuts import redirect, render

# Create your views here.
def home (request):
    return render(request, 'home.html')

def input (request):
    return render(request, 'input.html')

def get_options(request):
    ifsame = request.POST.get('ifsame')
    Destination = request.POST.get('Destination')
    Starting_Point = request.POST.get('Starting_Point')
    Max_Length = request.POST.get('Max_Length')

    if ifsame == '1':
        Destination = Starting_Point
    
    if str(Max_Length).strip() == "" :
        Max_Length = 100000

    if str(Destination).strip() == "" :
        return redirect ('input')
    if str(Starting_Point).strip() == "" :
        return redirect ('input')
    
    return render(request, 'show_options.html', {})

def end(request):
    return render (request, 'end.html')