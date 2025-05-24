def leerClientes():
    try:
        clients = []
        with open("clientes.txt", "r") as document:
            for line in document:
                name, requieredOccupation, presupuesto= line.strip().split(';')
                clients.append({"name": name, "requiered occupation": requieredOccupation, "presupuesto": presupuesto})
        return clients
    except Exception as e:
        print(f'Error al leer el archivo: {e}')
        return []

def leerEmpleados():
    try:
        workers=[]
        with open("empleados.txt", "r") as document:
            for line in document:
                name, occupation, price = line.strip().split(';')
                workers.append({"name": name, "occupation": occupation, "price": price})
        return workers
    except Exception as e:
        print(f'Error al leer el archivo: {e}')
        return[]

class graph:
    def __init__(self, nWorkers, nClients):
        self.nWorkers=nWorkers
        self.nClients=nClients
        self.graph={i: [] for i in range (nClients)}
        self.matchWorker=[-1] * nWorkers
    
    def addEdge(self, client, worker):
        self.graph[client].append(worker)
        
    def dfs(self, u, visited):
        for v in self.graph[u]:
            if not visited[v]:
                visited[v] = True
                if self.matchWorker[v] == -1 or self.dfs(self.matchWorker[v], visited):
                    self.matchWorker[v] = u
                    return True
        return False
    
    def maxBPM(self):
        result=0
        for u in range(self.nClients):
            visited=[False] * self.nWorkers
            if self.dfs(u, visited):
                result+=1
        return result
    
    def getMatches(self):
        matches = []
        for i in range(len(self.matchWorker)):
            if self.matchWorker[i] != -1:
                matches.append((self.matchWorker[i], i))
        return matches
    
if __name__ == "__main__":
    clients=leerClientes()
    workers=leerEmpleados()
    graph=graph(len(workers), len(clients))
    for i in range(len(clients)):
        for j in range(len(workers)):
            if clients[i]["requiered occupation"]==workers[j]["occupation"] and int(clients[i]["presupuesto"])>=int(workers[j]["price"]):
                graph.addEdge(i, j)
    maxBPM=graph.maxBPM()
    matches=graph.getMatches()
    print(f'El maximo emparejamiento es: {maxBPM}')
    for match in matches:
        print(f'Cliente {clients[match[0]]["name"]} emparejado con empleado {workers[match[1]]["name"]}')