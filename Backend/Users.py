

class Admin(object):
    def __init__(self):
        self.name = 'AdminIPC2'
        self.password = 'AdminIPC2771'
        self.students = []
        self.tutors = []
        self.courses = []
        self.notes = []
        self.t_fails = 0
        self.s_fails =0
    def getCourse(self,code:int):
        for c in self.courses:
            if c.code == code:
                return c
        print('no se encontro el curso')          
        return None
    
    def getStudent(self, code:int):
        for s in self.students:
            if s.code == code:
                return s
        print('no se encontro el estudiante')          
        return None
    
    def getTutor(self, code: int):
        for t in self.tutors:
            if t.code == code:
                return t
        print('no se encontro el Tutor')          
        return None
    
    def getMatrix(self, name: str):
        for m in self.notes:
            if m.name == name:
                return m
    
class Tutor(object):
    def __init__(self, name, code, password) :
        self.name = name
        self.code = code
        self.password = password
        self.courses = []
        self.time = []
    
    def getCourse(self,code:int):
        for c in self.courses:
            if c.code == code:
                return c
        print('no se encontro el curso')          
        return None    
        
    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "password": self.password
        }    


class Time(object):
    def __init__(self,start,end,code,name):
        self.start = start
        self.end = end
        self.code = code 
        self.name = name        
    
    def to_dict(self):
        return{
            "start": self.start,
            "end": self.end,
            "code": self.code,
            "name": self.name
        }    


class Course(object):
    def __init__(self,name, code):
        self.name = name
        self.code = code
        self.note = 0
        self.tutor = None
        
        
        
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
             
    def getCourse(self, code):
        for course in self.courses:
            if course.code == code:
                return course
        print("No se encontro el curso asignado")       
        return None
    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "password": self.password
        }  
           
class Activity(object):
    def __init__(self,name, note,code):
        self.name = name
        self.note = note
        self.code = code
    def to_dict(self):
        return{
            "name": self.name,
            "note": self.note,
            "code": self.code
        }    
                
                