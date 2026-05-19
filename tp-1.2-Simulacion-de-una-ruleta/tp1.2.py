import sys
import random
import matplotlib.pyplot as plt

if (
    len(sys.argv) != 13
    or sys.argv[1] != "-c"
    or sys.argv[3] != "-n"
    or sys.argv[5] != "-e"
    or sys.argv[7] != "-s"
    or sys.argv[9] != "-a"
    or sys.argv[11] != "-t"
    or int(sys.argv[2]) <= 0
    or int(sys.argv[4]) <= 0
    or not (sys.argv[6] in ["m", "d", "f", "p"])
    or int(sys.argv[8]) <= 0
    or int(sys.argv[10]) > int(sys.argv[8])
    or sys.argv[12] not in ["f", "i"]
):
    print(
        "Uso: python script.py -c <cantidad_corridas> -n <cantidad_tiradas> -e <estrategia (m=martingala/d=dalembert/f=fibonacci/p=paroli)> -s <saldo_inicial> -a <apuesta_inicial> -t <tipo_capital(f=finito/i=infinito)>"
    )
    sys.exit(1)


capital_infinito = True if sys.argv[12] == "i" else False
num_corridas = int(sys.argv[2])
num_tiradas = int(sys.argv[4])
estrategia_elegida = sys.argv[6]
saldo_inicial = int(sys.argv[8])
apuesta_inicial = int(sys.argv[10])
numeros_rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]


def tiradas():
    corridas = []
    for i in range(num_corridas):
        tiradas = []
        for j in range(num_tiradas):
            valor = random.randint(0, 36)
            tiradas.append(valor)
        corridas.append(tiradas)
    return corridas


def simulacion_martingala(
    listavalores,
):
    saldo = saldo_inicial
    apuesta = apuesta_inicial
    resultados_gano = []
    lista_saldos = []
    lista_apuestas = []
    bancarrotas_x = []
    bancarrotas_y = []
    for j in range(num_tiradas):
        if saldo < apuesta and capital_infinito == False:
            bancarrotas_x.append(j + 1)
            bancarrotas_y.append(saldo)
            apuesta = apuesta_inicial
            saldo = saldo_inicial

        lista_apuestas.append(apuesta)
        if listavalores[j] in numeros_rojos:
            resultados_gano.append(1)
            saldo += apuesta
            lista_saldos.append(saldo)
            apuesta = apuesta_inicial
        else:
            saldo -= apuesta
            resultados_gano.append(0)
            lista_saldos.append(saldo)
            apuesta = apuesta * 2

    return resultados_gano, lista_saldos, lista_apuestas, bancarrotas_x, bancarrotas_y


def simulacion_dalembert(listavalores):
    saldo = saldo_inicial
    apuesta = apuesta_inicial
    resultados_gano = []
    lista_saldos = []
    lista_apuestas = []
    bancarrotas_x = []
    bancarrotas_y = []

    for j in range(num_tiradas):
        if saldo < apuesta and capital_infinito == False:
            bancarrotas_x.append(j + 1)
            bancarrotas_y.append(saldo)
            apuesta = apuesta_inicial
            saldo = saldo_inicial
        lista_apuestas.append(apuesta)
        if listavalores[j] in numeros_rojos:
            saldo += apuesta
            lista_saldos.append(saldo)
            resultados_gano.append(1)
            if apuesta > apuesta_inicial:
                apuesta = apuesta - apuesta_inicial
        else:
            saldo -= apuesta
            lista_saldos.append(saldo)
            resultados_gano.append(0)
            apuesta = apuesta + apuesta_inicial

    return resultados_gano, lista_saldos, lista_apuestas, bancarrotas_x, bancarrotas_y


def simulacion_fibonacci(listavalores):
    saldo = saldo_inicial
    apuesta = apuesta_inicial
    resultados_gano = []
    lista_saldos = []
    lista_apuestas = []
    bancarrotas_x = []
    bancarrotas_y = []

    secuencia_fib = [1, 1]
    idx_fib = 0
    for i in range(1000):
        secuencia_fib.append(secuencia_fib[-1] + secuencia_fib[-2])

    for j in range(num_tiradas):
        if saldo < apuesta and capital_infinito == False:
            bancarrotas_x.append(j + 1)
            bancarrotas_y.append(saldo)
            apuesta = apuesta_inicial
            saldo = saldo_inicial
            idx_fib = 0
        lista_apuestas.append(apuesta)
        if listavalores[j] in numeros_rojos:
            saldo += apuesta
            idx_fib = max(0, idx_fib - 2)
            lista_saldos.append(saldo)
            resultados_gano.append(1)
            apuesta = apuesta_inicial * secuencia_fib[idx_fib]
        else:
            saldo -= apuesta
            lista_saldos.append(saldo)
            resultados_gano.append(0)
            idx_fib += 1
            apuesta = apuesta_inicial * secuencia_fib[idx_fib]

    return resultados_gano, lista_saldos, lista_apuestas, bancarrotas_x, bancarrotas_y


def simulacion_paroli(
    listavalores,
):
    saldo = saldo_inicial
    apuesta = apuesta_inicial
    resultados_gano = []
    lista_saldos = []
    lista_apuestas = []
    bancarrotas_x = []
    bancarrotas_y = []
    for j in range(num_tiradas):
        if saldo < apuesta and capital_infinito == False:
            bancarrotas_x.append(j + 1)
            bancarrotas_y.append(saldo)
            apuesta = apuesta_inicial
            saldo = saldo_inicial

        lista_apuestas.append(apuesta)
        if listavalores[j] in numeros_rojos:
            resultados_gano.append(1)
            saldo += apuesta
            lista_saldos.append(saldo)
            apuesta = apuesta * 2
        else:
            saldo -= apuesta
            resultados_gano.append(0)
            lista_saldos.append(saldo)
            apuesta = apuesta_inicial

    return resultados_gano, lista_saldos, lista_apuestas, bancarrotas_x, bancarrotas_y


def simulacion(listavalores, estrategia):

    for i in range(num_corridas):

        resultados_gano, lista_saldos, lista_apuestas, bancarrotas_x, bancarrotas_y = (
            simulacion_martingala(
                listavalores[i],
            )
            if estrategia == "m"
            else (
                simulacion_dalembert(listavalores[i])
                if estrategia == "d"
                else (
                    simulacion_fibonacci(listavalores[i])
                    if estrategia == "f"
                    else (
                        simulacion_paroli(listavalores[i])
                        if estrategia == "p"
                        else ([], [], [], [], [])
                    )
                )
            )
        )

        bancarrotas_x_total.append(bancarrotas_x)
        bancarrotas_y_total.append(bancarrotas_y)
        resultados_gano_total.append(resultados_gano)
        lista_saldos_total.append(lista_saldos)
        lista_apuestas_total.append(lista_apuestas)

        frecuencias_relativas = []
        for j in range(1, num_tiradas + 1):
            fr = sum(resultados_gano_total[i][:j]) / j
            frecuencias_relativas.append(fr)
        frecuencias_relativas_total.append(frecuencias_relativas)

    return (
        lista_saldos_total,
        frecuencias_relativas_total,
        bancarrotas_x_total,
        bancarrotas_y_total,
        lista_apuestas_total,
    )


def graficos(estrategia):

    estrategia = (
        "Martingala"
        if estrategia == "m"
        else (
            "d'Alembert"
            if estrategia == "d"
            else "Fibonacci" if estrategia == "f" else "Paroli"
        )
    )

    # Gráfico de evolución del saldo
    plt.figure(figsize=(10, 4))
    for i in range(num_corridas):
        plt.plot(
            range(1, num_tiradas + 1),
            lista_saldos_total[i],
            label=f"Corrida {i+1}",
            alpha=0.7,
        )
        if capital_infinito == False:
            plt.scatter(
                bancarrotas_x_total[i],
                bancarrotas_y_total[i],
                color="red",
                s=50,
                zorder=5,
                label=f"Bancarrotas detectadas ({len(bancarrotas_x_total[i])})",
            )
    plt.axhline(
        y=1000, color="red", linestyle="--", label=f"Saldo Inicial ({saldo_inicial})"
    )
    # plt.axhline(y=0, color="black", linestyle="-", label="Bancarrota")
    plt.xlabel("Iteración")
    plt.ylabel("Saldo")
    plt.title(f"Evolucion del saldo - {estrategia}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Gráfico de frecuencia relativa de ganar
    esperado = 18 / 37
    plt.figure(figsize=(10, 5))
    for i in range(num_corridas):
        plt.plot(
            range(1, num_tiradas + 1),
            frecuencias_relativas_total[i],
            alpha=0.7,
            label=f"Corrida {i+1}",
        )
    plt.axhline(
        y=esperado,
        color="blue",
        linestyle="--",
        label=f"Frecuencia esperada ({esperado:.4f})",
    )
    plt.xlabel("n (número de tiradas)")
    plt.ylabel("fr (frecuencia relativa)")
    plt.title(f"Frecuencia Relativa de Obtener Apuesta Favorable - {estrategia}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # grafico de evolución de las apuestas
    plt.figure(figsize=(10, 5))
    for i in range(num_corridas):
        plt.plot(lista_apuestas_total[i], alpha=0.7, label=f"Corrida {i+1}")
    plt.xlabel("Iteración")
    plt.ylabel("Monto de la apuesta")
    plt.title(f"Evolución de las apuestas - {estrategia}")
    plt.legend()
    plt.tight_layout()
    plt.show()


listavalores = tiradas()

lista_saldos_total = []
frecuencias_relativas_total = []
bancarrotas_x_total = []
bancarrotas_y_total = []
lista_apuestas_total = []
resultados_gano_total = []

simulacion(listavalores, estrategia_elegida)
graficos(estrategia_elegida)

# simulacion_dalembert(False)
# simulacion_fibonacci(False)
# simulacion_paroli(False)
