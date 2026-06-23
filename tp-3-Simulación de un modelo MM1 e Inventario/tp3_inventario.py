import simpy
import random
import numpy as np

# --- PARÁMETROS (Justificables en el informe) ---
TIEMPO_SIM = 365        # 1 año de simulación
CORRIDAS = 30           # Exigido por enunciado
COSTO_PEDIDO_FIJO = 100 # Por orden
COSTO_MANTENIMIENTO = 2 # Por unidad por día
COSTO_FALTANTE = 5      # Por unidad faltante por día

s_MIN = 20              # Punto de reorden
S_MAX = 100             # Capacidad máxima

def simulacion_inventario(env, s, S, metricas):
    inventario = S
    
    # Acumuladores de área para integrales de costo
    area_mantenimiento = 0
    area_faltante = 0
    ultimo_cambio = 0
    ordenes_totales = 0

    def actualizar_areas():
        nonlocal area_mantenimiento, area_faltante, ultimo_cambio
        dt = env.now - ultimo_cambio
        if inventario > 0:
            area_mantenimiento += inventario * dt
        elif inventario < 0:
            area_faltante += abs(inventario) * dt
        ultimo_cambio = env.now

    # Proceso 1: Arribo de Clientes (Demanda)
    def clientes():
        nonlocal inventario
        while True:
            # Arribos aleatorios (Ej: cada 1 o 2 días promedio)
            yield env.timeout(random.expovariate(1.0)) 
            actualizar_areas()
            
            demanda = random.randint(1, 10) # Cantidad pedida aleatoria
            inventario -= demanda

    # Proceso 2: Revisión de Inventario y Pedidos (Control)
    def control_inventario():
        nonlocal inventario, ordenes_totales
        while True:
            yield env.timeout(7) # Revisión semanal, por ejemplo
            actualizar_areas()
            
            if inventario < s:
                cantidad_a_pedir = S - inventario
                ordenes_totales += 1
                # Simular demora de entrega (Lead Time) de 2 días
                env.process(entrega_pedido(cantidad_a_pedir))

    def entrega_pedido(cantidad):
        nonlocal inventario
        yield env.timeout(2) # Tiempo que tarda el proveedor
        actualizar_areas()
        inventario += cantidad

    # Registrar los procesos en SimPy
    env.process(clientes())
    env.process(control_inventario())
    env.run(until=TIEMPO_SIM)
    
    # Asegurar el cálculo final hasta el tiempo de corte
    actualizar_areas()

    # Cálculos económicos de la corrida
    c_orden = ordenes_totales * COSTO_PEDIDO_FIJO
    c_mant = area_mantenimiento * COSTO_MANTENIMIENTO
    c_falt = area_faltante * COSTO_FALTANTE
    
    metricas['orden'].append(c_orden)
    metricas['mantenimiento'].append(c_mant)
    metricas['faltante'].append(c_falt)
    metricas['total'].append(c_orden + c_mant + c_falt)

# --- CICLO PRINCIPAL (30 Corridas) ---
metricas_totales = {'orden': [], 'mantenimiento': [], 'faltante': [], 'total': []}

for _ in range(CORRIDAS):
    env = simpy.Environment()
    simulacion_inventario(env, s_MIN, S_MAX, metricas_totales)

# --- IMPRESIÓN DE RESULTADOS PROMEDIO ---
print(f"=== RESULTADOS PROMEDIO TRAS {CORRIDAS} CORRIDAS ===")
print(f"Costo de Orden Promedio:        {np.mean(metricas_totales['orden']):.2f}")
print(f"Costo de Mantenimiento Promedio: {np.mean(metricas_totales['mantenimiento']):.2f}")
print(f"Costo de Faltante Promedio:      {np.mean(metricas_totales['faltante']):.2f}")
print(f"--------------------------------------------------")
print(f"Costo Total Promedio:            {np.mean(metricas_totales['total']):.2f}")