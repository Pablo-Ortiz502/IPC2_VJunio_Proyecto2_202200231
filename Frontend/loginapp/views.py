from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Aquí llamarías a tu API para verificar el login.
        if username == 'admin' and password == '1234':
            return HttpResponse("Login correcto")
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')