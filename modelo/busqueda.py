import time
from ambiente import *
from arbol import *
from collections import deque
from queue import PriorityQueue



def es_nodo_meta(nodo):
    ambiente = nodo.estado
    mando_posicion = ambiente.mando.get_posicion()
    grogu_posicion = ambiente.grogu.get_posicion()
    
    # Verificar si la posición del Mando coincide con la posición de Grogu
    return mando_posicion == grogu_posicion

def es_enemigo(nodo):
    ambiente = nodo.estado
    mando_posicion = ambiente.mando.get_posicion()
    enemigos = ambiente.enemigos
    for enemigo in enemigos:
        if enemigo.get_posicion() == mando_posicion:
            return True
    return False            

def es_nave(nodo):
    if nodo.paso_por_nave:
        return True
    else:
        ambiente = nodo.estado
        mando_posicion = ambiente.mando.get_posicion()
        naves = ambiente.naves
        for nave in naves:
            if nave.get_posicion() == mando_posicion:
                return True
        return False  

def reconstruir_camino(nodo):
    camino = []
    while nodo.padre is not None:
        camino.append(nodo.operador)
        nodo = nodo.padre
    camino.reverse()  # Invertir el camino para obtener el orden correcto
    return camino

def evitar_ciclos(nodo):
    if nodo.profundidad <= 1:
        return False
    antecesor = nodo.padre.padre

    while antecesor is not None:
        if antecesor.estado == nodo.estado:
            return True
        antecesor = antecesor.padre

    return False

def busqueda_profundidad(ambiente):
    inicio = time.time()
    nodo = Nodo(ambiente)
    stack = [nodo]  # Usar una pila para almacenar nodos a explorar
    explorados = set()  # Conjunto para almacenar estados explorados
    nodos_expandidos = []  # Lista para almacenar los nodos expandidos
    
    while stack:
        nodo_actual = stack.pop()  # Obtener el nodo más reciente de la pila
        
        if es_nodo_meta(nodo_actual):
            tiempo_total = time.time() - inicio
            return reconstruir_camino(nodo_actual), "Se encontró", nodos_expandidos, nodo_actual.profundidad, tiempo_total
         
        estado_actual = str(nodo_actual.estado.matriz)  # Convertir la matriz a una cadena para usarla como clave
        
        if estado_actual in explorados or evitar_ciclos(nodo_actual):
            continue  # Evitar nodos ya explorados y ciclos
        
        explorados.add(estado_actual)  # Agregar el estado actual al conjunto de explorados
        nodos_expandidos.append(nodo_actual)  # Agregar el nodo actual a la lista de nodos expandidos
        
        for accion in nodo_actual.estado.mando.get_movimientos_posibles(nodo_actual.estado.matriz):
            nuevo_estado = nodo_actual.estado.copy()
            nuevo_estado.transicion(accion)
            nuevo_nodo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.profundidad + 1)
            stack.append(nuevo_nodo)  # Agregar el nuevo nodo a la pila
    
    return [], "No se encontró", nodos_expandidos




def busqueda_amplitud(ambiente):
    inicio = time.time()
    nodo = Nodo(ambiente)
    queue = PriorityQueue([nodo])  # Usar una cola para almacenar nodos a explorar
    explorados = set()  # Conjunto para almacenar estados explorados
    nodos_expandidos = []  # Lista para almacenar los nodos expandidos 
    while queue:
        nodo_actual = queue.popleft()  # Obtener el nodo más antiguo de la cola
        
        if es_nodo_meta(nodo_actual):
            tiempo_total = time.time() - inicio
            return reconstruir_camino(nodo_actual), "Se encontró", nodos_expandidos, nodo_actual.profundidad, tiempo_total
         
        estado_actual = str(nodo_actual.estado.matriz)  # Convertir la matriz a una cadena para usarla como clave
        
        if estado_actual in explorados or evitar_ciclos(nodo_actual):
            continue  # Evitar nodos ya explorados y ciclos
        
        explorados.add(estado_actual)  # Agregar el estado actual al conjunto de explorados
        nodos_expandidos.append(nodo_actual)  # Agregar el nodo actual a la lista de nodos expandidos
        
        for accion in nodo_actual.estado.mando.get_movimientos_posibles(nodo_actual.estado.matriz):
            nuevo_estado = nodo_actual.estado.copy()
            nuevo_estado.transicion(accion)
            nuevo_nodo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.profundidad + 1)
            queue.append(nuevo_nodo)  # Agregar el nuevo nodo a la cola
    
    return [], "No se encontró", nodos_expandidos



from queue import PriorityQueue

def busqueda_costo_uniforme(ambiente):
    inicio = time.time()
    nodo = Nodo(ambiente)
    queue = PriorityQueue()  # Usar una cola de prioridad para almacenar nodos a explorar
    queue.put((nodo.costo, nodo))  # Insertar el nodo inicial en la cola de prioridad
    explorados = set()  # Conjunto para almacenar estados explorados
    nodos_expandidos = []  # Lista para almacenar los nodos expandidos 
    
    while not queue.empty():
        _, nodo_actual = queue.get()  # Obtener el nodo con el menor costo acumulado de la cola de prioridad
        
        if es_nodo_meta(nodo_actual):
            tiempo_total = time.time() - inicio
            return reconstruir_camino(nodo_actual), "Se encontró", nodos_expandidos, nodo_actual.profundidad, tiempo_total, nodo_actual.costo
         
        estado_actual = str(nodo_actual.estado.matriz)  # Convertir la matriz a una cadena para usarla como clave
        
        if estado_actual in explorados or evitar_ciclos(nodo_actual):
            continue  # Evitar nodos ya explorados y ciclos
        
        explorados.add(estado_actual)  # Agregar el estado actual al conjunto de explorados
        nodos_expandidos.append(nodo_actual)  # Agregar el nodo actual a la lista de nodos expandidos
        
        for accion in nodo_actual.estado.mando.get_movimientos_posibles(nodo_actual.estado.matriz):
            nuevo_estado = nodo_actual.estado.copy()
            nuevo_estado.transicion(accion)
            if es_nave(nodo_actual) and not es_enemigo(nodo_actual):
                nuevo_nodo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.profundidad + 1, nodo_actual.costo + 1/2, nodo_actual.contador_pasos + 1, True, nodo_actual.paso_por_enemigo)
                if nuevo_nodo.contador_pasos >= 10:
                    nuevo_nodo.paso_por_nave = False
                    nuevo_nodo.contador_pasos = 0

            if es_nave(nodo_actual) and es_enemigo(nodo_actual):
                nuevo_nodo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.profundidad + 1, nodo_actual.costo + 1/2, nodo_actual.contador_pasos, nodo_actual.paso_por_nave, nodo_actual.paso_por_enemigo)
            elif es_enemigo(nodo_actual):
                nuevo_nodo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.profundidad + 1, nodo_actual.costo + 5, nodo_actual.contador_pasos, nodo_actual.paso_por_nave, nodo_actual.paso_por_enemigo)
            if not es_enemigo(nodo_actual) and not es_nave(nodo_actual):
                nuevo_nodo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.profundidad + 1, nodo_actual.costo + 1, nodo_actual.contador_pasos, nodo_actual.paso_por_nave, nodo_actual.paso_por_enemigo)
            queue.put((nuevo_nodo.costo, nuevo_nodo))  # Agregar el nuevo nodo a la cola de prioridad
    
    return [], "No se encontró", nodos_expandidos




# Cargar el ambiente desde el archivo
ambiente = Ambiente()
ambiente.cargar_desde_archivo(r'modelo\ambiente.txt')



# Realizar la búsqueda DFS
camino, mensaje, nodos_expandidos, profundidad , tiempo_total, costo_total = busqueda_costo_uniforme(ambiente)  # Modifica esta línea

print("Camino encontrado:", camino)
print("Mensaje:", mensaje)
print("Nodos expandidos:", len(nodos_expandidos))  # Agrega esta línea para mostrar los nodos expandidos
print("Tiempo de ejecución:", tiempo_total)
print("Profundidad:", profundidad)
print("Costo:", costo_total)
