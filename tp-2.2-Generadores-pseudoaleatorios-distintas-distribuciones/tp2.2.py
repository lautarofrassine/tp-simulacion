import matplotlib.pyplot as plt
import numpy as np
import math

# --- CONFIGURACIÓN GLOBAL DEL GCL ---
semilla = 12345
a = 1664525
c = 1013904223
m = 2**32




def generadorglc():
    global semilla
    semilla = (a * semilla + c) % m  # Actualiza la semilla global para la próxima llamada
    return semilla / m

# --- TRANSFORMACIONES (MÉTODOS DE NAYLOR) ---

def uniforme(minimo, maximo):
    """Genera un número pseudoaleatorio en el rango [minimo, maximo]"""
    valor = generadorglc()
    resultado_final = minimo + valor * (maximo - minimo)
    return resultado_final  # Retorna el valor en lugar de solo imprimirlo


def normal(media, desviacion):
    """Genera un número pseudoaleatorio con distribución Normal N(media, desviacion)"""
    # Suma 12 números independientes distribuidos U(0,1)
    suma = sum(generadorglc() for _ in range(12))
    
    # Transforma a Normal Estándar N(0,1)
    z = suma - 6  
    
    # Transforma a la Normal deseada N(media, desviacion)
    resultado_final = media + z * desviacion
    return resultado_final

def generar_empirica_discreta(valores, probabilidades):
    """
    Basado en el criterio de Naylor (pág. 136, ec. 4-154).
    valores: lista de b_i
    probabilidades: lista de p_i
    """
    r = generadorglc()  # Número uniforme entre 0 y 1
    acumulada = 0.0
    
    for i in range(len(valores)):
        acumulada += probabilidades[i]
        if r <= acumulada:
            return valores[i]
    return valores[-1]



def generar_binomial(n, p):
    """
    Traducido de la subrutina BINOM (Naylor, pág. 129)
    n: número de ensayos
    p: probabilidad de éxito
    """
    x = 0.0  # Inicializar contador de éxitos
    for i in range(int(n)):
        r = generadorglc()  # Generar R (uniforme 0-1)
        if r <= p:           # Si r <= p, es un éxito
            x += 1.0
    return x

# Ejecutar pruebas
print("--- PRUEBA DISTRIBUCIÓN UNIFORME ---")
print(f"Número uniforme entre 10 y 50: {uniforme(10, 50):.4f}")
print(f"Número uniforme entre 10 y 50: {uniforme(10, 50):.4f}\n")

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

def probar_empirica_discreta():
    # --- PARÁMETROS DEL TEST ---
    iteraciones = 10000
    b_i = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    p_i = [0.273, 0.037, 0.195, 0.009, 0.124, 0.058, 0.062, 0.151, 0.047, 0.044]
    muestra = [generar_empirica_discreta(b_i, p_i) for _ in range(iteraciones)]

    # 1. Cálculo de frecuencias relativas para el test
    frecuencias_obs = [muestra.count(v) / iteraciones for v in b_i]

    # 2. Visualización con Matplotlib
    plt.figure(figsize=(10, 5))
    x = range(len(b_i))

    # Comparación visual
    plt.bar(x, p_i, width=0.4, label='Probabilidad Original (Naylor)', alpha=0.5, color='gray')
    plt.bar([i + 0.4 for i in x], frecuencias_obs, width=0.4, label='Frecuencia Observada', color='blue')

    plt.xticks([i + 0.2 for i in x], b_i)
    plt.title(f'Test de Distribución Empírica Discreta ({iteraciones} iteraciones)')
    plt.xlabel('Valor (b_i)')
    plt.ylabel('Probabilidad / Frecuencia')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # 3. Test de error (Opcional para el informe)
    for i in range(len(b_i)):
        error = abs(p_i[i] - frecuencias_obs[i])
        print(f"Valor {b_i[i]}: Teórico={p_i[i]:.3f} | Obs={frecuencias_obs[i]:.3f} | Error={error:.4f}")

def probar_binomial():
   # --- PARÁMETROS DEL TEST ---
    n_ensayos = 20    # n (parámetro de la distribución)
    p_exito = 0.5     # p (parámetro de la distribución)
    iteraciones = 10000 # Cantidad de valores a generar para el test

    # 1. Generación de la muestra
    muestra = [generar_binomial(n_ensayos, p_exito) for _ in range(iteraciones)]

    # 2. Test Estadístico (Prueba de Momentos según Naylor)
    media_teorica = n_ensayos * p_exito
    varianza_teorica = n_ensayos * p_exito * (1 - p_exito)

    media_obs = sum(muestra) / iteraciones
    varianza_obs = sum((x - media_obs)**2 for x in muestra) / iteraciones

    print(f"--- Resultados del Test (n={n_ensayos}, p={p_exito}) ---")
    print(f"Media: Teoría={media_teorica:.4f} | Observada={media_obs:.4f}")
    print(f"Varianza: Teoría={varianza_teorica:.4f} | Observada={varianza_obs:.4f}")

    # 3. Test Visual con Matplotlib
    plt.figure(figsize=(10, 6))

    # Histograma de los datos generados (normalizado para comparar con probabilidad)
    plt.hist(muestra, bins=range(n_ensayos + 2), align='left', density=True, 
            alpha=0.6, color='skyblue', label='Frecuencia Experimental')

    # Línea de la distribución teórica
    x_teorico = list(range(n_ensayos + 1))
    y_teorico = [funcion_probabilidad_teorica(n_ensayos, p_exito, xi) for xi in x_teorico]
    plt.plot(x_teorico, y_teorico, 'ro-', label='f(x) Teórica (Naylor)')

    plt.title(f'Test Distribución Binomial ({iteraciones} iteraciones)')
    plt.xlabel('Número de éxitos (x)')
    plt.ylabel('Probabilidad f(x)')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()



def funcion_probabilidad_teorica(n, p, x):
    """Calcula f(x) = (n sobre x) * p^x * q^(n-x)"""
    combinaciones = math.comb(n, x)
    return combinaciones * (p**x) * ((1-p)**(n-x))



def test_distribucion_exponencial(media_esperada, cantidad_simulaciones=10000):
    """
    Esta función genera valores aleatorios con distribución exponencial
    y realiza automáticamente un testeo numérico y gráfico.
    """
    valores_exponenciales = []
    
    # 1. GENERACIÓN DE VALORES (Basado en el método de Naylor)
    for _ in range(cantidad_simulaciones):
        r = generadorglc()  # Número uniforme entre 0 y 1
        # Aplicación de la Transformada Inversa: x = -EX * log(r)
        x = -media_esperada * math.log(r)
        valores_exponenciales.append(x)
        
    # 2. TESTEO NUMÉRICO
    media_obtenida = sum(valores_exponenciales) / cantidad_simulaciones
    print(f"--- RESULTADOS DEL TESTEO ---")
    print(f"Media teórica ingresada (EX): {media_esperada}")
    print(f"Media empírica de los {cantidad_simulaciones} valores: {media_obtenida:.4f}")
    
    # 3. TESTEO GRÁFICO (Histograma)
    plt.hist(valores_exponenciales, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title(f"Testeo: Distribución Exponencial (Media = {media_esperada})")
    plt.xlabel("Valor de la variable (x)")
    plt.ylabel("Densidad de probabilidad f(x)")
    plt.grid(axis='y', alpha=0.75)
    
    # Esta instrucción es la que abre la ventana con el gráfico
    plt.show()

# Llama a esta función al final del archivo para ejecutarla
# probar_uniforme()

def generar_poisson(lmbda):
    """
    Genera un valor de variable aleatoria de Poisson.
    Basado en la subrutina POISSN de T. Naylor.
    Parámetro 'lmbda': Valor esperado o media de ocurrencias.
    """
    x = 0
    b = math.exp(-lmbda)  # Equivalente a B = EXP(-P) en Naylor
    tr = 1.0
    
    # Bucle infinito hasta que se cumpla la condición de Naylor
    while True:
        r = generadorglc()  # Aquí llamamos a tu propia función generadora
        tr = tr * r
        
        # Si el producto acumulado es menor que e^(-lambda), terminamos
        if tr < b:
            return x
        
        # Si no, sumamos 1 ocurrencia y volvemos a iterar
        x += 1

def test_distribucion_poisson(lmbda, cantidad_simulaciones=10000):



    """
    Realiza el testeo numérico y gráfico llamando a la función generar_poisson.
    """
    valores_poisson = []
    
    # 1. GENERACIÓN DE VALORES
    for _ in range(cantidad_simulaciones):
        valores_poisson.append(generar_poisson(lmbda))
        
    # 2. TESTEO NUMÉRICO
    media_obtenida = sum(valores_poisson) / cantidad_simulaciones
    print(f"--- RESULTADOS DEL TESTEO ---")
    print(f"Media teórica ingresada (Lambda): {lmbda}")
    print(f"Media empírica de los {cantidad_simulaciones} valores: {media_obtenida:.4f}")
    
    # 3. TESTEO GRÁFICO (Histograma de barras discretas)
    # Buscamos el valor máximo generado para crear las "cajas" (bins) de los enteros
    max_val = max(valores_poisson)
    bins_discretos = range(0, int(max_val) + 2)
    
    plt.hist(valores_poisson, bins=bins_discretos, density=True, alpha=0.7, color='lightgreen', edgecolor='black', align='left')
    plt.title(f"Testeo: Distribución de Poisson ($\lambda$ = {lmbda})")
    plt.xlabel("Número de ocurrencias (x)")
    plt.ylabel("Probabilidad / Frecuencia relativa")
    plt.xticks(range(0, int(max_val) + 1)) # Fuerza a que el eje X muestre solo números enteros
    plt.grid(axis='y', alpha=0.75)
    
    # Abre la ventana con el gráfico
    plt.show()

  # Puedes cambiar lambda para probar con diferentes valores

probar_empirica_discreta()





