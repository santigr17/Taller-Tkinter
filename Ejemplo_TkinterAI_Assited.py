# -----------------------------------------
# Ejemplo Tkinter completo con Pillow y Canvas
# -----------------------------------------

from tkinter import *
from PIL import Image, ImageTk
import threading
import winsound
import os
from tkinter import messagebox
import time

# -----------------------------------------
# Función para cargar imágenes con Pillow
# -----------------------------------------
def cargarImg(nombre, size=None):
    ruta = os.path.join('img', nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra la imagen: {ruta}")
    img = Image.open(ruta)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# -----------------------------------------
# Música
# -----------------------------------------
def stop_music():
    img_tk = cargarImg("musicbtn.png", size=(80,80))
    canvas.itemconfig(song_img_item, image=img_tk)
    canvas.song_img_tk = img_tk
    winsound.PlaySound(None, winsound.SND_ASYNC)

def play_song(filename, imgfile):
    stop_music()
    img_tk = cargarImg(imgfile, size=(80,80))
    canvas.itemconfig(song_img_item, image=img_tk)
    canvas.song_img_tk = img_tk  # mantener referencia
    threading.Thread(target=winsound.PlaySound, args=(filename, winsound.SND_ASYNC)).start()

# -----------------------------------------
# Ventana del juego
# -----------------------------------------
def VentanaJuego(nombre_jugador):
    root.withdraw()  # esconder ventana principal

    juego = Toplevel()
    juego.title("Juego Misiles")
    juego.minsize(800,600)
    juego.resizable(width=NO,height=NO)

    C_juego = Canvas(juego, width=800, height=600)
    C_juego.pack()

    # Fondo del juego
    bg_img = cargarImg("fondo1.png", size=(800,600))
    C_juego.create_image(0,0,anchor='nw', image=bg_img)
    C_juego.bg_img = bg_img

    # Label del jugador
    L_nombre = Label(C_juego, text=f"Jugador:\n {nombre_jugador}", font=('Agency FB',16),
                     fg='white', bg='#353a4e')
    L_nombre.place(x=30, y=120)

    # Variables globales
    global flag_base_destruida, flag_misil, clicks, ataques
    flag_base_destruida = False
    flag_misil = True
    clicks = 0
    ataques = 0
    # Label de misiles usados
    L_clicks = Label(C_juego, text=clicks, font=('Agency FB',11), fg='white', bg='#353a4e')
    L_clicks.place(x=140, y=29)

    # Función para crear un misil
    def crearmisil(i):
        global flag_misil, flag_base_destruida
        flag_misil = True
        flag_base_destruida = False

        posx = 50 * i
        posy = 0
        misil_img = cargarImg("bomba.png", size=(30,60))
        misil_item = C_juego.create_image(posx, posy, anchor='nw', image=misil_img)
        C_juego.misil_img = misil_img  # mantener referencia

        # Click sobre misil
        def on_click(event):
            global flag_misil, clicks
            clicks+=1
            L_clicks.config(text=clicks)
            items = C_juego.find_overlapping(event.x, event.y, event.x, event.y)
            if misil_item in items:
                flag_misil = False
        C_juego.bind('<Button-1>', on_click)

        # Movimiento del misil
        def move(posy):
            global flag_misil, flag_base_destruida
            if posy > 490:
                flag_misil = False
                flag_base_destruida = True
                return
            if flag_misil:
                C_juego.coords(misil_item, posx, posy)
                C_juego.update()
                time.sleep(0.02)
                move(posy+3)
        move(posy)
        C_juego.delete(misil_item)
        return flag_base_destruida

    # Función para ejecutar ataque
    def ataque_aux(i):
        if i >= 16:
            return True
        elif crearmisil(i):
            return False
        else:
            global ataques
            ataques += 1
            return ataque_aux(i+1)

    def ataque():
        result = ataque_aux(0)
        if result:
            messagebox.showinfo("Felicidades", "¡Felicidades has ganado!")
        else:
            yesno = messagebox.askyesno("Confirmar", "¿Jugar de nuevo?")
            if yesno:
                threading.Thread(target=ataque).start()

    # Botón volver
    def back():
        juego.destroy()
        root.deiconify()
    Btn_back = Button(C_juego, text="Atrás", bg="white", fg="green", command=back)
    Btn_back.place(x=100,y=560)

    # Iniciar ataque en hilo
    threading.Thread(target=ataque).start()

# -----------------------------------------
# Ventana principal
# -----------------------------------------
root = Tk()
root.title("Taller Tkinter")
root.minsize(800,600)
root.resizable(width=NO,height=NO)

canvas = Canvas(root, width=800, height=600)
canvas.pack()

# Fondo del menú
bg_img = cargarImg("menu_bg.png", size=(800,600))
canvas.create_image(0,0,anchor='nw', image=bg_img)
canvas.bg_img = bg_img

# Texto About
about = """Instituto Tecnologico de Costa Rica
Computer Engineering
Tutorías taller de programación
*AI Assited
Ejemplo de música en Windows
Juego destrucción de misiles
Fecha de emisión: 05/03/2018
Ultima modificación: 26/03/2026
Version: 2.0.0
"""
Label(canvas, text=about, font=('Agency FB',16), bg='#78b7e8', fg='white', borderwidth=10, justify='left').place(x=0, y=150)

# Entrada del nombre
Label(canvas, text="Ingrese su nombre:", font=('Agency FB',14), bg='#c0cfd6', fg='white').place(x=330,y=425)
E_nombre = Entry(canvas, width=20, font=('Agency FB',14))
E_nombre.place(x=330,y=450)

# Imagen de canción
song_img_tk = cargarImg("musicbtn.png", size=(80,80))
song_img_item = canvas.create_image(400,500, anchor='nw', image=song_img_tk)
canvas.song_img_tk = song_img_tk

# Botones de canciones
Button(root, text="Canción 1", bg="#c0cfd6", fg="white",
       command=lambda: play_song("song1.wav","img1.png")).place(x=100,y=550)
Button(root, text="Canción 2", bg="#c0cfd6", fg="white",
       command=lambda: play_song("song2.wav","img2.png")).place(x=200,y=550)
Button(root, text="Parar", bg="#c0cfd6", fg="white", command=stop_music).place(x=300,y=550)

# Botón iniciar juego
def empezar_juego():
    nombre = E_nombre.get()
    VentanaJuego(nombre)

btnPlayImg = cargarImg("play.png", size=(80,80))
Button(root, text="Juego", image=btnPlayImg, fg="#c0cfd6", command=empezar_juego).place(x=560,y=470)

root.mainloop()