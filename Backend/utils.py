

from Users import Admin, Tutor, Student, Course, Time
from xml.dom import minidom
import re
from xml.dom.minidom import Document

def Login(code ,password, admin:Admin):
    
    if password == admin.password and code == admin.name:
        return 1

    for student in admin.students:
        if password == student.password and code == str(student.code):
            return 2
    
    for tutor in admin.tutors:
        if password == tutor.password and code == str(tutor.code):
            return 3
    
    return 0

def Settings(xml,admin:Admin):
    
    xml_string = xml.decode('utf-8') if isinstance(xml, bytes) else xml

    dom = minidom.parseString(xml_string)
    root = dom.documentElement

    
    courses = root.getElementsByTagName("curso")
    for c in courses:
        code = c.getAttribute("codigo")
        name = c.firstChild.nodeValue.strip()
        
        ex = next((c for c in admin.courses if c.code == int(code)), None)
        
        if not ex:
            admin.courses.append(Course(name, int(code)))

  
    tutors = root.getElementsByTagName("tutor")
    for t in tutors:
        code = t.getAttribute("registro_personal")
        password = t.getAttribute("contrasenia")
        name = t.firstChild.nodeValue.strip()
        
        ex = next((t for t in admin.tutors if t.code == int(code)), None)
        
        if not ex:
            admin.tutors.append(Tutor(name, int(code), password))
        
        

  
    students = root.getElementsByTagName("estudiante")
    for s in students:
        code = s.getAttribute("carnet")
        password = s.getAttribute("contrasenia")
        name = s.firstChild.nodeValue.strip()
        
        
        ex = next((s for s in admin.students if s.code == int(code)), None)
        
        if not ex:
            admin.students.append(Student(name, int(code), password))
        
        
          
       
                        
   
    tutorCourse = root.getElementsByTagName("tutor_curso")
    for tc in tutorCourse:
        courseC = int(tc.getAttribute("codigo"))
        tutorC = int(tc.firstChild.nodeValue.strip())
        
       
        course = next((c for c in admin.courses if c.code == courseC), None)
        tutor = next((t for t in admin.tutors if t.code == tutorC), None)

        if course and tutor:
            tutor.courses.append(course)
            course.setTutor(tutor.name)
        else:
            admin.t_fails +=1
 
    studenCourses = root.getElementsByTagName("estudiante_curso")
    for ec in studenCourses:
        courseC = int(ec.getAttribute("codigo"))
        studentC = int(ec.firstChild.nodeValue.strip())

        course = next((c for c in admin.courses if c.code == courseC), None)
        student = next((s for s in admin.students if s.code == studentC), None)

        if course and student:
            student.courses.append(course)
        else:
            admin.s_fails +=1
            
            
def Timer(xml,tutor:Tutor): 
    xml_string = xml.decode('utf-8') if isinstance(xml, bytes) else xml
               
    dom = minidom.parseString(xml_string)
    courses = dom.getElementsByTagName("curso")

    for course in courses:
        codigo = int(course.getAttribute("codigo"))
        date = course.firstChild.nodeValue.strip()

       
        time = re.findall(r'\b\d{2}:\d{2}\b', date)
        if len(time) >= 2:
            for c in tutor.courses:
                if c.code == codigo:
                    time_obj = Time(time[0], time[1], codigo)
                    tutor.time.append(time_obj)
            
def WriteXML(tutors,students,inTutors,inStudents):
    doc = Document()

   
    root = doc.createElement("configuraciones_aplicadas")
    doc.appendChild(root)

  
    tutorElm = doc.createElement("tutores_cargados")
    tutorElm.appendChild(doc.createTextNode(str(tutors + inTutors)))
    root.appendChild(tutorElm)

    studentElm = doc.createElement("estdudiantes_cargados")
    studentElm.appendChild(doc.createTextNode(str(students + inStudents)))
    root.appendChild(studentElm)

    #asignaciones
    asaignElm = doc.createElement("asignaciones")
    root.appendChild(asaignElm)

    # tutores
    tutorAsgn = doc.createElement("tutores")
    asaignElm.appendChild(tutorAsgn)

    totalT = doc.createElement("total")
    totalT.appendChild(doc.createTextNode(str(tutors + inTutors)))
    tutorAsgn.appendChild(totalT)

    validT = doc.createElement("correcto")
    validT.appendChild(doc.createTextNode(str(tutors)))
    tutorAsgn.appendChild(validT)

    incorrectT = doc.createElement("incorrecto")
    incorrectT.appendChild(doc.createTextNode(str(inTutors)))
    tutorAsgn.appendChild(incorrectT)

    # estudiantes
    studentAsgn = doc.createElement("estudiantes")
    asaignElm.appendChild(studentAsgn)

    totalS = doc.createElement("total")
    totalS.appendChild(doc.createTextNode(str(students + inStudents)))
    studentAsgn.appendChild(totalS)

    validS = doc.createElement("correcto")
    validS.appendChild(doc.createTextNode(str(students)))
    studentAsgn.appendChild(validS)

    incorrectS = doc.createElement("incorrecto")
    incorrectS.appendChild(doc.createTextNode(str(inStudents)))
    studentAsgn.appendChild(incorrectS)

    
    return doc.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")