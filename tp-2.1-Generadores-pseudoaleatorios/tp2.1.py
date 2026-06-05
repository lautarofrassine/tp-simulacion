import random
import math
import numpy as np
import ctypes
import matplotlib.pyplot as plt

N = 250000  # que sea el cuadrado de algun numero, por la dimnesion de la imagen de test_bitmap


def generador_windows_rand():
    numeros = []
    msvcrt = ctypes.CDLL("msvcrt.dll")
    for _ in range(N):
        numeros.append(msvcrt.rand() / 32768)
    return numeros


def generador_python_random():
    numeros = []
    for i in range(N):
        numeros.append(random.random())
    return numeros


def generador_gcl(semilla, a, c, m):
    # Formula: X_{n+1} = (a * X_n + c) mod m
    numeros = []
    x = semilla
    for i in range(N):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros


def generador_cuadrados_medios(semilla):
    numeros = []
    x = semilla
    datos_esperados = len(str(semilla))

    for _ in range(N):
        cuadrado_str = str(x**2).zfill(datos_esperados * 2)
        mitad = len(cuadrado_str) // 2
        inicio = mitad - (datos_esperados // 2)
        fin = mitad + (datos_esperados // 2)

        x = int(cuadrado_str[inicio:fin])
        numeros.append(x / (10**datos_esperados))
    return numeros


def test_media(numeros, nombre_metodo):
    media_muestral = sum(numeros) / N
    media_esperada = 0.5
    varianza_teorica = 1 / 12
    Z = (media_muestral - media_esperada) / math.sqrt(
        varianza_teorica / N
    )  # desviacion estandar
    p_valor = 1.0 - math.erf(abs(Z) / math.sqrt(2.0))

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
    plt.plot(
        iteraciones,
        medias_acumuladas,
        color="blue",
        label="Media Muestral Acumulada",
        linewidth=1.5,
    )
    plt.axhline(
        y=0.5,
        color="red",
        linestyle="--",
        label="Media Teórica ($\mu = 0.5$)",
        linewidth=1.5,
    )
    plt.plot(
        iteraciones,
        limite_superior,
        color="gray",
        linestyle=":",
        label="Límites de Confianza (95%)",
    )
    plt.plot(iteraciones, limite_inferior, color="gray", linestyle=":")
    plt.fill_between(
        iteraciones,
        limite_inferior,
        limite_superior,
        color="gray",
        alpha=0.1,
        label="Región de Aceptación",
    )

    plt.text(
        0.02,
        0.95,
        texto_cuadro,
        transform=plt.gca().transAxes,
        fontsize=11,
        fontweight="bold",
        color=color_texto,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor=color_fondo,
            edgecolor=color_borde,
            alpha=0.9,
        ),
    )

    plt.title(
        f"Test de la Media - Convergencia ({nombre_metodo})",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Cantidad de Números Generados ($N$)", fontsize=12)
    plt.ylabel("Valor de la Media", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper right")
    plt.ylim(0.4, 0.6)

    plt.tight_layout()

    plt.show()

    plt.clf()
    plt.close("all")

    return {
        "media": media_muestral,
        "Z": Z,
        "p_valor": p_valor,
        "resultado": estado_test,
    }


def test_kolmogorov(numeros, nombre_metodo):

    cuantiles_muestrales = np.sort(numeros)
    cuantiles_teoricos = np.linspace(1 / N, 1, N)

    cuantiles_muestrales = np.sort(numeros)
    cuantiles_teoricos = np.linspace(1 / N, 1, N)
    distancias = np.abs(cuantiles_muestrales - cuantiles_teoricos)
    D = np.max(distancias)
    valor_critico = 1.36 / math.sqrt(N)
    if D <= valor_critico:
        estado_test = "Aceptado"
        texto_cuadro = (
            f"Método: {nombre_metodo}\n"
            f"QQ-Plot: ACEPTADO\n"
            f"Distancia D: {D:.4f}\n"
            f"D Crítico Máx: {valor_critico:.4f}"
        )
        color_fondo = "#d4edda"  # Verde claro
        color_borde = "#c3e6cb"
        color_texto = "#155724"
    else:
        estado_test = "Rechazado"
        texto_cuadro = (
            f"Método: {nombre_metodo}\n"
            f"QQ-Plot: RECHAZADO\n"
            f"Distancia D: {D:.4f}\n"
            f"D Crítico Máx: {valor_critico:.4f}"
        )
        color_fondo = "#f8d7da"  # Rojo claro
        color_borde = "#f5c6cb"
        color_texto = "#721c24"

    plt.figure(figsize=(7, 7))

    plt.scatter(
        cuantiles_teoricos,
        cuantiles_muestrales,
        s=1,
        color="black",
        alpha=0.6,
        label="Datos de la muestra",
    )

    plt.plot(
        [0, 1],
        [0, 1],
        color="red",
        linestyle="--",
        linewidth=1.5,
        label="Uniforme Teórica",
    )

    plt.text(
        0.05,
        0.95,
        texto_cuadro,
        transform=plt.gca().transAxes,
        fontsize=10,
        fontweight="bold",
        color=color_texto,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor=color_fondo,
            edgecolor=color_borde,
            alpha=0.9,
        ),
    )

    plt.title(
        f"Gráfico Q-Q (QQ-Plot) - {nombre_metodo}", fontsize=14, fontweight="bold"
    )
    plt.xlabel("Cuantiles Teóricos ($U(0,1)$)", fontsize=12)
    plt.ylabel("Cuantiles Muestrales (Datos)", fontsize=12)
    plt.xlim(-0.02, 1.02)
    plt.ylim(-0.02, 1.02)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="lower right")

    plt.tight_layout()
    plt.show()

    plt.clf()
    plt.close("all")

    return {"Distancia": D, "D Crítico": valor_critico, "resultado": estado_test}


def test_chicuadrado(numeros, nombre_metodo):
    k = 10
    limites_intervalos = np.linspace(0, 1, k + 1)
    frec_observadas, _ = np.histogram(numeros, bins=limites_intervalos)
    frec_esperada = N / k
    chi2 = 0.0
    for obs in frec_observadas:
        chi2 += ((obs - frec_esperada) ** 2) / frec_esperada
    valor_critico = 16.919

    if chi2 <= valor_critico:
        estado_test = "Aceptado"
        texto_cuadro = (
            f"Método: {nombre_metodo}\n"
            f"Chi-Cuadrado: ACEPTADO\n"
            f"Estadístico X2: {chi2:.2f}\n"
            f"Valor Crítico Max: {valor_critico}"
        )
        color_fondo = "#d4edda"  # Verde claro
        color_borde = "#c3e6cb"
        color_texto = "#155724"
    else:
        estado_test = "Rechazado"
        texto_cuadro = f"Método: {nombre_metodo}\nChi-Cuadrado: RECHAZADO\nEstadístico X2: {chi2:.2f}\nValor Crítico Max: {valor_critico}"
        color_fondo = "#f8d7da"  # Rojo claro
        color_borde = "#f5c6cb"
        color_texto = "#721c24"

    plt.figure(figsize=(10, 6))

    centros_barras = (limites_intervalos[:-1] + limites_intervalos[1:]) / 2
    ancho_barra = (1 / k) * 0.8  # Espaciado estético entre barras

    plt.bar(
        centros_barras,
        frec_observadas,
        width=ancho_barra,
        color="skyblue",
        edgecolor="black",
        alpha=0.7,
        label="Frecuencia Observada ($O_i$)",
    )

    plt.axhline(
        y=frec_esperada,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Frecuencia Esperada ($E_i = {int(frec_esperada)}$)",
    )

    plt.text(
        0.02,
        0.95,
        texto_cuadro,
        transform=plt.gca().transAxes,
        fontsize=11,
        fontweight="bold",
        color=color_texto,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor=color_fondo,
            edgecolor=color_borde,
            alpha=0.9,
        ),
    )

    plt.title(
        f"Test de Frecuencias Chi-Cuadrado - {nombre_metodo}",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Subintervalos en $[0, 1)$", fontsize=12)
    plt.ylabel("Cantidad de Números (Frecuencia)", fontsize=12)
    plt.xticks(limites_intervalos)
    plt.grid(True, linestyle="--", alpha=0.5, axis="y")
    plt.legend(loc="upper right")

    plt.ylim(0, max(frec_observadas) * 1.30)

    plt.tight_layout()
    plt.show()

    plt.clf()
    plt.close("all")

    return {"chi2_stat": chi2, "valor_critico": valor_critico, "resultado": estado_test}


def test_bitmap(numeros, nombre_metodo):
    # dimension es el tamaño de la imagen (tiene que ser un cuadrado)
    dimension = int(math.sqrt(N))

    datos_recortados = np.array(numeros[:N])

    # 2. Convertimos a Blanco y Negro absoluto usando un umbral (threshold) de 0.5
    # Si el número es >= 0.5 se vuelve 1 (blanco), si es menor se vuelve 0 (negro)
    mapa_bits = np.where(datos_recortados >= 0.5, 1, 0)

    # 3. Redimensionamos el vector plano para transformarlo en una matriz 2D (imagen)
    matriz_imagen = mapa_bits.reshape((dimension, dimension))

    # =========================================================================
    # CONFIGURACIÓN DE LA GRÁFICA
    # =========================================================================
    plt.figure(figsize=(6, 6))

    plt.imshow(matriz_imagen, cmap="gray", interpolation="nearest")

    plt.axis("off")

    plt.title(
        f"Test de Bitmap (Ruido Visual): {nombre_metodo}",
        fontsize=14,
        fontweight="bold",
    )

    plt.tight_layout()
    plt.show()

    plt.clf()
    plt.close("all")


gcl_nums = generador_gcl(12345, 1103515245, 12345, 2**31)
cm_nums = generador_cuadrados_medios(5121)
python_nums = generador_python_random()
windows_nums = generador_windows_rand()

gcl_media = test_media(gcl_nums, "GCL")
cm_media = test_media(cm_nums, "Cuadrados Medios")
python_media = test_media(python_nums, "Python Random")
windows_media = test_media(windows_nums, "Windows Rand")

gcl_kol = test_kolmogorov(gcl_nums, "GCL")
cm_kol = test_kolmogorov(cm_nums, "Cuadrados Medios")
python_kol = test_kolmogorov(python_nums, "Python Random")
windows_kol = test_kolmogorov(windows_nums, "Windows Rand")

test_bitmap(gcl_nums, "GCL")
test_bitmap(cm_nums, "Cuadrados Medios")
test_bitmap(python_nums, "Python Random")
test_bitmap(windows_nums, "Windows Rand")

gcl_chi = test_chicuadrado(gcl_nums, "GCL")
cm_chi = test_chicuadrado(cm_nums, "Cuadrados Medios")
python_chi = test_chicuadrado(python_nums, "Python Random")
windows_chi = test_chicuadrado(windows_nums, "Windows Rand")


resultados = [
    ["GCL", gcl_media["resultado"], gcl_kol["resultado"], gcl_chi["resultado"]],
    [
        "Cuadrados Medios",
        cm_media["resultado"],
        cm_kol["resultado"],
        cm_chi["resultado"],
    ],
    [
        "Python Random",
        python_media["resultado"],
        python_kol["resultado"],
        python_chi["resultado"],
    ],
    [
        "Windows Rand",
        windows_media["resultado"],
        windows_kol["resultado"],
        windows_chi["resultado"],
    ],
]


fig, ax = plt.subplots(figsize=(10, 3))
ax.axis("off")
tabla = ax.table(
    cellText=resultados,
    colLabels=["Método", "Test Media", "Kolmogorov-Smirnov", "Chi²"],
    cellLoc="center",
    loc="center",
)
tabla.auto_set_font_size(False)
tabla.set_fontsize(11)
tabla.scale(1.2, 2)
# Encabezados
for col in range(4):
    celda = tabla[(0, col)]
    celda.set_facecolor("#4472C4")
    celda.set_text_props(color="white", weight="bold")
# Colorear resultados
for fila in range(1, len(resultados) + 1):
    for col in range(1, 4):
        valor = str(tabla[(fila, col)].get_text().get_text()).lower()
        if "acept" in valor:
            tabla[(fila, col)].set_facecolor("#d4edda")
            tabla[(fila, col)].set_text_props(weight="bold")
        else:
            tabla[(fila, col)].set_facecolor("#f8d7da")
            tabla[(fila, col)].set_text_props(weight="bold")
plt.title(
    "Resumen de Resultados de las Pruebas Estadísticas",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
plt.tight_layout()
plt.show()
plt.clf()
plt.close("all")
