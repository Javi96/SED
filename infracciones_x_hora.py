# -*- coding: utf-8 -*-


'''
    Utilizando el contenido del fichero "infractions_db", genera una gráfica en tiempo real que muestra
    el número de infracciones que se han detectado para cada hora.
'''


#Imports necesarios.
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import load_infractions


# Creamos la figura que se va a dibujar.
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

#Lista de elementos que representarán el contenido de los ejes x e y de la gráfica.
xs = []
ys = []

#Esta función se llamará de forma periódica. De esta forma, se irán mostrando las actualizaciones en la gráfica.
def animate(i, xs, ys):
    ax.clear()
    xs=[]
    ys=[]
    
     #Cargamos las infracciones que almacena el sistema.
    infractions=load_infractions('infractions_db')
    
    result={}    

    #Para cada hora, obtenemos el número de infracciones que han sucedido.
    for k, v in infractions.items():
        #v es una lista de pares. El segundo elemento es la fecha de la infracción.
        for x in v:
            date=x[1].split('_')[3]
            if date in result:
                result[date]=result[date] +1
            else:
                result[date]=1
                
    for k,v in result.items():
        xs.append(k)
        ys.append(v)

    #Dibujamos el contenido de las listas xs e ys.
    ax.clear()
    ax.plot(xs, ys)

    #Especificamos el formato de la gráfica.
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Número de infracciones por día')
    plt.ylabel('Número de infracciones')    
    plt.xlabel('Hora')

#Especificamos cómo se llamará a la función "animate" de forma periódica y mostramos la gráfica.
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()





    
