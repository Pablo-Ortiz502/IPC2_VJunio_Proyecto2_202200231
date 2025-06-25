from flask import Flask, request, jsonify
from utils import Login,Timer,Settings,WriteXML,setNotes
from Users import Activity, Admin
admin = Admin()
app = Flask(__name__)

#http://localhost:5000

#login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    code = data.get('code')
    password = data.get('password')
    
    
    if not code or not password:
        return jsonify({"message": "Faltan campos"}), 400
    else:
        user = Login(code, password,admin) 
        print(user)

    if user == 1:
        app.config['USER'] = admin
        return jsonify({"message": "Login exitoso", "user": 1 }), 200
    
    try:
        int(code)
    except ValueError:
        print('codigo invalido')
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    if user == 2:
        for s in admin.students:
            if s.code == int(code):
                app.config['USER'] = s       
        return jsonify({"message": "Login exitoso", "User": 2}), 200
    
    if user == 3:
        for t in admin.tutors:
            if t.code == int(code):
                app.config['USER'] = t          
        return jsonify({"message": "Login exitoso", "user": 3}), 200
    
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    
#------------------------------------addmin ------------------------------------------------   
@app.route('/settXML', methods=['POST'])
def setXML():
    xml = request.data.decode('utf-8') 
   
    Settings(xml,admin)
    
    for student in admin.students:
        print(f"{student.name} ({student.code}) - Cursos asignados: {[c.name for c in student.courses]}")
        
    for tutor in admin.tutors:
        print(f"{tutor.name} ({tutor.code})- Cursos asignados: {[c.name for c in tutor.courses]} ")    
    
    return jsonify({"message": "exito"}),200

@app.route('/getStu', methods=['POST'])
def getStu():
    data = request.get_json()
    code = data.get('code')
    print(code)
    
    for s in admin.students:
        if s.code == int(code):
            student = admin.getStudent(int(code)).to_dict()
            return jsonify({'user': student, "tp": "student"}),200
    for t in admin.tutors:
        if t.code == int(code):
            tutor = admin.getTutor(int(code)).to_dict()
            return jsonify({'user': tutor, "tp": "tutor"}),200
        
    return jsonify({"message": "error al buscar el usuario" }),400
    

@app.route('/getAd', methods=['POST'])
def getAd():
    return jsonify({"name": "Pablo Jose Ortiz Linares","carnet": "202200231"})

@app.route('/getUs', methods=['POST'])
def getUs():
    users =[]
    for t in admin.tutors:
        users.append(t.to_dict())
    for s in admin.students:
        users.append(s.to_dict())
    return jsonify({"users": users}),200

@app.route('/getXML', methods=['POST'])
def getXML():
    
    tutors = len(admin.tutors)
    students = len(admin.students)
    fali_t = admin.t_fails
    fail_s = admin.s_fails
    
    xml = WriteXML(tutors,students,fali_t,fail_s)
    return jsonify({"res": xml})
        


#-----------------------------------------tutor-------------------------------------
@app.route('/timeXML', methods=['POST'])
def timeXML():
    tutor = app.config.get('USER')
    if not tutor:
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    xml = request.data
    Timer(xml,tutor)
    print(tutor.time)
    
    return jsonify({"message": "exito"}),200

@app.route('/getTimeXML', methods=['POST'])
def  getTime():
    tutor = app.config.get('USER')  
    times = []
    for t in tutor.time:
        print(t.to_dict())
        times.append(t.to_dict())
    
    return jsonify({"times": times}),200



@app.route('/setNotes',methods=['POST']) 
def notesApi():
    tutor = app.config.get('USER')
    if not tutor:
        print("aqui no hay tutor")
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    xml = request.data.decode('utf-8')
    matrix = setNotes(xml,tutor,admin)
    print("hola")
    
    rowHead = matrix.row.first
    notes = []
    while rowHead is not None:
        current = rowHead.acces
        columHead = matrix.colum.first
        while current is not None:
            notes.append(Activity(columHead.header,current.valor,current.x).to_dict())
            columHead = columHead.next
            current = current.next
                
        rowHead = rowHead.next

    return jsonify({"message": "exito"}),200 

@app.route('/NotesP',methods=['POST'])
def NotesT():
    tutor = app.config.get('USER')
    if not tutor:
        print("aqui no hay tutor")
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    courses = []
    for c in tutor.courses:
        matrix = admin.getMatrix(c.code)
        if matrix:
            courses.append(c.name)
    
    return jsonify({"courses": courses}),200

@app.route('/act',methods=['POST'])
def actT():
    tutor = app.config.get('USER')
    if not tutor:
        print("aqui no hay tutor")
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    data = request.get_json()
    name = data.get('name')
    code = 0
    
    for c in tutor.courses:
        if c.name.lower() == name.lower():
            code = c.code
    print(code)
    matrix = admin.getMatrix(code)
    
    if matrix:
        return jsonify({"activities": matrix.act}),200
    else:
        return jsonify({"error":"no hay notas"}),401
    
@app.route('/getNotesP',methods=['POST'])
def getNotesP():
    code = 0
    tutor = app.config.get('USER')
    if not tutor:
        print("aqui no hay tutor")
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    data = request.get_json()
    name = data.get('name')
    print("-------------------------------",name)
    for c in tutor.courses:
        if c.name.lower() == name.lower():
            code = c.code
    print(code)
    matrix = admin.getMatrix(code)
    
    data = []
    if matrix:
        for act in matrix.act:
            list, promedy = matrix.getRow(act)
            data.append({'act':act, 'prom':promedy})     
        print(data)         
        return jsonify({"activities": data}),200       
    return jsonify({"error": "error"}),401


@app.route("/getTop",methods=['POST'])
def getTop():
    code = 0
    tutor = app.config.get('USER')
    if not tutor:
        print("aqui no hay tutor")
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    #peticiones
    data = request.get_json()
    name = data.get('name')
    activity = data.get('act')
    
    print(name)
    print(activity)
     
    print("-------------------------------",name)
    for c in tutor.courses:
        if c.name.lower() == name.lower():
            code = c.code
    print(code)
    matrix = admin.getMatrix(code)
    
    listOrder = []
    if matrix:
        for act in matrix.act:
            if act.lower() == activity.lower():
                list, promedy = matrix.getRow(act)
                listOrder = sorted(list, key=lambda x: x["note"],reverse=True)
                break
                            
        return jsonify({"top": listOrder}),200       
    return jsonify({"error": "error"}),401
     


if __name__ == '__main__':
    app.run(debug=True,port=5000)

       