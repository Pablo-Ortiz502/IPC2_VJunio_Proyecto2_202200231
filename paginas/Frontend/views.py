from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests

def login_view(request):
    error = None
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    if request.method == "POST":
        code = (request.POST.get("username"))
        password = request.POST.get("password")

        response = requests.post("http://localhost:5000/login", json={
            "code": code,
            "password": password
        })
        print("hola muuuuuuuuuuuuuuuuuuundo")

        if response.status_code == 200:# login exitoso
            
            request.session["code"] = code #codigo de tutor o estudiante
            return redirect("homeAdmin")  # Redirige a admin
        else:
            error = "Credenciales inválidas"

    return render(request, "login.html", {"error": error})

def home_view(request):

    response = requests.post("http://localhost:5000/getAd")
  

    if response.status_code == 200:
        data = response.json()
        name = data.get("name")
        code = data.get("carnet")
        
        return render(request, "home.html", {"name": name, "code": code})
        
        
    return JsonResponse({"error": "Tipo de usuario no válido"})



def test_view(request):
    return render(request,"home.html")