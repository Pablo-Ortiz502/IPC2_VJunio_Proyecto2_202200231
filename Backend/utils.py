from django.conf import settings
from Users import Admin, Tutor, Student, Course
from xml.dom import minidom

def Login(code,password, admin:Admin):
    if password is None or code is None:
        return 0
    
    if password == admin.password and code == admin.name:
        return 1
    
    for student in admin.students:
        if password == student.password and code == student.code:
            return 2
    
    for tutor in admin.tutors:
        if password == tutor.password and code == tutor.code:
            return 3
    
    return 0

def Settings(ruta,admin:Admin):
    
    dom = minidom.parse(ruta)
    root = dom.documentElement

    
    courses = root.getElementsByTagName("curso")
    for c in courses:
        code = c.getAttribute("codigo")
        name = c.firstChild.nodeValue.strip()
        admin.courses.append(Course(name, int(code)))

  
    tutors = root.getElementsByTagName("tutor")
    for t in tutors:
        code = t.getAttribute("registro_personal")
        password = t.getAttribute("contrasenia")
        name = t.firstChild.nodeValue.strip()
        admin.tutors.append(Tutor(name, int(code), password))

  
    students = root.getElementsByTagName("estudiante")
    for s in students:
        code = s.getAttribute("carnet")
        password = s.getAttribute("contrasenia")
        name = s.firstChild.nodeValue.strip()
        admin.students.append(Student(name, int(code), password))

   
    tutorCourse = root.getElementsByTagName("tutor_curso")
    for tc in tutorCourse:
        courseC = int(tc.getAttribute("codigo"))
        tutorC = int(tc.firstChild.nodeValue.strip())
        
       
        course = next((c for c in admin.courses if c.code == courseC), None)
        tutor = next((t for t in admin.tutors if t.code == tutorC), None)

        if course and tutor:
            tutor.courses.append(course.code)
            course.setTutor(tutor.name)

 
    studenCourses = root.getElementsByTagName("estudiante_curso")
    for ec in studenCourses:
        courseC = int(ec.getAttribute("codigo"))
        studentC = int(ec.firstChild.nodeValue.strip())

        course = next((c for c in admin.courses if c.code == courseC), None)
        student = next((s for s in admin.students if s.code == studentC), None)

        if course and student:
            student.addCourse(course)
 
 
if __name__ == "__main__":
    admin = Admin()
    from utils import Settings
    root = 'D:/Usac/IPC2/IPC2_VJunio_Proyecto2_202200231/prueba.xml'
    Settings(root,admin)
    
    for student in admin.students:
        print(f"{student.name} ({student.code}) - Cursos asignados: {[c.name for c in student.courses]}")
        print(admin.tutors[0].courses)