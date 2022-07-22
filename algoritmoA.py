class Node:
    def __init__(self,data,level,fval):
        """ Inicializa el nodo con los datos, el nivel del nodo y el valor calculado"""
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        """ Genera nodos secundarios a partir del nodo dado moviendo el espacio en blanco
            en las cuatro direcciones {arriba, abajo, izquierda, derecha} """
        x,y = self.find(self.data,'_')
        """ val_list contiene valores posicionales para mover el espacio en blanco en 
            cualquiera de las 4 direcciones [arriba, abajo, izquierda, derecha] respectivamente. """
        val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data,x,y,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                children.append(child_node)
        return children
        
    def shuffle(self,puz,x1,y1,x2,y2):
        """ Mueva el espacio en blanco en la dirección dada y si el valor de posición está fuera
             de límites el retorno es None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
            

    def copy(self,root):
        """ Copia la función para crear una matriz similar del nodo dado"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            
    def find(self,puz,x):
        """ Usado específicamente para encontrar la posición del espacio en blanco """
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    return i,j


class Puzzle:
    def __init__(self,size):
        """ Inicializa el tamaño del puzzle por el tamaño especificado, abre y cierra las listas para vaciar """
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """ Acepta el puzzle del usuario """
        puz = []
        for i in range(0,self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self,start,goal):
        """ Función heurística para calcular el valor heurístico f(x) = h(x) + g(x) """
        return self.h(start.data,goal)+start.level

    def h(self,start,goal):
        """ Calcula la diferencia de los puzzles """
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp
        

    def process(self):
        """ Acepta los puzzles inicial y objetivo"""
        print("Ingrese el estado inicial")
        start = self.accept()
        print("\n")
        print("Ingrese el estado objetivo")        
        goal = self.accept()
        print("\n")
        start = Node(start,0,0)
        start.fval = self.f(start,goal)
        """ Pone el nodo de inicio en la lista abierta"""
        self.open.append(start)
        print("\n\n")
        while True:
            cur = self.open[0]
            print("")
            print("  | ")
            print(" \\\'/ \n")
            
            for i in cur.data:
                for j in i:
                    print(j,end=" ")
                print("")
            """ Si la diferencia entre el nodo actual y el objetivo es 0, hemos llegado al nodo objetivo"""
            if(self.h(cur.data,goal) == 0):
                break
            for i in cur.generate_child():
                i.fval = self.f(i,goal)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]

            """ ordenar la lista en función del valor f """
            self.open.sort(key = lambda x:x.fval,reverse=False)


puz = Puzzle(3)
puz.process()