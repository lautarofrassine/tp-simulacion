import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN GLOBAL DEL GCL ---
semilla = 12345
a = 1664525
c = 1013904223
m = 2**32

def siguiente_uniforme():
    global semilla
    semilla = (a * semilla + c) % m  # Actualiza la semilla global para la próxima llamada
    return semilla / m

# --- TRANSFORMACIONES (MÉTODOS DE NAYLOR) ---

def uniforme(minimo, maximo):
    """Genera un número pseudoaleatorio en el rango [minimo, maximo]"""
    valor = siguiente_uniforme()
    resultado_final = minimo + valor * (maximo - minimo)
    return resultado_final  # Retorna el valor en lugar de solo imprimirlo

def normal(media, desviacion):
    """Genera un número pseudoaleatorio con distribución Normal N(media, desviacion)"""
    # Suma 12 números independientes distribuidos U(0,1)
    suma = sum(siguiente_uniforme() for _ in range(12))
    
    # Transforma a Normal Estándar N(0,1)
    z = suma - 6  
    
    # Transforma a la Normal deseada N(media, desviacion)
    resultado_final = media + z * desviacion
    return resultado_final

# --- PRUEBAS Y VERIFICACIÓN ---

def probar_normal():
    # 1. Generar una muestra grande (por ejemplo, 10,000 números)
    media_deseada = 0
    desviacion_deseada = 1
    muestras = [normal(media_deseada, desviacion_deseada) for _ in range(10000)]

    # 2. Verificación Estadística
    media_calculada = np.mean(muestras)
    desviacion_calculada = np.std(muestras)

    print("--- PRUEBA DISTRIBUCIÓN NORMAL ---")
    print(f"Media teórica: {media_deseada} | Calculada: {media_calculada:.4f}")
    print(f"Desviación teórica: {desviacion_deseada} | Calculada: {desviacion_calculada:.4f}\n")

    # 3. Verificación Visual (Histograma)
    plt.figure(figsize=(8, 5))
    plt.hist(muestras, bins=50, density=True, alpha=0.6, color='g', edgecolor='black')

    # Dibujar la línea de la distribución normal teórica para comparar
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = (1 / (desviacion_deseada * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media_deseada) / desviacion_deseada)**2)
    plt.plot(x, p, 'r', linewidth=2, label='Normal Teórica')

    plt.title('Verificación del Método de Naylor (Irwin-Hall)')
    plt.xlabel('Valores')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Ejecutar pruebas
print("--- PRUEBA DISTRIBUCIÓN UNIFORME ---")
print(f"Número uniforme entre 10 y 50: {uniforme(10, 50):.4f}")
print(f"Número uniforme entre 10 y 50: {uniforme(10, 50):.4f}\n")

def probar_uniforme():
    # 1. Generar una muestra grande entre 10 y 50
    min_deseado = 10
    max_deseado = 50
    muestras = [uniforme(min_deseado, max_deseado) for _ in range(10000)]

    # 2. Verificación Estadística
    # La media teórica de una uniforme es (min + max) / 2
    media_teorica = (min_deseado + max_deseado) / 2
    media_calculada = np.mean(muestras)

    print("--- PRUEBA DISTRIBUCIÓN UNIFORME ---")
    print(f"Media teórica: {media_teorica} | Calculada: {media_calculada:.4f}\n")

    # 3. Verificación Visual (Histograma)
    plt.figure(figsize=(8, 5))
    # bins=40 para que coincida con el rango de 40 unidades entre 10 y 50
    plt.hist(muestras, bins=40, density=True, alpha=0.6, color='b', edgecolor='black')

    # Dibujar la línea de la densidad teórica uniforme: 1 / (max - min)
    densidad_teorica = 1 / (max_deseado - min_deseado)
    plt.axhline(y=densidad_teorica, color='r', linestyle='-', linewidth=2, label='Uniforme Teórica')

    plt.title(f'Verificación de Distribución Uniforme [{min_deseado}, {max_deseado}]')
    plt.xlabel('Valores')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, densidad_teorica * 1.5) # Ajustar margen superior del gráfico
    plt.show()

# Llama a esta función al final del archivo para ejecutarla
probar_uniforme()