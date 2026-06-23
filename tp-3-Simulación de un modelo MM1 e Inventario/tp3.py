import simpy
import random
from collections import defaultdict

# Parámetros
LAMBDA = 4      # tasa de arribo
MU = 5          # tasa de servicio
TIEMPO_SIM = 1000
CAPACIDADES_A_PROBAR = [0, 2, 5, 10, 50]

def simular_sistema_finito(tamano_cola_max):
    env = simpy.Environment()
    servidor = simpy.Resource(env, capacity=1)

    # Contadores para denegación de servicio
    clientes_arribados = 0
    clientes_rechazados = 0

    def cliente(env, nombre, servidor):
        nonlocal clientes_rechazados
        llegada = env.now

        # --- REEMPLAZA EL IF ANTERIOR POR ESTE BLOQUE ---
        # Capacidad total del sistema = Clientes en el servidor + Clientes en la cola
        clientes_actuales_sistema = servidor.count + len(servidor.queue)
        capacidad_max_sistema = 1 + tamano_cola_max # 1 del servidor + espacio de cola

        if clientes_actuales_sistema >= capacidad_max_sistema:
            clientes_rechazados += 1
            return 
        # ------------------------------------------------

        with servidor.request() as req:
            yield req
            
            # Tu lógica actual de simulación
            tiempo_servicio = random.expovariate(MU)
            yield env.timeout(tiempo_servicio)

    def generador_clientes(env, servidor):
        nonlocal clientes_arribados
        i = 0
        while True:
            i += 1
            clientes_arribados += 1
            env.process(cliente(env, f"C{i}", servidor))
            
            tiempo_entre_arribos = random.expovariate(LAMBDA)
            yield env.timeout(tiempo_entre_arribos)

    # Ejecución de la corrida
    env.process(generador_clientes(env, servidor))
    env.run(until=TIEMPO_SIM)

    # Cálculo de la probabilidad de denegación
    prob_denegacion = clientes_rechazados / clientes_arribados if clientes_arribados > 0 else 0
    
    return clientes_arribados, clientes_rechazados, prob_denegacion






def simular_una_corrida(LAMBDA):
    """Ejecuta una sola corrida y retorna los resultados."""
    env = simpy.Environment()
    servidor = simpy.Resource(env, capacity=1)

    tiempos_cola = []
    tiempos_sistema = []

    # Diccionario para acumular el tiempo que la cola pasa con 'n' clientes
    tiempo_en_estado_cola = defaultdict(float)
    ultimo_cambio_cola = 0.0

    # Utilización
    tiempo_ocupado = 0

    # Clientes promedio
    clientes_sistema = 0
    clientes_cola = 0

    area_sistema = 0
    area_cola = 0

    ultimo_evento_sistema = 0
    ultimo_evento_cola = 0

    def actualizar_sistema(env):
        nonlocal area_sistema, ultimo_evento_sistema, clientes_sistema

        area_sistema += clientes_sistema * (env.now - ultimo_evento_sistema)
        ultimo_evento_sistema = env.now


    def actualizar_cola(env):
        nonlocal area_cola, ultimo_evento_cola, clientes_cola

        area_cola += clientes_cola * (env.now - ultimo_evento_cola)
        ultimo_evento_cola = env.now


    def cliente(env, nombre, servidor):
        nonlocal tiempo_ocupado
        nonlocal ultimo_cambio_cola
        nonlocal clientes_sistema
        nonlocal clientes_cola

        llegada = env.now

        # --- CAMBIO EN LA COLA: Alguien se suma a la cola ---
        n_antes_de_entrar = len(servidor.queue)
        tiempo_en_estado_cola[n_antes_de_entrar] += env.now - ultimo_cambio_cola
        ultimo_cambio_cola = env.now

        # entra al sistema
        actualizar_sistema(env)
        clientes_sistema += 1

        # si el servidor está ocupado, entra a cola
        if servidor.count >= servidor.capacity:
            actualizar_cola(env)
            clientes_cola += 1

        with servidor.request() as req:
            yield req

            # sale de la cola y comienza servicio
            if clientes_cola > 0:
                actualizar_cola(env)
                clientes_cola -= 1

            # --- CAMBIO EN LA COLA: Alguien sale de la cola para ser atendido ---
            n_antes_de_atender = len(servidor.queue) + 1
            tiempo_en_estado_cola[n_antes_de_atender] += env.now - ultimo_cambio_cola
            ultimo_cambio_cola = env.now

            inicio_servicio = env.now

            tiempos_cola.append(inicio_servicio - llegada)

            tiempo_servicio = random.expovariate(MU)
            tiempo_ocupado += tiempo_servicio

            yield env.timeout(tiempo_servicio)

            salida = env.now

            tiempos_sistema.append(salida - llegada)

            # sale del sistema
            actualizar_sistema(env)
            clientes_sistema -= 1


    def generador_clientes(env, servidor):
        i = 0

        while True:
            i += 1

            env.process(cliente(env, f"C{i}", servidor))

            tiempo_entre_arribos = random.expovariate(LAMBDA)
            yield env.timeout(tiempo_entre_arribos)


    env.process(generador_clientes(env, servidor))
    env.run(until=TIEMPO_SIM)

    # Al terminar, asegurar que se registre el tiempo del último estado hasta el fin de la simulación
    n_final = len(servidor.queue)
    tiempo_en_estado_cola[n_final] += TIEMPO_SIM - ultimo_cambio_cola

    # Actualizar áreas hasta el final de la simulación
    actualizar_sistema(env)
    actualizar_cola(env)

    # Calcular promedios
    promedio_cola = sum(tiempos_cola) / len(tiempos_cola) if tiempos_cola else 0
    promedio_sistema = sum(tiempos_sistema) / len(tiempos_sistema) if tiempos_sistema else 0
    utilizacion = tiempo_ocupado / TIEMPO_SIM
    promedio_clientes_cola = area_cola / TIEMPO_SIM
    promedio_clientes_sistema = area_sistema / TIEMPO_SIM

    # Calcular probabilidades de n clientes en cola
    probs_cola = {}
    for n in range(0, 11):
        probs_cola[n] = tiempo_en_estado_cola[n] / TIEMPO_SIM

    # Retornar diccionario con resultados
    return {
        "promedio_cola": promedio_cola,
        "promedio_sistema": promedio_sistema,
        "utilizacion": utilizacion,
        "promedio_clientes_cola": promedio_clientes_cola,
        "promedio_clientes_sistema": promedio_clientes_sistema,
        "probs_cola": probs_cola
    }


def simular(LAMBDA, num_corridas=30):
    """Ejecuta múltiples corridas y calcula promedios."""
    print(f"\n{'='*70}")
    print(f"Ejecutando {num_corridas} corridas...")
    print(f"{'='*70}")

    # Listas para acumular resultados de cada corrida
    resultados_corridas = []

    # Ejecutar múltiples corridas
    for i in range(1, num_corridas + 1):
        print(f"Corrida {i}/{num_corridas}...", end=" ", flush=True)
        resultado = simular_una_corrida(LAMBDA)
        resultados_corridas.append(resultado)
        print("✓")

    # Calcular promedios de todas las corridas
    promedio_cola_final = sum(r["promedio_cola"] for r in resultados_corridas) / num_corridas
    promedio_sistema_final = sum(r["promedio_sistema"] for r in resultados_corridas) / num_corridas
    utilizacion_final = sum(r["utilizacion"] for r in resultados_corridas) / num_corridas
    promedio_clientes_cola_final = sum(r["promedio_clientes_cola"] for r in resultados_corridas) / num_corridas
    promedio_clientes_sistema_final = sum(r["promedio_clientes_sistema"] for r in resultados_corridas) / num_corridas

    # Promediar las probabilidades
    probs_cola_final = {}
    for n in range(0, 11):
        probs_cola_final[n] = sum(r["probs_cola"][n] for r in resultados_corridas) / num_corridas

    # --- MOSTRAR RESULTADOS FINALES ---
    print("\n" + "="*70)
    print("--- RESUMEN DE RESULTADOS (PROMEDIO DE 30 CORRIDAS) ---")
    print("="*70)
    print(f"Promedio de clientes en el sistema: {promedio_clientes_sistema_final:.4f}")
    print(f"Promedio de clientes en cola:      {promedio_clientes_cola_final:.4f}")
    print(f"Tiempo promedio en sistema:        {promedio_sistema_final:.4f}")
    print(f"Tiempo promedio en cola:           {promedio_cola_final:.4f}")
    print(f"Utilización del servidor:          {utilizacion_final:.4f}")

    print("\nProbabilidad de encontrar n clientes en cola")
    for n in range(0, 11):
        prob = probs_cola_final[n]
        print(f"P(Nq = {n}) = {prob:.4f}")


MU = 5
TIEMPO_SIM = 1000

tasas_arribo = [
    ("25%", 0.25 * MU),
    ("50%", 0.50 * MU),
    ("75%", 0.75 * MU),
    ("100%", 1.00 * MU),
    ("125%", 1.25 * MU)
]

for porcentaje, lambda_actual in tasas_arribo:

    rho = lambda_actual / MU

    print("\n" + "="*70)
    print(f"TASA DE ARRIBO: {porcentaje}")
    print(f"λ = {lambda_actual:.2f} | μ = {MU} | ρ = {rho:.2f}")
    print("="*70)

    simular(lambda_actual)