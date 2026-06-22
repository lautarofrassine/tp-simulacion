import simpy
import random

# Parámetros
LAMBDA = 4      # tasa de arribo
MU = 5          # tasa de servicio
TIEMPO_SIM = 1000

env = simpy.Environment()
servidor = simpy.Resource(env, capacity=1)


tiempos_cola = []
tiempos_sistema = []


def cliente(env, nombre, servidor):
    global tiempo_ocupado
    tiempo_ocupado = 0
    llegada = env.now

    with servidor.request() as req:
        yield req

        inicio_servicio = env.now
        tiempos_cola.append(inicio_servicio - llegada) ##agrego el tiempo de cola a la lista

        tiempo_servicio = random.expovariate(MU)
        tiempo_ocupado += tiempo_servicio
        yield env.timeout(tiempo_servicio)

        salida = env.now

        print(nombre,
              "esperó", inicio_servicio - llegada,
              "y estuvo", salida - llegada)
        
        tiempos_sistema.append(salida - llegada) ##agrego el tiempo en sistema a la lista
        

def generador_clientes(env, servidor):
    i = 0

    while True:
        i += 1

        env.process(cliente(env, f"C{i}", servidor))

        tiempo_entre_arribos = random.expovariate(LAMBDA)
        yield env.timeout(tiempo_entre_arribos)


env.process(generador_clientes(env, servidor))
env.run(until=TIEMPO_SIM)

##promedios

promedio_cola = sum(tiempos_cola) / len(tiempos_cola)
print("Promedio de tiempo en cola:", promedio_cola)

promedio_sistema = sum(tiempos_sistema) / len(tiempos_sistema)
print("Promedio de tiempo en sistema:", promedio_sistema)


##Utilización del servidor
utilizacion = tiempo_ocupado / TIEMPO_SIM
print("Utilización del servidor:", utilizacion)