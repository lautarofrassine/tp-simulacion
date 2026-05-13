

"""
Algunas anotaciones del experimento (las pongo por si hay que agregarlas al informe en latex despues las sacamos de aca):
Experimento aleatorio: Girar la ruleta una vez
Espacio muestral: {0, 1, 2, ..., 36}
Variable aleatoria X: Número que sale en la ruleta
Tipo de variable aleatoria: Discreta
Distribución de probabilidad: Uniforme discreta
P(X=x) = 1/37 para x en {0, 1, 2, ..., 36}
Frecuencia relativa esperada: 1/37 ≈ 0.02703
Valor promedio esperado (teorico): E[X] = (0 + 1 + 2 + ... + 36) / 37 = 18
Varianza poblacional esperada (teorica): σ² = ((0-18)² + (1-18)² + ... + (36-18)²) / 37 ≈ 114.67
Desvío estándar poblacional esperado (teorico): σ = raiz cuadrada(varianza) ≈ 10.68

"""

import random
import statistics
import matplotlib.pyplot as plt

# cantidad de tiradas
n = 30

# cantidad de corridas
c = 4

# numero elegido
e = 11


desvio_n = []
dv = []


def tiradas():
    corridas = []
    for i in range(c):
        tiradas = []
        for j in range(n):
            valor = random.randint(0, 36)
            tiradas.append(valor)
        corridas.append(tiradas)
    return corridas


def frecuencia_relativa(listavalores,c):
    fr_c = []
    for i in range(c):
        exitos = 0
        fr_t = []
        for j in range(n):
            if listavalores[i][j] == e:
                exitos += 1
            fr_t.append(exitos / ((j + 1)))
        fr_c.append(fr_t)
    return fr_c


def promedio_observado(listavalores, c):

    vp_c = []
    for i in range(c):
        vp_t = []
        for j in range(n):
            vp_t.append(statistics.mean(listavalores[i][: j + 1]))
        vp_c.append(vp_t)
    return vp_c


def calcular_varianza(listavalores, c):

    vv_c = []
    for i in range(c):
        vv_t = []
        for j in range(n):
            vv_t.append(statistics.pvariance(listavalores[i][: j + 1]))

        vv_c.append(vv_t)

    return vv_c


def calcular_desvioestandar(listavalores, c):
    dv_c = []
    for i in range(c):
        dv_t = []
        for j in range(n):
            dv_t.append(statistics.pstdev(listavalores[i][: j + 1]))
        dv_c.append(dv_t)
    return dv_c


def frecuencia_absoluta():
    listavalores = []
    frecuencias = [0] * 37

    for i in range(1, n + 1):
        valor = random.randint(0, 36)
        listavalores.append(valor)

        frecuencias[valor] += 1

    plt.figure(figsize=(12, 6))
    numeros = list(range(37))

    # Creamos las barras
    plt.bar(numeros, frecuencias, color="seagreen", edgecolor="black", alpha=0.8)

    # Línea de frecuencia esperada (n / 37)
    esperado = n / 37
    plt.axhline(
        y=esperado,
        color="red",
        linestyle="--",
        label=f"Frecuencia Esperada ({esperado:.2f})",
    )

    # Estética del gráfico
    plt.title(f"Frecuencia Absoluta de cada número en {n} tiradas", fontsize=14)
    plt.xlabel("Número de la Ruleta", fontsize=12)
    plt.ylabel("Cantidad de veces que salió", fontsize=12)
    plt.xticks(numeros)  # Muestra todos los números del 0 al 36
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.legend()

    plt.tight_layout()
    plt.show()


# Generacion de todos los valores de las tiradas de todas las corridas
listavalores = tiradas()


#
#
#A partir de aca se generan los graficos con una sola corrida
#
#

frecuenciarelativa = frecuencia_relativa(listavalores, 1)

plt.figure(figsize=(10, 4))
plt.plot(
    range(1, n + 1),
    frecuenciarelativa[0],
    label="Corrida 1",
    alpha=0.7
)
plt.axhline(y=1 / 37, color="blue", linestyle="-", label="fr esperada (1/37 ≈ 0.02703)")
plt.title("Frecuencia relativa acumulada respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Frecuencia relativa")
plt.legend()
plt.tight_layout()
plt.show()


promedioobservado = promedio_observado(listavalores,1)

plt.figure(figsize=(10, 4))

plt.plot(range(1, n + 1), promedioobservado[0], label="Corrida 1", alpha=0.7)
plt.axhline(y=18, color="blue", linestyle="-", label="VP Esperado (18)")
plt.title("Valor Promedio Acumulado respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Valor Promedio")
plt.legend()
plt.tight_layout()
plt.show()


varianza = calcular_varianza(listavalores,4)

plt.figure(figsize=(10, 4))

plt.plot(range(1, n + 1), varianza[0], label="Corrida 1", alpha=0.7)
plt.axhline(y=114.67, color="blue", linestyle="-", label="Varianza Esperada (114.67)")
plt.title("Varianza Acumulada respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Varianza")
plt.legend()
plt.tight_layout()
plt.show()

desvioestandar = calcular_desvioestandar(listavalores,1)

plt.figure(figsize=(10, 4))

plt.plot(range(1, n + 1), desvioestandar[0], label="Corrida 1", alpha=0.7)
plt.axhline(y=10.68, color="blue", linestyle="-", label="Desvío Esperado (10.68)")
plt.title("Desvío Estándar Acumulado respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Desvío Estandar")
plt.legend()
plt.tight_layout()
plt.show()







#
#
#A partir de aca se generan los graficos con varias tiradas
#
#

# Calculo frecuencias relativas y genero grafico
frecuenciarelativa = frecuencia_relativa(listavalores, c)

plt.figure(figsize=(10, 4))
for i in range(c):
    plt.plot(
        range(1, n + 1),
        frecuenciarelativa[i],
        label=f"Corrida {i+1}",
        alpha=0.7,
    )
plt.axhline(y=1 / 37, color="blue", linestyle="-", label="fr esperada (1/37 ≈ 0.02703)")
plt.title("Frecuencia relativa acumulada respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Frecuencia relativa")
plt.legend()
plt.tight_layout()
plt.show()

# calculo valores promedios y genero grafico
promedioobservado = promedio_observado(listavalores,4)

plt.figure(figsize=(10, 4))
for i in range(c):
    plt.plot(range(1, n + 1), promedioobservado[i], label=f"Corrida {i+1}", alpha=0.7)
plt.axhline(y=18, color="blue", linestyle="-", label="VP Esperado (18)")
plt.title("Valor Promedio Acumulado respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Valor Promedio")
plt.legend()
plt.tight_layout()
plt.show()

# Calculo varianzas y genero grafico
varianza = calcular_varianza(listavalores,4)

plt.figure(figsize=(10, 4))
for i in range(c):
    plt.plot(range(1, n + 1), varianza[i], label=f"Corrida {i+1}", alpha=0.7)
plt.axhline(y=114.67, color="blue", linestyle="-", label="Varianza Esperada (114.67)")
plt.title("Varianza Acumulada respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Varianza")
plt.legend()
plt.tight_layout()
plt.show()

# Calculo el desvio y genero grafico
desvioestandar = calcular_desvioestandar(listavalores,4)

plt.figure(figsize=(10, 4))
for i in range(c):
    plt.plot(range(1, n + 1), desvioestandar[i], label=f"Corrida {i+1}", alpha=0.7)
plt.axhline(y=10.68, color="blue", linestyle="-", label="Desvío Esperado (10.68)")
plt.title("Desvío Estándar Acumulado respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Desvío Estandar")
plt.legend()
plt.tight_layout()
plt.show()


