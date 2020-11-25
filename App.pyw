import tkinter
from tkinter import Frame, Tk,Menu,Label,Button,Entry,PhotoImage
from tkinter.constants import END
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import sqlite3


root = Tk()
root.title('Registros')
root.geometry('370x360')
root.resizable(False,False)


frame1 = Frame(root)
frame1.pack()
menubar = Menu(root)
root.config(menu=menubar,width = 400, height = 300)

#----------BBDD------------------

bbdd = Menu(menubar,tearoff=0)
menubar.add_cascade(label = "BBDD",menu=bbdd)
bbdd.add_command(label = 'Conectar',command = lambda: crear_bd())
bbdd.add_separator()
bbdd.add_command(label = 'Salir',command= lambda: salir())

#----------Borrar----------------

borrar = Menu(menubar,tearoff = 0)
menubar.add_cascade(label = 'Borrar',menu = borrar)
borrar.add_command(label = 'Borrar campos',command= lambda: borrarcampos())

#----------CRUD------------------

crud = Menu(menubar,tearoff=0)
menubar.add_cascade(label = 'CRUD',menu = crud)
crud.add_command(label = 'Crear',command = lambda: insertar_datos())
crud.add_command(label = 'Leer',command = lambda: leer_datos())
crud.add_command(label = 'Actualizar',command = lambda: actualizar_datos())
crud.add_command(label = 'Eliminar' ,command = lambda : eliminar_datos())

#----------Ayuda------------------

ayuda = Menu(menubar,tearoff=0)
menubar.add_cascade(label = 'Ayuda',menu = ayuda)
ayuda.add_command(label = 'Licencia',command= lambda: licencia())
ayuda.add_command(label = 'Acerca de', command= lambda: acercaDe())

#----------Etiquetas---------------

idLabel = Label(frame1,text = 'ID: ')
idLabel.grid(column=0,row=0,sticky='w',padx=10,pady=10)

nombreLabel = Label(frame1,text='Nombre: ')
nombreLabel.grid(column=0,row=1,sticky='w',padx=10,pady=10)

ApellidoLabel = Label(frame1,text='Apellido: ')
ApellidoLabel.grid(column=0,row=2,sticky='w',padx=10,pady=10)

passLabel = Label(frame1,text='Contraseña: ')
passLabel.grid(column=0,row=3,sticky='w',padx=10,pady=10)

direccionLabel = Label(frame1,text= 'Direccion: ')
direccionLabel.grid(column=0,row=4,sticky='w',padx=10,pady=10)

comentariosLabel = Label(frame1,text= 'Comentarios: ')
comentariosLabel.grid(column=0,row=5,sticky='w',padx=10,pady=10)

#---------Botones---------------

crearBoton = Button(frame1, text= 'Crear',command= lambda: insertar_datos())
crearBoton.grid(row= 6, column=0)

leerBoton = Button(frame1, text= 'Leer', command= lambda: leer_datos())
leerBoton.grid(row= 6, column=1)

actualizarBoton = Button(frame1, text='Actualizar',command= lambda: actualizar_datos())
actualizarBoton.grid(row=6,column=2,padx=10,pady=10)

eliminarBoton = Button(frame1,text= 'Eliminar',command=lambda: eliminar_datos())
eliminarBoton.grid(row=6,column=3)

#---------Entrys----------------

idEntry = Entry(frame1)
idEntry.grid(row=0, column=1)

nombreEntry = Entry(frame1)
nombreEntry.grid(row=1, column=1)

apellidoEntry = Entry(frame1)
apellidoEntry.grid(row=2,column=1)

passEntry = Entry(frame1)
passEntry.grid(row=3,column=1)
passEntry.config(show='#')

direccionEntry = Entry(frame1)
direccionEntry.grid(row=4,column=1)

comentariosText = ScrolledText(frame1,width = 13, height = 5)
comentariosText.grid(row=5,column=1)

#---------Metodos-------------------

def salir():
    value = messagebox.askquestion('Salir?','Esta seguro de que desea salir?')
    if value == 'yes':
        root.destroy()

def acercaDe():
    messagebox.showinfo('Acerca de','Registros. Version 0.1')

def licencia():
    messagebox.showinfo('Agregar algo aqui mas tarde','RLM')

def borrarcampos():
    idEntry.delete(0,END)
    nombreEntry.delete(0,END)
    apellidoEntry.delete(0,END)
    passEntry.delete(0,END)
    direccionEntry.delete(0,END)
    comentariosText.delete(1.0,END)

#-------Base de datos--------------

def crear_bd():
    
        conexion = sqlite3.connect('Registro')
        cursor = conexion.cursor()
        try:
            cursor.execute('Create table persona(ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE VARCHAR(25), APELLIDO VARCHAR(50),PASS VARCHAR(50),DIRECCION VARCHAR(100))')
        except:
            messagebox.showerror('Error BD','La base de datos ya existe')

def insertar_datos():
        conexion = sqlite3.connect('Registro')
        cursor = conexion.cursor()
        registro = (nombreEntry.get(),apellidoEntry.get(),passEntry.get(),direccionEntry.get())
        cursor.executemany('INSERT INTO persona VALUES(NULL,?,?,?,?)',[registro])
        conexion.commit()

def leer_datos():
    conexion = sqlite3.connect('Registro')
    cursor = conexion.cursor()
    try:
        cursor.execute('SELECT * FROM persona WHERE ID = {}'.format(idEntry.get()))
        registro = cursor.fetchall()

        nombreEntry.delete(0,END)
        apellidoEntry.delete(0, END)
        passEntry.delete(0, END)
        direccionEntry.delete(0, END)
        for persona in registro:
            nombreEntry.insert(0,persona[1])
            apellidoEntry.insert(0,persona[2])
            passEntry.insert(0,persona[3])
            direccionEntry.insert(0,persona[4])
    except:
        messagebox.showerror('Oh no','Hubo un error inesperado')

def actualizar_datos():
    conexion = sqlite3.connect('Registro')
    cursor = conexion.cursor()

    try:
        value = messagebox.askquestion('Actualizar registro','Esta seguro de actualizar el registro')
        if value == 'yes':
            registro = (nombreEntry.get(),apellidoEntry.get(),passEntry.get(),direccionEntry.get(),int(idEntry.get()))
            cursor.execute('UPDATE persona set NOMBRE =?, APELLIDO = ?, PASS = ?,DIRECCION = ? WHERE ID = ?',registro)
            conexion.commit()
    except:
        messagebox.showerror('Oh no','Hubo un error inesperado')

    
def eliminar_datos():
    conexion = sqlite3.connect('Registro')
    cursor = conexion.cursor()

    try:
        value = messagebox.askquestion('Eliminar registro','Esta seguro de eliminar el registro?')
        if value == 'yes':   
            registro = (int(idEntry.get()))
            cursor.execute('DELETE FROM persona WHERE ID = {}'.format(idEntry.get()))
            conexion.commit()
    except:
        messagebox.showerror('Error','Ocurrio un error inesperado')
    
root.mainloop()
