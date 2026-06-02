import random
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def generador_gcl(semilla, a, c, m, iteraciones):
    #Formula: X_{n+1} = (a * X_n + c) mod m
    numeros = []
    x = semilla
    for i in range(iteraciones):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros


def generador_cuadrados_medios(semilla, iteraciones):
    numeros = []
    x = semilla
    datos_esperados = len(str(semilla)) 
    
    for _ in range(iteraciones):
        cuadrado_str = str(x ** 2).zfill(datos_esperados * 2) # hace q llene d 0 hasta el doble de la longitud de la semilla (esasi el metodo)
        # extraemos la parte central del cuadrado
        mitad = len(cuadrado_str) // 2
        inicio = mitad - (datos_esperados // 2)
        fin = mitad + (datos_esperados // 2)
        
        x = int(cuadrado_str[inicio:fin])
        numeros.append(x / (10 ** datos_esperados))
    return numeros

def test_media(numeros, nombre_metodo):
    N = len(numeros)
    media_muestral = sum(numeros) / N
    media_esperada = 0.5
    varianza_teorica = 1 / 12 # la distribucion uniforme tiene una varianza de 1/12, hay una demostracion probabilistica por ahi
    Z = (media_muestral - media_esperada) / math.sqrt(varianza_teorica / N)  #desviacion estandar
    p_valor = 2 * (1 - stats.norm.cdf(abs(Z)))
      # con el p-valor se puede determinar si se acepta o rechaza el generador, si el p-valor es menor que 0.05, se rechaza
    
   # =========================================================================
    # 2. GENERACIÓN Y APERTURA DEL GRÁFICO
    # =========================================================================
    if p_valor >= 0.05:
        estado_test = "Aceptado"
        texto_cuadro = f"Resultado: ACEPTADO\np-valor: {p_valor:.4f}\nZ: {Z:.4f}"
        color_fondo = "#d4edda"  # Verde claro
        color_borde = "#c3e6cb"
        color_texto = "#155724"
    else:
        estado_test = "Rechazado"
        texto_cuadro = f"Resultado: RECHAZADO\np-valor: {p_valor:.4f}\nZ: {Z:.4f}"
        color_fondo = "#f8d7da"  # Rojo claro
        color_borde = "#f5c6cb"
        color_texto = "#721c24"
    iteraciones = np.arange(1, N + 1)
    medias_acumuladas = np.cumsum(numeros) / iteraciones
    
    desvio_teorico = math.sqrt(varianza_teorica)
    limite_superior = 0.5 + 1.96 * (desvio_teorico / np.sqrt(iteraciones))
    limite_inferior = 0.5 - 1.96 * (desvio_teorico / np.sqrt(iteraciones))
    
    plt.figure(figsize=(10, 6))
    
    # Trazado de datos y bandas
    plt.plot(iteraciones, medias_acumuladas, color='blue', label='Media Muestral Acumulada', linewidth=1.5)
    plt.axhline(y=0.5, color='red', linestyle='--', label='Media Teórica ($\mu = 0.5$)', linewidth=1.5)
    plt.plot(iteraciones, limite_superior, color='gray', linestyle=':', label='Límites de Confianza (95%)')
    plt.plot(iteraciones, limite_inferior, color='gray', linestyle=':')
    plt.fill_between(iteraciones, limite_inferior, limite_superior, color='gray', alpha=0.1, label='Región de Aceptación')

    plt.text(
        0.02, 0.95, texto_cuadro,
        transform=plt.gca().transAxes,
        fontsize=11,
        fontweight='bold',
        color=color_texto,
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=color_fondo, edgecolor=color_borde, alpha=0.9)
    )
    
    # Formato básico
    plt.title(f'Test de la Media - Convergencia ({nombre_metodo})', fontsize=14, fontweight='bold')
    plt.xlabel('Cantidad de Números Generados ($N$)', fontsize=12)
    plt.ylabel('Valor de la Media', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper right')
    plt.ylim(0.4, 0.6) 
    
    plt.tight_layout()
    
    # 1. Abrimos la ventana del gráfico
    plt.show() 
    
    # 2. Forzamos el cierre y limpieza total de la memoria gráfica al cerrar la ventana
    plt.clf()
    plt.close('all')
    
    return {
        "media": media_muestral,
        "Z": Z,
        "p_valor": p_valor,
        "resultado": estado_test
    }

N = 15000 
gcl_nums = generador_gcl(12345, 1103515245, 12345, 2**31, N)
cm_nums = generador_cuadrados_medios(5121, N) #la semilla d 4 digitos debe ser

python_nums = [random.random() for _ in range(N)]
test_media(gcl_nums, "GCL")
test_media(cm_nums, "Cuadrados Medios")
test_media(python_nums, "Python Random")