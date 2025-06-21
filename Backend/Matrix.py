from sys import last_exc
from tkinter import N
from turtle import circle


class HeadNode():
    def __init__(self,id):
        self.id = id
        self.next = None
        self.prev = None
        self.acces = None
        self.value = None

class HeadList():
    def __init__(self, type):
        self.type = type
        self.first =None
        self.last = None
        self.size = 0
        
    def addHeadNode(self,newNode):
        if self.first is None:
            self.first = newNode
            self.last = newNode
        else:
            if newNode.id > self.first.id:
               newNode.next = self.first
               self.first.prev = newNode
               self.first = newNode 
            elif newNode.id > self.last.id:
                self.last.next = newNode
                newNode.prev = self.last
                self.last = newNode
            else:
                current = self.first
                while current is not None:
                    if newNode.i < current.id:
                        newNode.next = current
                        newNode.prev = current.prev
                        current.prev.next = newNode
                        current.prev = newNode
                        break
                    elif newNode.id > current.id:
                        current = current.next
                    else:
                        return      
        self.size +=1  
                
    def getHead(self, id) -> HeadNode:
        current = self.first
        
        while current is not None:
            if current.id == id:
                return current
            current = current.next
        return None
    
       
class Node():
    def __init__(self, x,y,valor):
        self.x = x
        self.y = y
        self.valor = valor
        self.next = None
        self.prev = None
        self.up = None
        self.down = None
        
class Matrix():
    def __init__(self,layer):
        self.lauyer = 0
        self.row = HeadList('x')
        self.colum = HeadList('y')
        
    def add(self,x,y,valor):
        new = Node(x,y,valor)
        
        nodeRow, nodeColum = self.checkHead(x,y)
        
        if nodeRow.acces is None:
            nodeRow.acces = new
        else:
            if new.y < nodeRow.acces.y:
                new.next = nodeRow.acces
                nodeRow.acces.prev = new
                nodeRow.acces = new
            else:
                current = nodeRow.acces
                while current is not None:
                    if new.y < current.y:
                        new.next = current
                        new.prev = current.prev
                        current.prev.next = new
                        current.prev = new
                        break
                    elif new.x == current.x and new.y == current.y:
                        return
                    else:
                        if current.next is None:
                            current.next = new
                            new.prev = current
                            break
                        else:
                            current = current.next
        
    def checkHead(self,x,y):
        xNode =  self.row.getHead(x)
        yNode = self.colum.getHead(y)
        
        if xNode is None:
            xNode = HeadNode(x)
            self.row.addHeadNode(xNode)
        if yNode is None:
            yNode = HeadNode(y)
            self.colum.addHeadNode(yNode)
       
        return xNode, yNode         
        
         