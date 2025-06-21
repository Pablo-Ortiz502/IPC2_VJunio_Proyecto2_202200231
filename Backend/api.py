from flask import Flask, request, jsonify, Response
from utils import Login,Timer,Settings,WriteXML
from Users import Admin, Student
from xml.dom import minidom
admin = Admin()
app = Flask(__name__)

#http://localhost:8000

#login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    code = data.get('code')
    password = data.get('password')
    
    
    if not code or not password:
        return jsonify({"message": "Faltan campos"}), 400
    else:
        status = Login(code, password,admin)

    if status == 1:
        app.config['USER'] = admin
        return jsonify({"message": "Login exitoso", "Admin": code}), 200
    
    try:
        int(code)
    except ValueError:
        print('codigo invalido')
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    if status == 2:
        for s in admin.students:
            if s.code == int(code):
                app.config['USER'] = s
        return jsonify({"message": "Login exitoso", "Estudiante": code}), 200
    
    if status == 3:
        for t in admin.tutors:
            if t.code == int(code):
                app.config['USER'] = t  
        return jsonify({"message": "Login exitoso", "Tutor": code}), 200
    
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    
#addmin    
@app.route('/settXML', methods=['POST'])
def setXML():
    xml = request.data.decode('utf-8') 
   
    Settings(xml,admin)
    
    for student in admin.students:
        print(f"{student.name} ({student.code}) - Cursos asignados: {[c.name for c in student.courses]}")
        
    for tutor in admin.tutors:
        print(f"{tutor.name} ({tutor.code})")    
    
    return jsonify({"message": "exito"}),200

@app.route('/getAd')
def getAd():
    return jsonify({"name": "Pablo Jose Ortiz Linares","carnet": "202200231"})

@app.route('/getUs')
def getUs():
    users =[]
    for t in admin.tutors:
        users.append(t.to_dict())
    for s in admin.students:
        users.append(s.to_dict())
    return jsonify({"users": users}),200

@app.route('/getXML')
def getXML():
    
    tutors = len(admin.tutors)
    students = len(admin.students)
    fali_t = admin.t_fails
    fail_s = admin.s_fails
    
    xml = WriteXML(tutors,students,fali_t,fail_s)
    return jsonify({"salida": xml})
        


#tutor
@app.route('/timeXML', methods=['POST'])
def timeXML():
    tutor = app.config.get('USER')
    if not tutor:
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    xml = request.data.decode('utf-8') 
    Timer(xml,tutor)
    tutor =admin.tutors[0].time[0]
    print('-------',tutor.code,'inicia',tutor.start,'termina',tutor.end)
    
    return jsonify({"message": "exito"}),200



if __name__ == '__main__':
    app.run(debug=True,port=8000)