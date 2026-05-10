#ASI COMO ESTA LAS TIRADAS SE CREAN POR CADA FUNCION, LO QUE HACE QUE LOS GRAFICOS NO SEAN COMPARABLES ENTRE SI Y QUE SEA
#MAS COSTOSO EN TERMINOS DE RENDIMIENTO, SOLO HABRIA QUE CREAR UNA FUNCION PARA SIMULAR LAS TIRADAS Y LISTO, ES FACIL PERO ME DA PAJA
#DESPUES LO HAGO
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#BORRAR ESTO PARA ENVIARLO




import random
import statistics 
import matplotlib.pyplot as plt


#lista para almacenar los valores obtenidos en cada tirada
listavalores = []

#cantidad de tiradas
n=3700

numero_elegido = 11

 
desvio_n = []
dv = [] 
vv = [] 

fr_teorica = 1/37


def frecuencia_relativa():
    listavalores = []
    exitos = 0
    fr_n = []
    for i in range(1, n + 1):
        valor = random.randint(0, 36)
        listavalores.append(valor)
        
        if valor == numero_elegido:
            exitos += 1
        
        fr_n.append(exitos / i)

    return fr_n


def promedio_observado():

    listavalores = []
    vp_n = []
    for i in range(1, n + 1):
        valor = random.randint(0, 36)
        listavalores.append(valor)
        
        vp_n.append(sum(listavalores) / i)

    return vp_n


def calculardesvioestandar():
    listavalores = []

    for i in range(1, n + 1):
        
        
        valor = random.randint(0, 36)
        listavalores.append(valor)
    
        dv.append(statistics.pstdev(listavalores))

    plt.figure(figsize=(10, 4))
    plt.plot(dv, label='Desvío Observado', color='red')
    plt.axhline(y=10.68, color='blue', linestyle='-', label='Desvío Esperado (10.68)')
    plt.title('Número de tiradas')
    plt.ylabel('Desvío Estandar')
    plt.legend()
    plt.tight_layout()
    plt.show()
        


def calcular_varianza_poblacional():
    listavalores = []

    for i in range(1, n + 1):
        
        
        valor = random.randint(0, 36)
        listavalores.append(valor)
    
        vv.append(statistics.pvariance(listavalores))

    plt.figure(figsize=(10, 4))
    plt.plot(vv, label='Varianza Observada', color='red')
    plt.axhline(y=114.67, color='blue', linestyle='-', label='Varianza Esperada (114.67)')
    plt.title('Número de tiradas')
    plt.ylabel('Varianza')
    plt.legend()
    plt.tight_layout()
    plt.show()


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
    plt.bar(numeros, frecuencias, color='seagreen', edgecolor='black', alpha=0.8)

    # Línea de frecuencia esperada (n / 37)
    esperado = n / 37
    plt.axhline(y=esperado, color='red', linestyle='--', label=f'Frecuencia Esperada ({esperado:.2f})')

    # Estética del gráfico
    plt.title(f'Frecuencia Absoluta de cada número en {n} tiradas', fontsize=14)
    plt.xlabel('Número de la Ruleta', fontsize=12)
    plt.ylabel('Cantidad de veces que salió', fontsize=12)
    plt.xticks(numeros) # Muestra todos los números del 0 al 36
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
        



#Calculo la frecuencia relativa y genero grafico
frecuenciarelativa = frecuencia_relativa()

plt.figure(figsize=(10, 4))
plt.plot(frecuenciarelativa, label='Frecuencia Relativa', color='red')
plt.axhline(y=1/37, color='blue', linestyle='-', label='Esperada (1/37)')
plt.title('Número de tiradas')
plt.ylabel('Frecuencia relativa')
plt.legend()
plt.tight_layout()
plt.show()

#calculo el valor promedio y genero grafico
promedioobservado = promedio_observado()

plt.figure(figsize=(10, 4))
plt.plot(promedioobservado, label='Promedio Observado', color='red')
plt.axhline(y=18, color='blue', linestyle='-', label='VP Esperado (18)')
plt.title('Número de tiradas')
plt.ylabel('Valor Promedio')
plt.legend()
plt.tight_layout()
plt.show()

#Calculo el desvio y genero grafico
calculardesvioestandar()

calcular_varianza_poblacional()

frecuencia_absoluta()















"""
#simulo la ruleta en 3700 tiradas 
for i in range(1, n + 1):
    valor = random.randint(0, 36)
    listavalores.append(valor)
    
    
    if valor == numero_elegido:
        exitos += 1
    
    #sumo a la lista de frecuencia relativa
    fr_n.append(exitos / i)
    
    #sumo a la lista de valor promedio
    vp_n.append(sum(listavalores) / i)

    
    if i > 1:  
        dv.append(statistics.stdev(listavalores))
    else:
        dv.append(0)  

    
    if i > 1:  
        vv.append(statistics.variance(listavalores))
    

frecuencias = [0] * 37 

for valor in listavalores:
    frecuencias[valor] += 1




plt.figure(figsize=(10, 4))
plt.plot(fr_n, label='Frecuencia Relativa', color='red')
plt.axhline(y=1/37, color='blue', linestyle='-', label='Esperada (1/37)')
plt.title('Número de tiradas')
plt.ylabel('Frecuencia relativa')
plt.legend()
plt.tight_layout()
plt.show()



plt.figure(figsize=(10, 4))
plt.plot(vp_n, label='Promedio Observado', color='red')
plt.axhline(y=18, color='blue', linestyle='-', label='VP Esperado (18)')
plt.title('Número de tiradas')
plt.ylabel('Valor Promedio')
plt.legend()
plt.tight_layout()
plt.show()



"""








"""
plt.figure(figsize=(10, 4))
plt.plot(dv, label='Desvío Observado', color='red')
plt.axhline(y=10.68, color='blue', linestyle='-', label='Desvío Esperado (10.68)')
plt.title('Número de tiradas')
plt.ylabel('Desvío Estandar')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(vv, label='Varianza Observada', color='red')
plt.axhline(y=114.67, color='blue', linestyle='-', label='Varianza Esperada (114.67)')
plt.title('Número de tiradas')
plt.ylabel('Varianza')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.bar(range(37), frecuencias, color='red')
plt.title('Frecuencia Absoluta de cada número')
plt.xlabel('Número')
plt.ylabel('Frecuencia Absoluta')
plt.xticks(range(37))
plt.tight_layout()
plt.show()
"""


"""   
print(listavalores)    
moda = statistics.mode(listavalores)
mediana = statistics.median(listavalores)
desvio = statistics.stdev(listavalores)
mean = statistics.mean(listavalores)
varianza = statistics.variance(listavalores)
desvio_poblacional = statistics.pstdev(listavalores)

print("La moda es: ", moda)
print("La media es: ", mediana)
print("El desvio estandar es: ", desvio)
print("La media es: ", mean)
print("La varianza es: ", varianza)
print("El desvio poblacional es: ", desvio_poblacional)
 """   

        

