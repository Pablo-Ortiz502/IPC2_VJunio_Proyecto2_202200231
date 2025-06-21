class Admin(object):
    def __init__(self):
        self.name = 'AdminIPC2'
        self.password = 'AdminIPC2771'
        self.students = []
        self.tutors = []
        self.courses = []   
        
class Tutor(object):
    def __init__(self, name, code, password) :
        self.name = name
        self.code = code
        self.password = password
        self.courses = []


class Course(object):
    def __init__(self,name, code):
        self.name = name
        self.code = code
        self.note = None
        self.tutor = None
        self.actividades = []
        
        
        
    def setNonte(self, note):
        self.note = note    
    def setTutor(self, tutor):
        self.tutor = tutor         
        

class Student(object):
    def __init__(self, name, code, password):
        self.name = name
        self.code = code
        self.password = password
        self.courses =[]
        
        
    def addCourse(self, course):
        self.courses.append(course)
        print(self.courses)
        
    def getCourse(self, course):
        for course in self.courses:
            if course.name == course:
                return course
        print("No se encontro el curso asignado")       
        return None
    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "password": self.password
        }     
        
                