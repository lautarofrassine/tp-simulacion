
import random
import matplotlib.pyplot as plt



numero_elegido = 11
tiradas = 100;
numeros_rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
def simulacion_martingala():

    bancarrotas_x = []
    bancarrotas_y = []

    
    saldo = 1000
    apuesta = 10
    lista_saldos = []
    cant_bancarrotas = 0 
    lista = []
    for i in range(tiradas):
        lista.append(random.randint(0,36))



    for indice, i in enumerate(lista):
        
        if  i in numeros_rojos:
            saldo += apuesta
            lista_saldos.append(saldo)
            apuesta = 10
        else:
            saldo -= apuesta
            apuesta = apuesta * 2
            lista_saldos.append(saldo)
        if saldo <= 0:
            bancarrotas_x.append(indice + 1)
            bancarrotas_y.append(saldo)
            cant_bancarrotas += 1
            apuesta = 10
            saldo = 1000
    

    plt.plot(lista_saldos)
    plt.axhline(y=1000, color='red', linestyle='--', label="Saldo Inicial")
    plt.axhline(y=0, color='black', linestyle='-', label="Bancarrota")

    if cant_bancarrotas > 0:
        plt.scatter(bancarrotas_x, bancarrotas_y, color='red', s=50, zorder=5, 
                    label=f"Bancarrotas detectadas ({len(bancarrotas_x)})")
    plt.xlabel("Iteración")
    plt.ylabel("Saldo")
    plt.title("Simulación de Martingala")
    plt.legend()
    plt.show()

def simulacion_dalembert():
    bancarrotas_x = []
    bancarrotas_y = []
    saldo = 1000
    apuesta = 10
    lista_saldos = []
    incremento = apuesta/2
    cant_bancarrotas = 0 
    lista = []
   
    for i in range(tiradas):
        lista.append(random.randint(0,36))



    for indice, i in enumerate(lista):
        if  i in numeros_rojos:
            saldo += apuesta
            lista_saldos.append(saldo)
            if apuesta > 10:
                apuesta = apuesta - incremento
            
        else:
            saldo -= apuesta
            apuesta = apuesta + incremento
            lista_saldos.append(saldo)
        if saldo <= 0:
            bancarrotas_x.append(indice + 1)
            bancarrotas_y.append(saldo)
            cant_bancarrotas += 1
            saldo = 1000
            apuesta = 10
            saldo = 1000
            apuesta = 10

    plt.plot(lista_saldos)
    plt.axhline(y=1000, color='red', linestyle='--', label="Saldo Inicial")
    plt.axhline(y=0, color='black', linestyle='-', label="Bancarrota")

    if cant_bancarrotas > 0:
        plt.scatter(bancarrotas_x, bancarrotas_y, color='red', s=50, zorder=5, 
                    label=f"Bancarrotas detectadas ({len(bancarrotas_x)})")
    plt.xlabel("Iteración")
    plt.ylabel("Saldo")
    plt.title("Simulación de d'Alembert")
    plt.legend()
    plt.show()

def simulacion_fibonacci():
    bancarrotas_x = []
    bancarrotas_y = []
    saldo = 1000
    lista_saldos = []
    cant_bancarrotas = 0 

    apuesta_base = 10
    
    secuencia_fib = [1, 1, 2, 3] 
    idx_fib = 0  
    apuesta = apuesta_base * secuencia_fib[idx_fib]
    
   
    lista = []
    for i in range(tiradas):
        lista.append(random.randint(0, 36))

    for indice, i in enumerate(lista):
        if i in numeros_rojos:
            saldo += apuesta
            
           
            idx_fib = max(0, idx_fib - 2)
            apuesta = apuesta_base * secuencia_fib[idx_fib]
        else:
            saldo -= apuesta
            
            
            idx_fib += 1
            
            
            if idx_fib >= len(secuencia_fib):
                siguiente_fib = secuencia_fib[-1] + secuencia_fib[-2]
                secuencia_fib.append(siguiente_fib)
                
            apuesta = apuesta_base * secuencia_fib[idx_fib]
            
        lista_saldos.append(saldo)
        
        
        if saldo <= 0:
            bancarrotas_x.append(indice + 1)
            bancarrotas_y.append(saldo)
            cant_bancarrotas += 1
            
            
            saldo = 1000
            idx_fib = 0
            apuesta = apuesta_base * secuencia_fib[idx_fib]

    plt.plot(lista_saldos, label="Evolución del Saldo", color="purple")
    plt.axhline(y=1000, color='red', linestyle='--', label="Saldo Inicial")
    plt.axhline(y=0, color='black', linestyle='-', label="Bancarrota")

    if cant_bancarrotas > 0:
        plt.scatter(bancarrotas_x, bancarrotas_y, color='red', s=50, zorder=5, 
                    label=f"Bancarrotas detectadas ({cant_bancarrotas})")
                    
    plt.xlabel("Iteración")
    plt.ylabel("Saldo")
    plt.title("Simulación de Estrategia Fibonacci")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()


simulacion_fibonacci()  