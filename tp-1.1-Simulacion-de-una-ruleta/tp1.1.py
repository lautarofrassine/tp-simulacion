import sys
import random
import statistics
import matplotlib.pyplot as plt

if (
    len(sys.argv) != 7
    or sys.argv[1] != "-c"
    or sys.argv[3] != "-n"
    or sys.argv[5] != "-e"
    or int(sys.argv[2]) <= 0
    or int(sys.argv[4]) <= 0
    or not (0 <= int(sys.argv[6]) <= 36)
):
    print(
        "Uso: python script.py -c <cantidad_corridas> -n <cantidad_tiradas> -e <numero_elegido>"
    )
    sys.exit(1)

c = int(sys.argv[2])
n = int(sys.argv[4])
e = int(sys.argv[6])


def tiradas():
    corridas = []
    for i in range(c):
        tiradas = []
        for j in range(n):
            valor = random.randint(0, 36)
            tiradas.append(valor)
        corridas.append(tiradas)
    return corridas


def frecuencia_relativa(listavalores):
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


def promedio_observado(listavalores):

    vp_c = []
    for i in range(c):
        vp_t = []
        for j in range(n):
            vp_t.append(statistics.mean(listavalores[i][: j + 1]))
        vp_c.append(vp_t)
    return vp_c


def calcular_varianza(listavalores):

    vv_c = []
    for i in range(c):
        vv_t = []
        for j in range(n):
            vv_t.append(statistics.pvariance(listavalores[i][: j + 1]))

        vv_c.append(vv_t)

    return vv_c


def calcular_desvioestandar(listavalores):
    dv_c = []
    for i in range(c):
        dv_t = []
        for j in range(n):
            dv_t.append(statistics.pstdev(listavalores[i][: j + 1]))
        dv_c.append(dv_t)
    return dv_c


# Generacion de todos los valores de las tiradas de todas las corridas
listavalores = tiradas()

# Calculo de los valores necesarios para generar los graficos

frecuenciarelativa = frecuencia_relativa(listavalores)
promedioobservado = promedio_observado(listavalores)
varianza = calcular_varianza(listavalores)
desvioestandar = calcular_desvioestandar(listavalores)

#
# Gráficas de una sola corrida
#

plt.figure(figsize=(10, 4))
plt.plot(range(1, n + 1), frecuenciarelativa[0], label="Corrida 1", alpha=0.7)
plt.axhline(y=1 / 37, color="blue", linestyle="-", label="fr esperada (1/37 ≈ 0.02703)")
plt.title("Frecuencia relativa acumulada respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Frecuencia relativa")
plt.legend()
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 4))
plt.plot(range(1, n + 1), promedioobservado[0], label="Corrida 1", alpha=0.7)
plt.axhline(y=18, color="blue", linestyle="-", label="VP Esperado (18)")
plt.title("Valor Promedio Acumulado respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Valor Promedio")
plt.legend()
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 4))
plt.plot(range(1, n + 1), varianza[0], label="Corrida 1", alpha=0.7)
plt.axhline(y=114.67, color="blue", linestyle="-", label="Varianza Esperada (114.67)")
plt.title("Varianza Acumulada respecto al número de tiradas")
plt.xlabel("Número de tiradas")
plt.ylabel("Varianza")
plt.legend()
plt.tight_layout()
plt.show()


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
# Graficos de todas las corridas comparadas
#
#

if c > 1:
    plt.figure(figsize=(10, 4))
    for i in range(c):
        plt.plot(
            range(1, n + 1),
            frecuenciarelativa[i],
            label=f"Corrida {i+1}",
            alpha=0.7,
        )
    plt.axhline(
        y=1 / 37, color="blue", linestyle="-", label="fr esperada (1/37 ≈ 0.02703)"
    )
    plt.title("Frecuencia relativa acumulada respecto al número de tiradas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Frecuencia relativa")
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 4))
    for i in range(c):
        plt.plot(
            range(1, n + 1), promedioobservado[i], label=f"Corrida {i+1}", alpha=0.7
        )
    plt.axhline(y=18, color="blue", linestyle="-", label="VP Esperado (18)")
    plt.title("Valor Promedio Acumulado respecto al número de tiradas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Valor Promedio")
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 4))
    for i in range(c):
        plt.plot(range(1, n + 1), varianza[i], label=f"Corrida {i+1}", alpha=0.7)
    plt.axhline(
        y=114.67, color="blue", linestyle="-", label="Varianza Esperada (114.67)"
    )
    plt.title("Varianza Acumulada respecto al número de tiradas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Varianza")
    plt.legend()
    plt.tight_layout()
    plt.show()

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
