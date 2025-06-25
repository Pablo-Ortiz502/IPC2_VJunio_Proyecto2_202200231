from urllib import response
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os
from django.conf import settings
import plotly.graph_objects as go



def login_view(request):
    error = None
    if request.method == "POST":
        code = (request.POST.get("username"))
        password = request.POST.get("password")

        response = requests.post("http://localhost:5000/login", json={
            "code": code,
            "password": password
        })
        
        request.session["code"] = code #str

        if response.status_code == 200:# login exitoso
            data = response.json()
            user = data.get("user")
            request.session["user"] = int(user)
            return redirect("homeAdmin")  # Redirige a admin
        else:
            error = "Credenciales inválidas"
    
            

    return render(request, "login.html", {"error": error})


#---------------------------------homes----------------------------------------------
def home_view(request):
    user = request.session.get("user")
    print("la variable golbal user es:",user)
    
    if user == 1:
        response = requests.post("http://localhost:5000/getAd")
        if response.status_code == 200:
            data = response.json()
            name = data.get("name")
            return render(request, "home.html", {"name": name})
    if user == 3:
        
        t = [""]
        c = request.session.get("code")
        response2 = requests.post("http://localhost:5000/getStu", json={
            "code": c
            })
        
        response = requests.post("http://localhost:5000/getTimeXML")
        data3 = response.json()
        
        if response2.status_code == 200:
            data = response2.json()
            user = data.get("user")
            name = user.get("name")  
            return render(request, 'tutor.html', {'data': data3,"name": name})
        
    return JsonResponse({"error": "Tipo de usuario no válido"})

#---------------------------------admin----------------------------------------------
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
            xmlContent = 'Error al leer el archivo'
            
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


#-------------------------------------------Tutor---------------------------------------------------------------      
        
def time_view(request):
    xmlContent = ""
    data3 =[]
    c = request.session.get("code")
        
    if request.method == 'POST' and 'xml_file' in request.FILES:
        xmlFile = request.FILES['xml_file']
        name =""
        try:
            xmlContent = xmlFile.read().decode('utf-8')
           
            response = requests.post('http://localhost:5000/timeXML',  
                data=xmlContent,
                headers={'Content-Type': 'application/xml'}
            )
            response = requests.post("http://localhost:5000/getTimeXML")
            data3 = response.json()
            
            response2 = requests.post("http://localhost:5000/getStu", json={
            "code": c
            })
            
            if response2.status_code == 200:
                data2 = response2.json()
                user = data2.get("user")
                name = user.get("name")

        except UnicodeDecodeError:
            xmlContent = 'Error al leer el archivo'
        print(data3)    
        return render(request, 'tutor.html', {'data': data3,"name": name})
    
    return render(request, 'tutor.html')



def notes_view(request):
    c = request.session.get("code")
    name = ""
    
    response2 = requests.post("http://localhost:5000/getStu", json={
            "code": c
    })
            
    if response2.status_code == 200:
        data2 = response2.json()
        user = data2.get("user")
        name = user.get("name")
    
     
    if request.method == 'POST' and 'xml_file' in request.FILES:
        xmlFile = request.FILES['xml_file']
        data="no ufnciono"
        try:
            xmlContent = xmlFile.read().decode('utf-8')
           
            response = requests.post('http://localhost:5000/setNotes',  
                data=xmlContent,
                headers={'Content-Type': 'application/xml'}
            )
            data = response.json()
            

        except UnicodeDecodeError:
            xmlContent = 'Error al leer el archivo'         

        return render(request, 'tutor.html', {"name": name, "k":data})
    
    return render(request, 'tutor.html',{"name": name, "k":name})


def promedy_view(request):
    c = request.session.get("code")
    name = ""
    courses = []

    
    response2 = requests.post("http://localhost:5000/getStu", json={"code": c})
    if response2.status_code == 200:
        user = response2.json().get("user", {})
        name = user.get("name", "")

    
    resp_courses = requests.post("http://localhost:5000/NotesP")
    if resp_courses.status_code == 200:
        courses = resp_courses.json().get("courses", [])

    course = " "
    grafico_html = ""  


    if request.method == "POST":
        course = request.POST.get("course", " ")
        print("Actividad recibida:", course)

        
        resp_courses = requests.post("http://localhost:5000/NotesP")
        if resp_courses.status_code == 200:
            courses = resp_courses.json().get("courses", [])

        
        response3 = requests.post(
            "http://localhost:5000/getNotesP",
            json={"name": course}
        )

        if response3.status_code == 200:
            data3 = response3.json()
            print(data3)

            acts  = [c["act"].capitalize() for c in data3["activities"]]
            proms = [c["prom"] for c in data3["activities"]]

           
            fig = go.Figure(
                data=[go.Bar(x=acts, y=proms, marker_color="#1f77b4")]
            )
            fig.update_layout(
                title=f"Promedio de actividades - {course}",
                xaxis_title="Actividad",
                yaxis_title="Promedio",
                yaxis=dict(range=[0, max(proms) + 10]),
                template="simple_white",
                height=400,
                margin=dict(l=30, r=30, t=50, b=30),
            )

            
            grafico_html = fig.to_html(full_html=False)
        else:
            course = " "
            grafico_html = "<p>Error al obtener datos para el gráfico.</p>"


    return render(request, 'tutor.html',{"name": name, "s":course, "courses":courses, "grafic_html":grafico_html})




def top_view(request):
    c = request.session.get("code")
    name = ""
    courses = []
    activities = []
    
    response2 = requests.post("http://localhost:5000/getStu", json={"code": c})
    if response2.status_code == 200:
        user = response2.json().get("user", {})
        name = user.get("name", "")

    
    resp_courses = requests.post("http://localhost:5000/NotesP")
    if resp_courses.status_code == 200:
        courses = resp_courses.json().get("courses", [])

    course = " "
    if request.method == "POST":
        
        course = request.POST.get("course", " ")
        request.session["aCourse"] = course
        response6 = requests.post("http://localhost:5000/act", json={"name": courses[0]})
        if response6.status_code == 200:
            activities = response6.json().get("activities",[])


        return render(request, 'tutor.html',{"name": name, "w":course,"acts": activities})    

    return render(request, 'tutor.html',{"name": name, "r":course, "courses":courses})



def test_view(request): 
    if request.method == "POST":
        activities = []
        c = request.session.get("code")
        name = ""
        courses = []
        activity = " "
        response2 = requests.post("http://localhost:5000/getStu", json={"code": c})
        if response2.status_code == 200:
            user = response2.json().get("user", {})
            name = user.get("name", "")
        
        course = request.session.get('aCourse')
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", course)
        
        
        activity = request.POST.get("activity", " ")
        print("Actividad recibida:", activity)
        
        response6 = requests.post("http://localhost:5000/act", json={"name": course})
        if response6.status_code == 200:
            activities = response6.json().get("activities",[])
        
        response3 = requests.post("http://localhost:5000/getTop",
            json={"name": course, "act":activity}
        )

        if response3.status_code == 200:
            data3 = response3.json()
            print(data3)

            code  = [str(c["code"]) for c in data3["top"]]
            note = [c["note"] for c in data3["top"]]

           
            fig = go.Figure(
                data=[go.Bar(x=code, y=note, marker_color="#1f77b4")]
            )
            fig.update_layout(
                title=f"Top de notas - {activity}",
                xaxis_title="Carnet",
                yaxis_title="Nota",
                yaxis=dict(range=[0, max(note) + 10]),
                template="simple_white",
                height=400,
                margin=dict(l=30, r=30, t=50, b=30),
            )

            
            grafico_html = fig.to_html(full_html=False)
        else:
            course = " "
            grafico_html = "<p>Error al obtener datos para el gráfico.</p>"


        return render(request, 'tutor.html',{"name": name, "w":course,"q":activity , "courses":courses, "grafic_html":grafico_html,"acts": activities})
    return render(request, 'tutor.html')