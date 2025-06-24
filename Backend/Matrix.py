class HeadNode():
    def __init__(self, id,header):
        self.id = id
        self.next = None
        self.prev = None
        self.acces = None
        self.value = None
        self.header = header

class HeadList():
    def __init__(self, type):
        self.type = type
        self.first = None
        self.last = None
        self.size = 0
        
    def addHeadNode(self, newNode):
        if self.first is None:
            self.first = newNode
            self.last = newNode
        else:
            if newNode.id < self.first.id:
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
                    if newNode.id < current.id:
                        newNode.next = current
                        newNode.prev = current.prev
                        if current.prev:
                            current.prev.next = newNode
                        current.prev = newNode
                        break
                    elif newNode.id == current.id:
                        return  # Ya existe
                    current = current.next
        self.size += 1

    def getHead(self, id) -> HeadNode:
        current = self.first
        while current is not None:
            if current.id == id:
                return current
            current = current.next
        return None

class Node():
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor
        self.next = None
        self.prev = None
        self.up = None
        self.down = None

class Matrix():
    def __init__(self, layer, name):
        self.layer = layer
        self.name = name
        self.row = HeadList('x')
        self.colum = HeadList('y')

    def checkHead(self, x, y,activity):
        xNode = self.row.getHead(x)
        yNode = self.colum.getHead(y)

        if xNode is None:
            xNode = HeadNode(x,None)
            self.row.addHeadNode(xNode)
            
        if yNode is None:
            yNode = HeadNode(y,activity)
            self.colum.addHeadNode(yNode)
           

        return xNode, yNode

    def add(self, x, y, valor,activity):
        new = Node(x, y, valor)
        nodeRow, nodeCol = self.checkHead(x, y,activity)

        # Insertar en fila (horizontal)
        if nodeRow.acces is None:
            nodeRow.acces = new
        else:
            current = nodeRow.acces
            if new.y < current.y:
                new.next = current
                current.prev = new
                nodeRow.acces = new
            else:
                while current is not None:
                    if new.y == current.y:
                        return  
                    elif new.y < current.y:
                        new.next = current
                        new.prev = current.prev
                        if current.prev:
                            current.prev.next = new
                        current.prev = new
                        break
                    elif current.next is None:
                        current.next = new
                        new.prev = current
                        break
                    current = current.next

        # Insertar en columna (vertical)
        if nodeCol.acces is None:
            nodeCol.acces = new
        else:
            current = nodeCol.acces
            if new.x < current.x:
                new.down = current
                current.up = new
                nodeCol.acces = new
            else:
                while current is not None:
                    if new.x == current.x:
                        return  # Ya existe ese nodo
                    elif new.x < current.x:
                        new.down = current
                        new.up = current.up
                        if current.up:
                            current.up.down = new
                        current.up = new
                        break
                    elif current.down is None:
                        current.down = new
                        new.up = current
                        break
                    current = current.down

    def display(self):
        rowHead = self.row.first
        
        while rowHead is not None:
            current = rowHead.acces
            columHead = self.colum.first
            while current is not None:
                print(f"({current.x}, {columHead.header},{current.y}) = {current.valor}")
                columHead = columHead.next
                current = current.next
                
            rowHead = rowHead.next
            
            #aun falta

if __name__ == '__main__':
    m = Matrix(0,"curso 2")
    m.add(2010002332, 1, 'A',"tarea1")
    m.add(2010002332, 2, 'B',"tarea2")
    m.add(2010002332, 3, 'C',"tarea3") 

    m.display()