"""
____________________________________________
Tutorías de taller de programación          *
                                            *
Ejemplo de música en Windows                *
Juego destrucción de misiles                *
Version de python: 3.6.0                    *
Santiago Gamboa Ramírez                     *
2017                                        *
____________________________________________*
"""
#           _____________________________
#__________/BIBLIOTECAS
from tkinter import *
from threading import Thread
import threading
import winsound
import os
import random
import time
#           ____________________________
#__________/Código

#           ____________________________
#__________/Variable global
global flag_back #Si se desea parar un hilo antes de que se termine la ejecución
global flag_misil #Capturar que se tocó la pantalla y se debe destruir el misil del hilo

#           ____________________________
#__________/Función para cargar imagenes
def cargarImg(nombre):
    ruta=os.path.join('img',nombre)
    imagen=PhotoImage(file=ruta)
    return imagen
#           ____________________________
#__________/Música
def Song1():
    winsound.PlaySound('song1.wav', winsound.SND_ASYNC)
def Song2():
    winsound.PlaySound('song2.wav', winsound.SND_ASYNC)


#           ____________________________
#__________/Ventana Principal
root=Tk()
root.title('Taller Tkinter')
root.minsize(800,600)
root.resizable(width=NO,height=NO)
        
#           ______________________________
#__________/Se crea un lienzo para objetos
C_root=Canvas(root, width=800,height=600, bg='black')
C_root.place(x=0,y=0)

#           ____________________________
#__________/Cargar una imagen
CE=cargarImg("logo.gif")
imagen_cancion=Label(C_root,bg='white')
imagen_cancion.place(x=50,y=10)
imagen_cancion.config(image=CE)

#           ____________________________
#__________/funcion para el boton mute
def off():
    winsound.PlaySound(None, winsound.SND_ASYNC)

#           ________________________________________________________________
#__________/funcion para reroducir una cancion y cambiar la imagen del label
def play2():
    off()
    imagen2 = cargarImg("img2.gif")
    imagen_cancion.config(image=imagen2)
    p=Thread(target=Song1,args=())
    p.start()
    root.mainloop()
    
#           ________________________________________________________________
#__________/funcion para reroducir una cancion y cambiar la imagen del label
def play1():
    off()
    imagen = cargarImg("img1.gif") 
    imagen_cancion.config(image=imagen)
    p=Thread(target=Song2,args=())
    p.start()
    root.mainloop()

#           ____________________________
#__________/Crear una nueva ventana
def VentanaJuego():
    root.withdraw()

    juego=Toplevel()
    juego.title('EJEMPLO')
    juego.minsize(800,600)
    juego.resizable(width=NO, height=NO)
    
    C_juego=Canvas(juego, width=800,height=600, bg='light blue')
    C_juego.place(x=0,y=0)

    fondoImg=cargarImg('fondo1.gif')
    F_juego=Label(C_juego, image=fondoImg,bg='light blue')
    F_juego.photo=fondoImg
    F_juego.place(x=0,y=0)  
  

#           ___________________________________
#__________/Función que ejecuta 20 veces el hilo
    def crearmilsil():

        img_bomba=cargarImg('bomba.gif')
        bomba=Label(C_juego, image=img_bomba,bg='light blue')
        bomba.photo=img_bomba
        
#           _____________________________
#__________/Bandera para detener el misil
        global flag_misil
        flag_misil=True
        posx= random.randrange(50,750)
        velocidad_misil=random.randrange(1,10)
        posy=0
        bomba.place(x=posx,y=0)
        
#           ______________________________________
#__________/Capturar un click sobre el label bomba
        def onClick(event):
            global flag_misil
            flag_misil=False

        bomba.bind('<Button-1>',onClick)
        
#           ____________________________
#__________/Funcion que mueve un misil
        while(posy<490 and flag_misil and (not pausa)):
            posy+=velocidad_misil
            bomba.place(x=posx,y=posy)
            time.sleep(0.01)

        destruido=False
        if (not pausa):
            bomba.destroy()
            if(posy>=490):
                destruido=True
        return destruido
    
#           ___________________________________
#__________/Ciclo del hilo que crea los misiles
    def ataque():
        global pausa
        pausa=False
        result=True
        for i in range(20):
            if(pausa):
                break
            if(crearmilsil()):
                result=False
                break

        if(result):
            print("Felicidades has ganado")
        else:
            print("Mala suerte has perdido")

#           _____________________________
#__________/Volver a la ventana principal
    def back():
        global pausa
        pausa=True
        juego.destroy()
        root.deiconify()
        
#           __________________________________________
#__________/Se crea un hilo para controlar los misiles
            
    p=Thread(target=ataque,args=())
    p.start()
    
    
#           ____________________________
#__________/Boton volver pantalla juego
    
    Btn_back = Button(C_juego,text='Atras',command=back,bg='white',fg='blue')
    Btn_back.place(x=100,y=560)    
    
    
        
#           ____________________________
#__________/Botones de ventana principal

Btn_song1 = Button(C_root,text='Cancion 1',command=play1,bg='white',fg='blue')
Btn_song1.place(x=100,y=450)

Btn_song2=Button(C_root,text='Cancion 2',command=play2,bg='white',fg='blue')
Btn_song2.place(x=200,y=450)

Btn_mute=Button(C_root,text='Parar ',command=off,bg='white',fg='blue')
Btn_mute.place(x=300,y=450)

Btn_hilos = Button(C_root,text='Ejemplo',command=VentanaJuego,bg='white',fg='blue')
Btn_hilos.place(x=400,y=450)
root.mainloop()
