def leerClientes():
    try:
        
        clients = []
        with open("clientes.txt", "r") as document:
            for line in document:
                # Se espera que cada línea tenga el formato "nombre;ocupacion requerida;presupuesto"
                # Se usa strip() para eliminar espacios en blanco y saltos de línea
                # Se usa split() para separar los valores por el delimitador ";"
                name, requieredOccupation, presupuesto= line.strip().split(';')
                # Se verifica que el presupuesto sea un número positivo
                if float(presupuesto) < 0:
                    raise ValueError("En el/la cliente/a {name} el presupuesto no puede ser negativo")
                # se añade el cliente a la lista de clientes
                clients.append({"name": name, "requiered occupation": requieredOccupation, "presupuesto": presupuesto})
        # Se devuelve la lista de clientes
        return clients
    except Exception as e:
        # Se maneja cualquier excepción que ocurra durante la lectura del archivo
        print(f'Error al leer el archivo, verifique que los valores esten dentro de lo estipulado: {e}')
        return False

def leerEmpleados():
    try:
        workers=[]
        with open("empleados.txt", "r") as document:
            for line in document:
                # Se espera que cada línea tenga el formato "nombre;ocupacion;precio"
                # Se usa strip() para eliminar espacios en blanco y saltos de línea
                # Se usa split() para separar los valores por el delimitador ";"
                name, occupation, price = line.strip().split(';')
                # Se verifica que el precio sea un número positivo
                if float(price) < 0:
                    raise ValueError(f'En el/la trabajador/a {name} el precio no puede ser negativo')
                # se añade el trabajador a la lista de trabajadores
                workers.append({"name": name, "occupation": occupation, "price": price})
        return workers
    except Exception as e:
        print(f'Error al leer el archivo, verifique que los valores estén dentro de lo estipulado: {e}')
        return False
# En este codigo se implementa el algoritmo de emparejamiento bipartito para asignar trabajadores a clientes, es por esto que se cree la clase graph
class graph:
    # Se crea la clase graph para representar el grafo bipartito
    # Se inicializan los atributos nWorkers y nClients para representar la cantidad de trabajadores y clientes respectivamente
    # Se crea un diccionario graph para representar el grafo, donde cada cliente tiene una lista de trabajadores
    # Se inicializa el atributo matchWorker para representar la asignacion de trabajadores a clientes, inicialmente todos los trabajadores no tienen cliente asignado
    
    def __init__(self, nWorkers, nClients):
        self.nWorkers=nWorkers
        self.nClients=nClients
        self.graph={i: [] for i in range (nClients)}
        self.matchWorker=[-1] * nWorkers
    
    # Se crea el metodo addEdge para agregar una arista entre un cliente y un trabajador
    # Se agrega el trabajador a la lista de trabajadores del cliente en el grafo
    
    def addEdge(self, client, worker):
        self.graph[client].append(worker)
    
    # Se crea el metodo dfs para realizar una busqueda en profundidad pensando en la asignacion de trabajadores
    #este algoritmo se usa en el algoritmo de flujo maximo en redes, para grafos bipartitos se usa para encontrar un emparejamiento maximo
    #ya que si volvemos el grafo bipartito en un grafo dirigido, el algoritmo de flujo maximo nos da el emparejamiento maximo
    def dfs(self, u, visited):
        for v in self.graph[u]:
            if not visited[v]:
                visited[v] = True
                if self.matchWorker[v] == -1 or self.dfs(self.matchWorker[v], visited):
                    self.matchWorker[v] = u
                    return True
        return False
    
    # Se crea el metodo maxBPM para encontrar el emparejamiento maximo
    # Se inicializa el resultado en 0
    # Se itera sobre cada cliente y se llama al metodo dfs para encontrar un emparejamiento
    # Si se encuentra un emparejamiento, se incrementa el resultado
    # Se devuelve el resultado final
    def maxBPM(self):
        result=0
        for u in range(self.nClients):
            visited=[False] * self.nWorkers
            if self.dfs(u, visited):
                result+=1
        return result
    
    # Se crea el metodo getMatches para obtener los emparejamientos
    # Se itera sobre cada trabajador y se verifica si tiene un cliente asignado
    # Si tiene un cliente asignado, se agrega el emparejamiento a la lista de matches
    # Se devuelve la lista de emparejamientos
    def getMatches(self):
        matches = []
        for i in range(len(self.matchWorker)):
            if self.matchWorker[i] != -1:
                matches.append((self.matchWorker[i], i))
        return matches
    
if __name__ == "__main__":
    # Se llama a las funciones leerClientes y leerEmpleados para leer los datos de los archivos
    clients=leerClientes()
    workers=leerEmpleados()
    # Se verifica si se leyeron los datos correctamente
    if not clients or not workers:
        print("No se pudieron leer los datos de clientes o empleados.")
        exit(1)
    
    # Se crea un objeto de la clase graph con la cantidad de trabajadores y clientes
    graph=graph(len(workers), len(clients))
    # Se itera sobre cada cliente y trabajador para agregar las aristas al grafo
    for i in range(len(clients)):
        for j in range(len(workers)):
            if clients[i]["requiered occupation"]==workers[j]["occupation"] and int(clients[i]["presupuesto"])>=int(workers[j]["price"]):
                graph.addEdge(i, j)
    # Se llama al metodo maxBPM para encontrar el emparejamiento maximo
    maxBPM=graph.maxBPM()
    # Se llama al metodo getMatches para obtener los emparejamientos
    matches=graph.getMatches()
    # Se imprime el resultado
    print(f'El maximo emparejamiento es: {maxBPM}')
    for match in matches:
        print(f'{clients[match[0]]["name"]} --- {workers[match[1]]["name"]}')