from urllib import response
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
        
        request.session["code"] = code #str

        if response.status_code == 200:# login exitoso
            data = response.json()
            user = data.get("user")
            request.session["user"] = int(user)
            return redirect("homeAdmin")  # Redirige a admin
        else:
            error = "Credenciales inválidas"

    return render(request, "login.html", {"error": error})


#---------------------------------admin----------------------------------------------
def home_view(request):
    user = request.session.get("user")
    print("la variable golbal user es:",user)
    
    if user == 1:
        response = requests.post("http://localhost:5000/getAd")
        if response.status_code == 200:
            data = response.json()
            name = data.get("name")
            return render(request, "home.html", {"name": name})
        
        
        
    return JsonResponse({"error": "Tipo de usuario no válido"})


def upload_xml_view(request):
    xmlContent = ""
    apiRes = None

    if request.method == 'POST' and 'xml_file' in request.FILES:
        xmlFile = request.FILES['xml_file']
        name =""
        code = 0
        try:
            xmlContent = xmlFile.read().decode('utf-8')

           
            response = requests.post('http://localhost:5000/settXML',  
                data=xmlContent,
                headers={'Content-Type': 'application/xml'}
            )
            res = response.json()
            print(res)
            
            response2 = requests.post("http://localhost:5000/getXML")

            apiResponse = response2.json()
            apiRes = apiResponse.get("res")
            
            response3 = requests.post("http://localhost:5000/getAd")
            if response3.status_code == 200:
                data = response3.json()
                name = data.get("name")
                code = data.get("carnet")

        except UnicodeDecodeError:
            xmlContent = 'Error al leer el archivo. Asegúrate de que esté en UTF-8.'
        except requests.RequestException as e:
            apiRes = f'Error al conectar con la API: {str(e)}'
        return render(request, 'home.html', {'xmlContent': xmlContent,'apiRes': apiRes,"name": name, "code": int(code)})
    
    return render(request, 'home.html', {'xmlContent': "error",'apiRes': "error"})


def users_view(request):    
    
    name =""
    code =0
    data =[]
    
    if request.method == 'POST':
        response = requests.post("http://localhost:5000/getUs")
        if response.status_code == 200:
            data = response.json()
    
    
        response2 = requests.post("http://localhost:5000/getAd")
        if response2.status_code == 200:
            data2 = response2.json()
            name = data2.get("name")
            code = data2.get("carnet")

    return render(request,"home.html",{"data": data,"name": name, "code": int(code)})


def yo_view(request):
    name =""
    code =0
    
    if request.method == 'POST':
        response = requests.post("http://localhost:5000/getAd")
        if response.status_code == 200:
            data2 = response.json()
            name = data2.get("name")
            code = data2.get("carnet")
    return render(request,"home.html",{"yo": True,"name": name, "code": int(code)})
      
        
        
        


def test_view(request):
    return render(request,"home.html")