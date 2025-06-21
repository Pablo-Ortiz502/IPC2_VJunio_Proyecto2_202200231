

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
        
        