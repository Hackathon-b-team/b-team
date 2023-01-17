from django.shortcuts import render

def loginfunc(request):
    return render(request, 'login.html')
