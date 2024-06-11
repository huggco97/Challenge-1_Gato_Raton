import random
import time

# crea un tablero del tamanho tamano_tablero x tamanho_tablero
def crear_tablero(tamano_tablero):
    return [[' . ' for _ in range(tamano_tablero)] for _ in range(tamano_tablero)]

#Crea un nuevo tablero basado en el estado actual del juego.
def actualizar_tablero(tablero, posicion_gato, posicion_raton, cueva):
    tamano_tablero = len(tablero)
    nuevo_tablero = [[' . ' for _ in range(tamano_tablero)] for _ in range(tamano_tablero)]
    x_gato, y_gato = posicion_gato
    x_raton, y_raton = posicion_raton
    if cueva:
        x_cueva, y_cueva = cueva
        nuevo_tablero[x_cueva][y_cueva] = " 🕳️ "
    nuevo_tablero[x_gato][y_gato] = ' 🐈 '
    nuevo_tablero[x_raton][y_raton] = ' 🐁 '

    return nuevo_tablero

#Funcion para mostrar el tablero
def mostrar_tablero(tablero):
    for fila in tablero:
        print(' '.join(fila))
    print()

#Funcion para calcular los movimientos desde una posicion dada
def movimientos_posibles(posicion, tamano_tablero):
    x, y = posicion
    movimientos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
    for dx, dy in direcciones:
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < tamano_tablero and 0 <= nuevo_y < tamano_tablero:
            movimientos.append([nuevo_x, nuevo_y])
    return movimientos

#Evalúa la situación del juego y asigna puntajes según quién está más cerca de sus objetivos.
def evaluar(posicion_gato, posicion_raton, pos_cueva, turno_gato, prev_posiciones_raton):
    x_gato, y_gato = posicion_gato
    x_raton, y_raton = posicion_raton
    if pos_cueva:
        x_cueva, y_cueva = pos_cueva
    else:
        x_cueva, y_cueva = None, None
    
    if turno_gato:
        if posicion_gato == posicion_raton:
            return 1000  # El gato atrapó al ratón
        else:
            # Considerar la distancia inversa al ratón y a la cueva
            distancia_raton = abs(x_gato - x_raton) + abs(y_gato - y_raton)
            distancia_cueva = abs(x_gato - x_cueva) + abs(y_gato - y_cueva) if pos_cueva else 0
            # Predecir el movimiento del ratón basado en posiciones previas
            if prev_posiciones_raton:
                prediccion = prediccion_movimiento_raton(prev_posiciones_raton)
                distancia_prediccion = abs(x_gato - prediccion[0]) + abs(y_gato - prediccion[1])
                return -(distancia_raton + distancia_cueva + distancia_prediccion)
            return -(distancia_raton + distancia_cueva)  # Distancia inversa al ratón y a la cueva
    else:
        if pos_cueva and posicion_raton == pos_cueva:
            return -1000  # El ratón llegó a la cueva
        else:
            # Considerar la distancia a la cueva si está presente
            return abs(x_raton - x_cueva) + abs(y_raton - y_cueva) if pos_cueva else 0

def prediccion_movimiento_raton(prev_posiciones_raton):
    if len(prev_posiciones_raton) < 2:
        return prev_posiciones_raton[-1]
    delta_x = prev_posiciones_raton[-1][0] - prev_posiciones_raton[-2][0]
    delta_y = prev_posiciones_raton[-1][1] - prev_posiciones_raton[-2][1]
    prediccion = [prev_posiciones_raton[-1][0] + delta_x, prev_posiciones_raton[-1][1] + delta_y]
    return prediccion

#Se implementa el algoritmo Minimax para decidir el mejor movimiento del gato y del ratón 
#  para buscar el mejor movimiento posible 
# para el gato y el ratón, considerando 
# varios niveles de profundidad y utilizando poda alpha-beta para mejorar la eficiencia
def minimax(posicion_gato, posicion_raton, profundidad, es_turno_gato, tamano_tablero, pos_cueva, alpha, beta, prev_posiciones_raton):
    if profundidad == 0 or posicion_gato == posicion_raton or (pos_cueva and posicion_raton == pos_cueva):
        return evaluar(posicion_gato, posicion_raton, pos_cueva, es_turno_gato, prev_posiciones_raton)
    
    if es_turno_gato:
        mejor_valor = float('-inf')
        for movimiento in movimientos_posibles(posicion_gato, tamano_tablero):
            valor = minimax(movimiento, posicion_raton, profundidad - 1, False, tamano_tablero, pos_cueva, alpha, beta, prev_posiciones_raton)
            mejor_valor = max(mejor_valor, valor)
            alpha = max(alpha, valor)
            if beta <= alpha:
                break  # Poda beta
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for movimiento in movimientos_posibles(posicion_raton, tamano_tablero):
            nuevo_prev_posiciones_raton = prev_posiciones_raton + [movimiento]
            valor = minimax(posicion_gato, movimiento, profundidad - 1, True, tamano_tablero, pos_cueva, alpha, beta, nuevo_prev_posiciones_raton)
            mejor_valor = min(mejor_valor, valor)
            beta = min(beta, valor)
            if beta <= alpha:
                break  # Poda alpha
        return mejor_valor

#Encuentra el mejor movimiento para el gato usando Minimax
def mejor_movimiento_gato(posicion_gato, posicion_raton, tamano_tablero, pos_cueva, prev_posiciones_raton):
    mejor_valor = float('-inf')
    mejor_movimiento = None
    alpha = float('-inf')
    beta = float('inf')
    for movimiento in movimientos_posibles(posicion_gato, tamano_tablero):
        valor = minimax(movimiento, posicion_raton, 3, False, tamano_tablero, pos_cueva, alpha, beta, prev_posiciones_raton)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
        alpha = max(alpha, valor)
    return mejor_movimiento
#Encuentra el mejor movimiento para el raton usando Minimax
def mejor_movimiento_raton(posicion_raton, posicion_gato, tamano_tablero, pos_cueva, prev_posiciones_raton):
    mejor_valor = float('inf')
    mejor_movimiento = None
    alpha = float('-inf')
    beta = float('inf')
    for movimiento in movimientos_posibles(posicion_raton, tamano_tablero):
        nuevo_prev_posiciones_raton = prev_posiciones_raton + [movimiento]
        valor = minimax(posicion_gato, movimiento, 3, True, tamano_tablero, pos_cueva, alpha, beta, nuevo_prev_posiciones_raton)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
        beta = min(beta, valor)
    return mejor_movimiento

#Controla el flujo del juego, alternando turnos entre el gato y el ratón, 
#actualizando y mostrando el tablero en cada turno
def jugar_gato_raton(tamano_tablero, posicion_gato, posicion_raton):
    cueva = None
    tablero = crear_tablero(tamano_tablero)
    tablero = actualizar_tablero(tablero, posicion_gato, posicion_raton, cueva)
    mostrar_tablero(tablero)
    
    turno_gato = True
    tiempo_inicio = time.time()
    tiempo_ultima_cueva = tiempo_inicio
    turnos = 0
    prev_posiciones_raton = [posicion_raton]
    
    while posicion_gato != posicion_raton:
        tiempo_actual = time.time()
        if cueva is None and tiempo_actual - tiempo_inicio >= 10: # inicia el tiempo de aparicion de la cueva
            cueva = [random.randint(0, tamano_tablero - 1), random.randint(0, tamano_tablero - 1)]
            tiempo_ultima_cueva = tiempo_actual
            print("¡La cueva ha aparecido en:", cueva)
        elif cueva is not None and tiempo_actual - tiempo_ultima_cueva >= 30:# si pasaron mas de 30 segundos de la aparcion de la cueva le asigna otro lugar aleatorio
            cueva = [random.randint(0, tamano_tablero - 1), random.randint(0, tamano_tablero - 1)]
            tiempo_ultima_cueva = tiempo_actual
            print("¡La cueva ha cambiado de posición a:", cueva)
        
        if turno_gato:
            for _ in range(2 if turnos < 5 else 1):  # El gato se mueve dos veces por turno durante los primeros 5 turnos
                posicion_gato = mejor_movimiento_gato(posicion_gato, posicion_raton, tamano_tablero, cueva, prev_posiciones_raton)
                if posicion_gato == posicion_raton:
                    print("¡El gato atrapó al ratón!")
                    return
        else:
            posicion_raton = mejor_movimiento_raton(posicion_raton, posicion_gato, tamano_tablero, cueva, prev_posiciones_raton)
            prev_posiciones_raton.append(posicion_raton)
            if cueva and posicion_raton == cueva:
                print("¡El ratón llegó a la cueva!")
                return
        
        tablero = actualizar_tablero(tablero, posicion_gato, posicion_raton, cueva)
        mostrar_tablero(tablero)
        turno_gato = not turno_gato
        turnos += 1 #contar turnos trasncuridos
        time.sleep(1) #controlar velocidad del juego

if __name__ == "__main__":
    while True:
        tamano_tablero = int(input("Introduce el tamaño del tablero (mínimo 7): "))
        if tamano_tablero >= 7:
            break
        print("El tamaño del tablero debe ser al menos 7.")
    
    posicion_gato = [0, 0]
    posicion_raton = [tamano_tablero - 1, tamano_tablero - 1]
    num_ran = random.randint(1, 2)
    if num_ran == 1:
        posicion_raton[0] = posicion_raton[0] - 1
        posicion_raton[1] = posicion_raton[1]
    else:
        posicion_raton[0] = posicion_raton[0]
        posicion_raton[1] = posicion_raton[1] - 1
    
    jugar_gato_raton(tamano_tablero, posicion_gato, posicion_raton)
