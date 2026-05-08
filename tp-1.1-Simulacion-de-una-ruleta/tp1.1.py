

import random
import statistics 

import matplotlib.pyplot as plt


valor = random.randint(0, 36)

print(valor)


listavalores = []
listafrecuenciasrelativas = []
n=3700
numero_elegido = 11
exitos = 0

fr_n = [] 
vp_n = [] 
dv = [] 
vv = [] 

for i in range(1, n + 1):
    valor = random.randint(0, 36)
    listavalores.append(valor)
    
    
    if valor == numero_elegido:
        exitos += 1
    
    
    fr_n.append(exitos / i)
    
    
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

        

