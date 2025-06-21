class Course(object):
    def __init__(self,name, code):
        self.name = name
        self.code = code
        self.note = None
        self.tutor = None
        self.actividades = None
        
        
        
    def setNonte(self, note):
        self.note = note    
    def setTutor(self, tutor):
        self.tutor = tutor