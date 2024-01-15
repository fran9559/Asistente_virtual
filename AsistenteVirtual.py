import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import os
import subprocess as sub
import threading as th
from tkinter import *
from PIL import Image, ImageTk
from links import paginas, programas, comandos

main_window = Tk()
main_window.title("Asistente Virtual") ## title de la aplicacion
main_window.geometry("800x600") ## formato 
main_window.resizable(0,0) ## que no se pueda ampliar
main_window.config(bg="black") ## color de fondo

Label_title = Label(main_window, text= "Asistente Virtual",bg="black" , fg="white",
                    font=("Arial", 30, "bold"))
Label_title.pack(pady=5)

cargar_imagen = ImageTk.PhotoImage(Image.open("fotos/inteligencia-artifi.jpg"))
imagen_asistente = Label(main_window, image=cargar_imagen)
imagen_asistente.pack(pady=5)


# variables a usar

nombre = "asistente"
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[2].id)
engine.setProperty("rate", 145)

# funcion de voz

def talk(text):
    engine.say(text)
    engine.runAndWait()

# funcion para escuchar

def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("listener")    
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)

    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()

    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")

    return rec


def run_asistente():
    N = True
    while N == True:
        try:
            rec = listen()
            rec_finish = listen()
        except UnboundLocalError:
            print("No entendi, intenta de nuevo")
            continue

        # Funcion reproducir video youtube
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)

        # funcion buscar en wikiperia
        elif "buscar" in rec:
            search = rec.replace("buscar", "")
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ": " + wiki)
            talk(wiki)

        # funcion entrar pagina web
        elif "abrir" in rec:
            for pagina in paginas:
                if pagina in rec:
                    sub.call(f"start msedge.exe {paginas[pagina]}", shell=True)
                    talk(f"abriendo {pagina}")
            for programa in programas:
                if programa in rec:
                    talk(f"abiendo {programa}")
                    os.popen(programas[programa])

        # funcion escribir notas
        elif "escribe" in rec:
            try:
                with open("nota.txt", "a") as f:
                    writes(f)

            except FileNotFoundError as e:
                file = open("nota.txt", "w")
                write = file

        # funcion para salir
        elif 'salir' in rec:
            print("ok, nos vemos")
            #talk("ok " + nombreUsuario + " nos vemos")
            N = False
            

def writes(f):
    talk("¿Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

"""
print("Bienvenido, diga su nombre..")
talk("Bienvenido, diga su nombre..")
nombreUsuario = listen()
print("Hola " + nombreUsuario + " en que te puedo ayudar?")
talk("hola " + nombreUsuario + " en que te puedo ayudar?")

print("funciones por ahora: reproduce - buscar - abrir - escribe - salir")
"""

# Botones
def español_voz():
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 145)
    talk("hola soy asistente de voz...")

def mexican_voz():
    engine.setProperty("voice", voices[2].id)
    engine.setProperty("rate", 145)
    talk("hola soy asistente de voz...")

button_español = Button(main_window, text= "Voz España", bg="white" , fg="black",
                    font=("Arial", 12, "bold"),command=español_voz)
button_español.place(x=650, y=80, width= 100, height= 30)

button_mx = Button(main_window, text= "Voz Mexico", bg="white" , fg="black",
                    font=("Arial", 12, "bold"), command=mexican_voz)
button_mx.place(x=650, y=115, width= 100, height= 30)

button_listen = Button(main_window, text= "Escuchar", bg="white" , fg="black", 
                       font=("Arial", 20, "bold"), command=run_asistente)
button_listen.place(x=620, y=200)

# camvas de comandos 
canvas_comandos = Canvas(bg="black", width=185, height=130)
canvas_comandos.place(x=600, y=260)
canvas_comandos.create_text(85,60, text=comandos, fill="white", font="arial 10")

main_window.mainloop()