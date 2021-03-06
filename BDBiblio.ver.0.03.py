

# -*- coding: utf-8 -*-
"""

@author: LJAG
"""

import sqlite3
from sqlite3 import Error
import tkinter
#import time
from tkinter import messagebox
from tkinter import OptionMenu
from tkinter import ttk
from tkinter import *
import os

## DB --------------------------------------------------------

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        #print("created", create_table_sql)
        
    except Error as e:
        print(e)


def insert_usuario(conn, nom, appat, apmat, edadI, gen, esc, ocp, disc, tpus, clav, numtau):
     
    try:
        cur = conn.cursor()
        
        sqlinsert = ''' INSERT INTO UsuariosBD(Nombre, Apellido_Paterno, 
                    Apellido_Materno, 
                    Edad, Genero, 
                    Escolaridad, 
                    Ocupacion, 
                    Discapacidad, 
                    Tipo_Usuario, 
                    Clave_Acceso,
                    Num_Tarjeta)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        
        
        cur = conn.cursor()
        
        
        
        val = (nom, appat, apmat, edadI, gen, esc, ocp, disc, tpus.get(), clav, numtau)
        cur.execute(sqlinsert, val)
        
        #cur.execute(sqlinsert,(nom, appat, apmat, edadI, gen, esc, ocp, disc, tpus, clav, numtau))
        conn.commit()
        
        cur.close()
    
    
    except Error as e:
        print(e)
    
    

def insert_libro(conn, aut, titu, clavL, cant, col, cantP, numE, volL, numAD, numTL, ISBN, clf):
    
    try:
        cur = conn.cursor()
        
        sqlinsertL = ''' INSERT INTO libros_table(Autor, Titulo, 
                    Clave, 
                    Cantidad, Coleccion, 
                    Cantidad_prestados, 
                    Num_ejemplar, 
                    Volumen, 
                    Num_adquisicion, 
                    Num_tarjeta_libro,
                    ISBN,
                    Clasificacion)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
                    
                    
        cur = conn.cursor()
        cur.execute(sqlinsertL, (aut, titu, clavL, cant, col, cantP, numE, volL, numAD, numTL, ISBN, clf))
        conn.commit()
        
        
        

    except Error as e:
        print(e)


def admin_check(conn):
    
    try:
        cur = conn.cursor()
        
        cur.execute("SELECT Nombre FROM UsuariosBD WHERE Nombre=?", ("adminBD",))
        adcheck = cur.fetchall()
                
               
        
        if len(adcheck) == 0:
            
            print("got")
            sql = '''INSERT INTO UsuariosBD(Nombre, Clave_Acceso, Tipo_Usuario)
            VALUES(?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql,('adminBD','1234','Administrador',))
            conn.commit()
            cur.close()
            
        else:
            print("El administrador ya esta registrado")
        
    except Error as e:
        print(e)



def login_data(user_login, code_login, conn):
    
        
    try:
        
        
        cur = conn.cursor()
        
        print(user_login)
        
        cur.execute("SELECT Nombre, Clave_Acceso, Tipo_Usuario FROM UsuariosBD WHERE Nombre=?", (user_login,))
        
        log_data = cur.fetchall()
        
        print(log_data)
        
        if len(log_data) == 0:
            print("El usuario no esta registrado")
            user_not_found()
            
            #Insert a way to exit login
        
        else:
        
            print(log_data)
            print(len(log_data))
            print(type(log_data))
            print(log_data[0][0])
        
            
            
            if (log_data[0][0] == user_login) and (log_data[0][1] == code_login) and (log_data[0][2]=="Administrador"):
            
                print("Acceso permitido")
                login_sucess()
            
            else:
                print("El usuario o la contraseña son incorrectos")
                password_not_recognised()
            
            
        
    except Error as e:
        print(e)

def mostrarUsuario(root, sqlS,editar):
    try:
        
        tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        #tree = ttk.Treeview(sf, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        mw = 80
        
        tree.column("#1", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#1", text="ID")
        
        tree.column("#2", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#2", text="Nombre")
        
        tree.column("#3", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#3", text="Apellido Paterno")
        
        tree.column("#4", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#4", text="Apellido Materno")
        
        tree.column("#5", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#5", text="Edad")
        
        tree.column("#6", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#6", text="Género")
        
        tree.column("#7", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#7", text="Escolaridad")
        
        tree.column("#8", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#8", text="Ocupación")
        
        tree.column("#9", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#9", text="Discapacidad")
        
        tree.column("#10", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#10", text="Tipo Usuario")
        
        tree.column("#11", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#11", text="# Tarjeta")
        
        #tree.grid()
        
        tree.pack(fill=BOTH, expand=1)
        
        
        cur = conn.cursor()
        
        
        
        #cur.execute("SELECT id_U, Nombre, Apellido_Paterno, Apellido_Materno, Edad, Genero, Escolaridad, Ocupacion, Discapacidad, Tipo_Usuario, Num_Tarjeta FROM UsuariosBD") # seleccionan todas las columnas menos la clave
        cur.execute(sqlS)
        filas = cur.fetchall()
        
        
        

        for i in filas:
            #print(i)
                            
            tree.insert("", tkinter.END, values=i)
            
        
        cur.close()
        
        salir = tkinter.Button(root, text = "Cerrar", command= root.destroy).pack(side=RIGHT)
        
        
        
    except Error as e:
        print(e)

    if editar:
        eliminar= tkinter.Button(root,text='Eliminar',command= lambda: on_delete_selected_button_clicked(tree,"UsuariosBD",root)).pack(side=LEFT)
        edit= tkinter.Button(root,text='Editar',command=lambda:on_modify_selected_button_clicked(tree,"UsuariosBD",root)).pack(side=LEFT) 

def mostrarPrestamo(root, sqlP,editar):
    try:
        
        tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
        
        #tree = ttk.Treeview(sf, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        tree.column("#1", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#1", text="ID")
        
        tree.column("#2", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#2", text="Fecha Inicio")
        
        tree.column("#3", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#3", text="Fecha Termino")
        
        tree.column("#4", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#4", text="Libros")
        
        tree.column("#5", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#5", text="Estado Prestamo")
        
        
        
        tree.pack(fill=BOTH, expand=1)
        
        
        cur = conn.cursor()
        
        
        
        cur.execute(sqlP)
        filas = cur.fetchall()
        
        
        

        for i in filas:
            print(i)
                            
            tree.insert("", tkinter.END, values=i)
            
        
        cur.close()
        
        
        
        
        
    except Error as e:
        print(e)
    
    
    
    salir = tkinter.Button(root, text = "Cerrar", command= root.destroy).pack(side=RIGHT)
    if editar:
        eliminar= tkinter.Button(root,text='Eliminar', command= lambda: on_delete_selected_button_clicked(tree,"prestamos_table",root)).pack(side=LEFT)
        edit= tkinter.Button(root,text='Editar',command=lambda:on_modify_selected_button_clicked(tree,"prestamos_table",root)).pack(side=LEFT)

def mostrarLibro(root, sqlL, editar):
    try:
        
        tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12"), show='headings')
        
        #tree = ttk.Treeview(sf, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        mw = 80
        
        tree.column("#1", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#1", text="Autor")
        
        tree.column("#2", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#2", text="Título")
        
        tree.column("#3", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#3", text="Clave")
        
        tree.column("#4", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#4", text="Cantidad")
        
        tree.column("#5", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#5", text="Colección")
        
        tree.column("#6", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#6", text="Cantidad prestados")
        
        tree.column("#7", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#7", text="# Ejemplar")
        
        tree.column("#8", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#8", text="Volumen")
        
        tree.column("#9", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#9", text="# Adquisición")
        
        tree.column("#10", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#10", text="# Tarjeta")
        
        tree.column("#11", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#11", text="ISBN")
        
        tree.column("#12", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#12", text="Clasificación")
        
        #tree.grid()
        
        tree.pack(fill=BOTH, expand=1)
        
        
        cur = conn.cursor()
        
        
        
        cur.execute(sqlL)
        filas = cur.fetchall()
        
        
        

        for i in filas:
            print(i)
                            
            tree.insert("", tkinter.END, values=i)
            
        
        cur.close()
        
        
        
        
        
    except Error as e:
        print(e)
    
    
    salir = tkinter.Button(root, text = "Cerrar", command= root.destroy).pack(side=RIGHT)
    if editar:
        eliminar= tkinter.Button(root,text='Eliminar', command= lambda: on_delete_selected_button_clicked(tree,"libros_table",root)).pack(side=LEFT)
        edit= tkinter.Button(root,text='Editar',command=lambda:on_modify_selected_button_clicked(tree,"libros_table",root)).pack(side=LEFT)

def main():
    
    database = r"C:\sqlite\db\pruebabd.db" # CONNECTION IS CREATED, ADRESS FOR LOCAL FILE
    
    
    #Tabla de usuarios
    users_table = """ CREATE TABLE IF NOT EXISTS UsuariosBD (
                                        id_U integer PRIMARY KEY,
                                        Nombre text NOT NULL,
                                        Apellido_Paterno text,
                                        Apellido_Materno text,
                                        Edad integer,
                                        Genero text,
                                        Escolaridad text,
                                        Ocupacion text,
                                        Discapacidad text,
                                        Tipo_Usuario text,
                                        Clave_Acceso text,
                                        Num_Tarjeta text
                                    ); """

    
    #Tabla conexion usuarios prestamos
    
    U_P_table = """ CREATE TABLE IF NOT EXISTS U_P_table (
                                        id_U integer  integer,
                                        id_P integer integer
                                    ); """
  
    #Tabla conexion prestamos libros
    
    P_L_table = """ CREATE TABLE IF NOT EXISTS P_L_table (
                                        id_P integer integer,
                                        id_L integer integer
                                    ); """
    
    #Tabla de Prestamos

    prestamos_table = """ CREATE TABLE IF NOT EXISTS prestamos_table (
                                        id_P integer PRIMARY KEY,
                                        Fecha_Inicial text NOT NULL,
                                        Fecha_Final text NOT NULL,
                                        Libros integer,
                                        Estado text
                                    ); """
    
    
    #Tabla de libros

    libros_table = """ CREATE TABLE IF NOT EXISTS libros_table (
                                        id_L integer PRIMARY KEY,
                                        Autor text NOT NULL,
                                        Titulo text NOT NULL,
                                        Clave text,
                                        Cantidad integer,
                                        Coleccion text,
                                        Cantidad_prestados integer,
                                        Num_ejemplar text,
                                        Volumen text,
                                        Num_adquisicion text,
                                        Num_tarjeta_libro text,
                                        ISBN text,
                                        Clasificacion text 
                                    ); """
    
    
    

    # create a database connection
    global conn
    conn = create_connection(database)
    
    
    

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, users_table)
        
        create_table(conn, U_P_table)
        
        create_table(conn, P_L_table)
        
        create_table(conn, prestamos_table)
        
        create_table(conn, libros_table)
        
        
        
        admin_check(conn)
        
        

    else:
        print("Error! No se pudo conectar a la base de datos.")





### GUI ------------------------------------------------------



# Designing window for registration

def register():
    
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()


# Designing window for login 

def login():
    
    
    global login_screen
    login_screen = Toplevel(main_screen)
    main_screen.withdraw()
    login_screen.title("Login")
    login_screen.geometry("600x650")
    label1 = Label( login_screen, image = bg) 
    label1.place(x = 0, y = 0) 
    frame1 = Frame(login_screen) 
    


    
    Label(login_screen, text="Ingrese su información para acceder",font=("Arial",20),bg="white").place(x = 75,y=170)

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Usuario",bg="white").place(x = 100,y=250)
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.place(x = 100,y=270)
    Label(login_screen, text="Contraseña",bg="white").place(x = 100,y=350)
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.place(x = 100,y=370)
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).place(x = 250,y=500)
    



# Implementing event on login button 

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    
    login_data(username1, password1, conn)
    
    
    """

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()
        
    """




# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("600x650")
    label1 = Label(login_success_screen, image = bg) 
    label1.place(x = 0, y = 0) 
    frame1 = Frame(login_success_screen) 
    Label(login_success_screen, text="Login Success",font=("Calibri", 16),bg = "white").place(x=220,y=200)
    Button(login_success_screen, text="OK", command=delete_login_success).place(x=280,y=300)

# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Deleting popups

def delete_login_success():
    login_success_screen.destroy()
    login_screen.destroy()
    menu()
    main_screen.withdraw()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    
    main()
    
    global main_screen
    global bg
    main_screen = Tk()  # create a GUI window
    main_screen.geometry("600x650") # set the configuration of GUI window 
    main_screen.title("Account Login")  # set the title of GUI window
     # create a Form label
    bg = PhotoImage(file = "fondo.png") 
    label1 = Label( main_screen, image = bg) 
    label1.place(x = 0, y = 0) 
    frame1 = Frame(main_screen) 
    Label(text="Base de Datos", width="30", height="2", font=("Calibri", 16),bg = "white").place(x=100,y=200)
    bgingresar = PhotoImage(file = "Ingresar.png")
    Button(text="Ingresar", height="40", width="90", command = login,bg="white",image = bgingresar,border = "0").place(x = 245, y = 300) # create Login Button
    #Button(text="Register", height="2", width="30", command=register).pack() # create a register button

    main_screen.mainloop() # start the GUI


##------------------------------------------------------------------------------
##-------------------------------GUI PART #2------------------------------------
##------------------------------------------------------------------------------




def menu():  
  ventana2= tkinter.Toplevel()
  ventana2.geometry( "600x650")
  global main_screen
  main_screen.withdraw()
  label1 = Label(ventana2, image = bg) 
  label1.place(x = 0, y = 0) 
  frame1 = Frame(ventana2) 
  
  def salir():
      ventana2.destroy()
      main_screen.destroy()
      sys.exit()

  texto = tkinter.Label(ventana2, text = "Menú",font=("Calibri", 25),bg = "white").place( x = 250, y = 180)
  boton_consulta = tkinter.Button(ventana2, text = "Consulta", command= lambda: consulta(ventana2),bg = "white").place(x = 70, y = 250 )
  boton_registro_usuario = tkinter.Button(ventana2, text = "Registro de usuarios", command=lambda:registro(ventana2),bg = "white").place(x = 70, y =300 )
  boton_prestamo = tkinter.Button(ventana2, text = "Préstamo", command=lambda:prestamo(ventana2),bg = "white").place(x = 70, y = 350 )
  boton_registro_libro = tkinter.Button(ventana2, text = "Registro de libros", command=lambda: libros(ventana2),bg = "white").place(x = 70, y = 400 )
  boton_edicion_datos = tkinter.Button(ventana2, text = "Edicion de datos",command = lambda:edicionDatos(ventana2),bg = "white").place(x = 70, y = 450 )
  boton_busqueda = tkinter.Button(ventana2, text = "Busqueda", command=lambda:busqueda(ventana2),bg = "white").place(x = 70, y = 500)

  #boton_salir2 = tkinter.Button(ventana2, text = "Salir", command= ventana2.destroy).place(x = 250, y = 250 )
  
  boton_salir2 = tkinter.Button(ventana2, text = "Salir", command= salir,bg = "white").place(x = 290, y = 550 )


def consulta(ven_para_cerrar):
    
  ventana3=tkinter.Tk()
  ventana3.geometry( "600x500+100+50")
  ven_para_cerrar.withdraw()

  def usuarioBD():
      
    
    tablaUsuario=tkinter.Tk()
    tablaUsuario.geometry( "1000x450")
    #usuarioDisplay = tkinter.Label(tablaUsuario, text = """Tabla Usuarios """).grid(row=0, column=0, sticky="nsew")
    
    #scrollbar
    
    #frame se pone todo tablaUsuario dentro
    #mf = Frame(tablaUsuario) #, width=900, height = 400
    #mf.pack(fill=BOTH, expand=1)
    
    #canv = Canvas(mf)
    #canv.pack(side=LEFT, fill=BOTH, expand=1)
    
    #scb = ttk.Scrollbar(mf, orient=VERTICAL, command=canv.yview)
    #scb.pack(side=RIGHT, fill=Y)
    
    #canv.configure(yscrollcommand=scb.set)
    #canv.bind('<Configure>', lambda e: canv.configure(scrollregion=canv.bbox("all")))
    
    #sf = Frame(canv)
    
    #canv.create_window((0,0), window=sf, anchor="nw")
    
    try:
        
        tree = ttk.Treeview(tablaUsuario, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        #tree = ttk.Treeview(sf, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        mw = 80
        
        tree.column("#1", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#1", text="ID")
        
        tree.column("#2", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#2", text="Nombre")
        
        tree.column("#3", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#3", text="Apellido Paterno")
        
        tree.column("#4", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#4", text="Apellido Materno")
        
        tree.column("#5", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#5", text="Edad")
        
        tree.column("#6", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#6", text="Género")
        
        tree.column("#7", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#7", text="Escolaridad")
        
        tree.column("#8", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#8", text="Ocupación")
        
        tree.column("#9", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#9", text="Discapacidad")
        
        tree.column("#10", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#10", text="Tipo Usuario")
        
        tree.column("#11", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#11", text="# Tarjeta")
        
        #tree.grid()
        
        tree.pack(fill=BOTH, expand=1)
        
        
        cur = conn.cursor()
        
        
        
        cur.execute("SELECT id_U, Nombre, Apellido_Paterno, Apellido_Materno, Edad, Genero, Escolaridad, Ocupacion, Discapacidad, Tipo_Usuario, Num_Tarjeta FROM UsuariosBD") # seleccionan todas las columnas menos la clave
        filas = cur.fetchall()
        
        
        

        for i in filas:
            print(i)
                            
            tree.insert("", tkinter.END, values=i)
            
        
        cur.close()
        
        
        
        
        
    except Error as e:
        print(e)
      
      
    #salir = tkinter.Button(tablaUsuario, text = "Cerrar", command= tablaUsuario.destroy).grid(row=2, column=1, sticky="nsew")
    
    #salir = tkinter.Button(sf, text = "Cerrar", command= tablaUsuario.destroy).pack(side=RIGHT)
    salir = tkinter.Button(tablaUsuario, text = "Cerrar", command= tablaUsuario.destroy).pack(side=RIGHT)
    
    
    return

  def prestamoBD():
    tablaPrestamo=tkinter.Tk()
    tablaPrestamo.geometry( "600x600")
    #prestamoDisplay = tkinter.Label(tablaPrestamo, text = """Aqui se muestrala tabla """).grid(row=0, column=0, sticky="nsew")
    
    try:
        
        tree = ttk.Treeview(tablaPrestamo, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
        
        #tree = ttk.Treeview(sf, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        tree.column("#1", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#1", text="ID")
        
        tree.column("#2", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#2", text="Fecha Inicio")
        
        tree.column("#3", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#3", text="Fecha Termino")
        
        tree.column("#4", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#4", text="Libros")
        
        tree.column("#5", anchor=tkinter.CENTER, minwidth=80, width=80)
        tree.heading("#5", text="Estado Prestamo")
        
        
        
        tree.pack(fill=BOTH, expand=1)
        
        
        cur = conn.cursor()
        
        
        
        cur.execute("SELECT id_P, Fecha_Inicial, Fecha_Final, Libros, Estado FROM prestamos_table") # seleccionan todas las columnas menos la clave
        filas = cur.fetchall()
        
        
        

        for i in filas:
            print(i)
                            
            tree.insert("", tkinter.END, values=i)
            
        
        cur.close()
        
        
        
        
        
    except Error as e:
        print(e)
    
    
    
    salir = tkinter.Button(tablaPrestamo, text = "Cerrar", command= tablaPrestamo.destroy).pack(side=RIGHT)
    
    
    
    return

  def libroBD():
    tablaLibro=tkinter.Tk()
    tablaLibro.geometry( "1000x400")
    #libroDisplay = tkinter.Label(tablaLibro, text = """Aqui se muestra
    #la tabla """).grid(row=0, column=0, sticky="nsew")
    
    try:
        
        tree = ttk.Treeview(tablaLibro, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12"), show='headings')
        
        #tree = ttk.Treeview(sf, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"), show='headings')
        
        mw = 80
        
        tree.column("#1", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#1", text="Autor")
        
        tree.column("#2", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#2", text="Título")
        
        tree.column("#3", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#3", text="Clave")
        
        tree.column("#4", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#4", text="Cantidad")
        
        tree.column("#5", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#5", text="Colección")
        
        tree.column("#6", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#6", text="Cantidad prestados")
        
        tree.column("#7", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#7", text="# Ejemplar")
        
        tree.column("#8", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#8", text="Volumen")
        
        tree.column("#9", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#9", text="# Adquisición")
        
        tree.column("#10", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#10", text="# Tarjeta")
        
        tree.column("#11", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#11", text="ISBN")
        
        tree.column("#12", anchor=tkinter.CENTER, minwidth=mw, width=80)
        tree.heading("#12", text="Clasificación")
        
        #tree.grid()
        
        tree.pack(fill=BOTH, expand=1)
        
        
        cur = conn.cursor()
        
        
        
        cur.execute("SELECT Autor, Titulo, Clave, Cantidad, Coleccion, Cantidad_prestados, Num_ejemplar, Volumen, Num_adquisicion, Num_tarjeta_libro, ISBN, Clasificacion FROM libros_table") # seleccionan todas las columnas menos la clave
        filas = cur.fetchall()
        
        
        

        for i in filas:
            print(i)
                            
            tree.insert("", tkinter.END, values=i)
            
        
        cur.close()
        
        
        
        
        
    except Error as e:
        print(e)
    
    
    salir = tkinter.Button(tablaLibro, text = "Cerrar", command= tablaLibro.destroy).pack(side=RIGHT)
    
    
    return
  def regresar():
        """
        Metodo para regresar a la ventana anterior
        """
        ven_para_cerrar.deiconify()
        ventana3.destroy()

  texto2 = tkinter.Label(ventana3, text = "Consulta", font = ("Arial", 30)).place( x = 275, y = 400)
  boton_usuario = tkinter.Button(ventana3, text = "Usuario", command = usuarioBD).place(x = 50, y = 50 )

  #Se despliega tabla de datos de usuarioBD
  #---------------------------------------------

  boton_prestamo2 = tkinter.Button(ventana3, text = "Préstamo", command = prestamoBD).place(x = 50, y =90 )

  #Se despliega tabla de datos de prestamoBD
  #---------------------------------------------

  boton_libro = tkinter.Button(ventana3, text = "Libro", command = libroBD).place(x = 50, y = 130 )

  #Se despliega tabla de datos de libroBD
  #---------------------------------------------

  boton_menu = tkinter.Button(ventana3, text = "Regresar", command=regresar).place(x = 150, y = 250)
 
def registro(ven_para_cerrar):
    ven_para_cerrar.withdraw()
    def registrarBD():
        #---------------------------------
        #"""añadir datos a Base de datos"""
        
        #conn, nom, appat, apmat, edadI, gen, esc, ocp, disc, tpus, ca, numtau
        
        nom = textBox_nombre.get()
        appat = textBox_apellidop.get()
        apmat = textBox_apellidom.get()
        edadI =textBox_edad.get()
        gen = textBox_genero.get()
        esc = textBox_escolaridad.get()
        ocp = textBox_ocupacion.get()
        disc = textBox_discapacidad.get()
        numtau = textBox_numero_tarjeta_usuario.get()
        
        clav = textBox_clave.get()
        
        
        
        insert_usuario(conn, nom, appat, apmat, edadI, gen, esc, ocp, disc, tpus, clav, numtau)
        
        textBox_nombre.delete(0, END)
        textBox_apellidop.delete(0, END)
        textBox_apellidom.delete(0, END)
        textBox_edad.delete(0, END)
        textBox_genero.delete(0, END)
        textBox_escolaridad.delete(0, END)
        textBox_ocupacion.delete(0, END)
        textBox_discapacidad.delete(0, END)
        textBox_clave.delete(0, END)
        textBox_numero_tarjeta_usuario.delete(0, END)
        
        #.delete(0, END)
        
        #username_login_entry = Entry(login_screen, textvariable=username_verify)
        
        #-----------------------------------
                
        correcto = messagebox.showinfo(message="Se ha registrado con exito", title="Exito")
        #con.close()
        
        return
    def regresar():
        """
        Metodo para regresar a la ventana anterior
        """
        ven_para_cerrar.deiconify()
        ventana4.destroy()


    ventana4=tkinter.Tk()
    ventana4.geometry( "600x600+100+50")
    texto3 = tkinter.Label(ventana4, text = "Registro de Usuarios", font = ("Arial", 30)).place( x = 160, y = 500)
    boton_menu2 = tkinter.Button(ventana4, text = "Regresar", command=regresar).place(x = 320, y = 450)
    
    #boton_registrar = tkinter.Button(ventana4, text = "Registrar", command= registrarBD).place(x = 250, y = 400)

    #funcion para agregar datos de persona registrada a base de datos
    
    
    
    #-----------------------------------------------
    
    # definir variables para la los cuadros de texto
    nom = StringVar()
    appat = StringVar()
    apmat = StringVar()
    edadI = StringVar()
    gen = StringVar()
    esc = StringVar()
    ocp = StringVar()
    disc = StringVar()
    tpus = StringVar()
    numtau = StringVar()
    clav = StringVar()
    
    

    # Texto de los cuadros de seleccion

    nombre = tkinter.Label(ventana4,text="Nombre").place ( x = 100, y = 10)
    apellidop = tkinter.Label(ventana4,text="Apellido Paterno").place ( x = 100, y = 35)
    apellidom = tkinter.Label(ventana4,text="Apellido Materno").place ( x = 100, y = 60)
    edad = tkinter.Label(ventana4,text="Edad").place ( x = 100, y = 85)
    genero = tkinter.Label(ventana4,text="Género").place ( x = 100, y = 110)
    escolaridad = tkinter.Label(ventana4,text="Escolaridad").place ( x = 100, y = 135)
    ocupacion = tkinter.Label(ventana4,text="Ocupación").place ( x = 100, y = 160)
    discapacidad = tkinter.Label(ventana4,text="Discapacidad").place( x =100, y = 185)
    numtarjetaus = tkinter.Label(ventana4,text="Número tarjeta usuario").place( x =100, y = 210)
    tipousuario = tkinter.Label(ventana4,text="Tipo de Usuario").place( x =100, y = 235)
    
    
    #Campos de entrada para el registro de usuarios
    
    textBox_nombre = tkinter.Entry(ventana4, textvariable = nom)
    #textBox_nombre.pack(side=tkinter.TOP)
    textBox_nombre.place( x =250, y = 10)
    
    textBox_apellidop = tkinter.Entry(ventana4, textvariable = appat)
    #textBox_apellidop.pack(side=tkinter.TOP)
    textBox_apellidop.place( x =250, y = 35)
    
    textBox_apellidom = tkinter.Entry(ventana4, textvariable = apmat)
    #textBox_apellidom.pack(side=tkinter.TOP)
    textBox_apellidom.place( x =250, y = 60)
    
    textBox_edad = tkinter.Entry(ventana4, textvariable = edadI)
    #textBox_edad.pack(side=tkinter.TOP)
    textBox_edad.place( x =250, y = 85)
    
    textBox_genero = tkinter.Entry(ventana4, textvariable = gen)
    #textBox_genero.pack(side=tkinter.TOP)
    textBox_genero.place( x =250, y = 110)
    
    textBox_escolaridad = tkinter.Entry(ventana4, textvariable = esc)
    #textBox_escolaridad.pack(side=tkinter.TOP)
    textBox_escolaridad.place( x =250, y = 135)
    
    textBox_ocupacion = tkinter.Entry(ventana4, textvariable = ocp)
    #textBox_ocupacion.pack(side=tkinter.TOP)
    textBox_ocupacion.place( x =250, y = 160)
    
    textBox_discapacidad = tkinter.Entry(ventana4, textvariable = disc)
    #textBox_discapacidad.pack(side=tkinter.TOP)
    textBox_discapacidad.place( x =250, y = 185)
    
    #NUMtau
    
    textBox_numero_tarjeta_usuario = tkinter.Entry(ventana4, textvariable = numtau)
    #textBox_discapacidad.pack(side=tkinter.TOP)
    textBox_numero_tarjeta_usuario.place( x =250, y = 210)
    
    
    
    textBox_clave = tkinter.Entry(ventana4, textvariable = clav)
    #textBox_discapacidad.pack(side=tkinter.TOP)
    textBox_clave.place( x =250, y = 285)
    
    claveadmin = tkinter.Label(ventana4,text="Clave Administrador")
    claveadmin.place( x =100, y = 285)
    
    
    #oculta las ventantas antes de la seleccion
    
    textBox_clave.place_forget()
    claveadmin.place_forget()
    
    
    #Dropdown menu   
    
    
    def adclave(event):
    
        if varDesTipUs.get() == "Administrador":
            claveadmin.place( x =100, y = 285)
            textBox_clave.place( x =250, y = 285)
            #tpus = "Administrador"
            tpus.set("Administrador")
            clav = textBox_clave.get()
        
        elif varDesTipUs.get() == "Usuario":
            textBox_clave.place_forget()
            claveadmin.place_forget()
            #tpus = "Usuario"
            tpus.set("Usuario")
            
    
    
    varDesTipUs = StringVar(ventana4)
    opTipus = ['Administrador','Usuario'] #opciones de la ventana deslizante opciones tipo usuario
    varDesTipUs.set("Selecionar")
    ventanaDeslizanteTipUs = OptionMenu(ventana4, varDesTipUs, *opTipus, command=adclave)
    ventanaDeslizanteTipUs.config(width=15)
    ventanaDeslizanteTipUs.place(x = 250, y = 235)
    
    selecTipUs = varDesTipUs.get() #obtiene la seleccion del menu deslizante
    
    
    boton_registrar = tkinter.Button(ventana4, text = "Registrar", command= registrarBD).place(x = 250, y = 400)
    

    
    if textBox_nombre or textBox_apellidop or textBox_apellidom or textBox_edad or textBox_genero or textBox_escolaridad or textBox_ocupacion == "":
      pass

def libros(ven_para_cerrar):
    ven_para_cerrar.withdraw()
    def registarLibro():
      #---------------------------------
      #---------Registro en DB   
      #------------------------------
      
      aut = textBox_autor.get()
      titu = textBox_titulo.get()
      clavL = textBox_clave.get()
      cant = textBox_cantidad.get()
      col = textBox_coleccion.get()
      cantP = textBox_cantidad_prestados.get()
      numE = textBox_numero_ejemplar.get()
      volL = textBox_volumen.get()
      numAD = textBox_numero_adq.get()
      numTL = textBox_numero_tarjeta_libro.get()
      ISBN  = textBox_ISBN.get()
      clf = textBox_clasif.get()
      
      insert_libro(conn, aut, titu, clavL, cant, col, cantP, numE, volL, numAD, numTL, ISBN, clf)
      
      textBox_autor.delete(0, END)
      textBox_titulo.delete(0, END)
      textBox_clave.delete(0, END)
      textBox_cantidad.delete(0, END)
      textBox_coleccion.delete(0, END)
      textBox_cantidad_prestados.delete(0, END)
      textBox_numero_ejemplar.delete(0, END)
      textBox_volumen.delete(0, END)
      textBox_numero_adq.delete(0, END)
      textBox_numero_tarjeta_libro.delete(0, END)
      textBox_ISBN.delete(0, END)
      textBox_clasif.delete(0, END)
      
      
      correcto = messagebox.showinfo(message="Se ha registrado con exito", title="Exito")
      return
    def regresar():
        """
        Metodo para regresar a la ventana anterior
        """
        ven_para_cerrar.deiconify()
        ventana5.destroy()

    ventana5 = tkinter.Tk()
    ventana5.geometry( "600x500+100+50")
    texto4 = tkinter.Label(ventana5, text = "Registro Libros", font = ("Arial", 30)).place( x = 230, y = 400)
    
    boton_menu3 = tkinter.Button(ventana5, text = "Regresar", command=regresar).place(x = 300, y = 350)
    
    boton_registrar2 = tkinter.Button(ventana5, text = "Registrar", command=registarLibro).place(x = 250, y = 310)
    
    autor = tkinter.Label(ventana5,text="Autor").place ( x = 95, y = 10)
    
    titulo = tkinter.Label(ventana5,text="Titulo").place ( x = 95, y = 35)
    
    clave = tkinter.Label(ventana5,text="Clave").place ( x = 95, y = 60)
    
    cantidad = tkinter.Label(ventana5,text="Cantidad").place ( x = 95, y = 85)
    
    coleccion = tkinter.Label(ventana5,text="Colección").place ( x = 95, y = 110)
    
    cantidad_prestados = tkinter.Label(ventana5,text="Cantidad prestados").place ( x = 95, y = 135)
    
    numero_ejemplar = tkinter.Label(ventana5,text="Volumen").place ( x = 95, y = 160)
    
    numero_ejemplar = tkinter.Label(ventana5,text="N° de adquisición").place ( x = 95, y = 185)
    
    numero_ejemplar = tkinter.Label(ventana5,text="N° de tarjeta del libro").place ( x = 95, y = 210)
    
    numero_ejemplar = tkinter.Label(ventana5,text="ISBN").place ( x = 95, y = 235)
    
    numero_ejemplar = tkinter.Label(ventana5,text="Clasificación").place ( x = 95, y = 260)
    
    
    
    #------------------------------------------
    #Definición de variables para los cuadros de texto
    
    aut = StringVar()
    titu = StringVar()
    clavL= StringVar()
    cant = StringVar()
    col = StringVar()
    cantP = StringVar()
    numE = StringVar()
    volL = StringVar()
    numAD = StringVar()
    numTL = StringVar()
    ISBN  = StringVar()
    clf = StringVar()
    
    
    textBox_autor = tkinter.Entry(ventana5)
    #textBox_autor.pack(side=tkinter.TOP)
    textBox_autor.place(x = 250, y = 10)
    
    textBox_titulo = tkinter.Entry(ventana5)
    #textBox_titulo.pack(side=tkinter.TOP)
    textBox_titulo.place(x = 250, y = 35)
    
    textBox_clave = tkinter.Entry(ventana5)
    #textBox_clave.pack(side=tkinter.TOP)
    textBox_clave.place(x = 250, y = 60)
    
    textBox_cantidad = tkinter.Entry(ventana5)
    #textBox_cantidad.pack(side=tkinter.TOP)
    textBox_cantidad.place(x = 250, y = 85)
    
    textBox_coleccion = tkinter.Entry(ventana5)
    #textBox_coleccion.pack(side=tkinter.TOP)
    textBox_coleccion.place(x = 250, y = 110)
    
    textBox_cantidad_prestados = tkinter.Entry(ventana5)
    #textBox_cantidad_prestados.pack(side=tkinter.TOP)
    textBox_cantidad_prestados.place(x = 250, y = 135)
    
    textBox_numero_ejemplar = tkinter.Entry(ventana5)
    #textBox_numero_ejemplar.pack(side=tkinter.TOP)
    textBox_numero_ejemplar.place(x = 250, y = 160)
    #----------------------------------------------------------------
    textBox_volumen = tkinter.Entry(ventana5)
    #textBox_numero_ejemplar.pack(side=tkinter.TOP)
    textBox_volumen.place(x = 250, y = 185)
    
    textBox_numero_adq = tkinter.Entry(ventana5)
    #textBox_numero_ejemplar.pack(side=tkinter.TOP)
    textBox_numero_adq.place(x = 250, y = 210)
    
    textBox_numero_tarjeta_libro = tkinter.Entry(ventana5)
    #textBox_numero_ejemplar.pack(side=tkinter.TOP)
    textBox_numero_tarjeta_libro.place(x = 250, y = 235)
    
    textBox_ISBN = tkinter.Entry(ventana5)
    #textBox_numero_ejemplar.pack(side=tkinter.TOP)
    textBox_ISBN.place(x = 250, y = 260)
    
    textBox_clasif = tkinter.Entry(ventana5)
    #textBox_numero_ejemplar.pack(side=tkinter.TOP)
    textBox_clasif.place(x = 250, y = 260)

def prestamo(ven_para_cerrar):
    ven_para_cerrar.withdraw()
    def registarPrestamo():
      #---------------------------------
      #---------Registro en DB   
      
      
      
      #------------------------------
      correcto = messagebox.showinfo(message="Se ha registrado con exito", title="Exito")
      return
    def regresar():
        """
        Metodo para regresar a la ventana anterior
        """
        ven_para_cerrar.deiconify()
        ventana6.destroy()

    ventana6=tkinter.Tk()
    ventana6.geometry( "600x500+100+50")
    texto5 = tkinter.Label(ventana6, text = "Préstamo", font = ("Arial", 30)).place( x = 250, y = 400)
    boton_menu4 = tkinter.Button(ventana6, text = "Regresar", command=regresar).place(x = 300, y = 180)
    boton_registrar3 = tkinter.Button(ventana6, text = "Registrar", command=registarPrestamo).place(x = 250, y = 140)    
    fechain=tkinter.Label(ventana6,text="Fecha Inicial").place ( x = 110, y = 5)
    fechafi=tkinter.Label(ventana6,text="Fecha Final").place ( x = 110, y = 25)
    libros=tkinter.Label(ventana6,text="Libros").place ( x = 110, y = 45)
    estado=tkinter.Label(ventana6,text="Estado").place ( x = 110, y = 65)
    textBox_fechain = tkinter.Entry(ventana6)
    textBox_fechain.pack(side=tkinter.TOP)
    textBox_fechafi = tkinter.Entry(ventana6)
    textBox_fechafi.pack(side=tkinter.TOP)
    textBox_libros = tkinter.Entry(ventana6)
    textBox_libros.pack(side=tkinter.TOP)
    textBox_estado = tkinter.Entry(ventana6)
    textBox_estado.pack(side=tkinter.TOP)

def on_delete_selected_button_clicked(tree,tabla,root):
    try:
        tree.item(tree.selection())['values'][0]
    except IndexError as e:
        messagebox.showinfo(message="Selecciona un objeto")
        return
    delete_items(tree,tabla,root)

def on_modify_selected_button_clicked(tree,tabla,root):
    try:
        tree.item(tree.selection())['values'][0]
    except IndexError as e:
        messagebox.showinfo(message="Selecciona un objeto")
        return
    modify_items(tree,tabla,root)

def modify_items(tree,tabla,root):
    #FALTA TERMINAR ESTE METODO
    """
    Funcion diseñada para el boton de edición de datos, habra 3 botones para selecionar dependiendo de como se quieran edicar los datos
    Entrada: La ventana que se desea cerrar depues de abrir la ventana
    Salida: Ninguna
    """
    root.withdraw()
    def regresar():
        """
        Metodo para regresar a la ventana anterior
        """
        ventana_edicion_datos.destroy()
        root.destroy()

    ventana_edicion_datos = tkinter.Tk()
    ventana_edicion_datos.geometry("600x650")
    texto = tkinter.Label(ventana_edicion_datos, text = "Edición de Datos", font = ("Arial", 30)).place( x = 150, y = 50)
    boton_sinnombre1 = tkinter.Button(ventana_edicion_datos, text = "Boton Sin Nombre 1",).place(x = 240, y = 125 )
    boton_sinnombre2 = tkinter.Button(ventana_edicion_datos, text = "Boton Sin Nombre 2",).place(x = 240, y = 175 )
    boton_sinnombre3 = tkinter.Button(ventana_edicion_datos, text = "Boton Sin Nombre 3",).place(x = 240, y = 225 )
    boton_regresar = tkinter.Button(ventana_edicion_datos, text = "Regresar",command = regresar).place(x = 450, y = 500 )
    label = Label(ventana_edicion_datos) 
    label.place(x = 0, y = 0) 
    #label.draw
    frame = Frame(ventana_edicion_datos)

def delete_items(tree,tabla,root):
    #print(tree)
    #print(tabla)
    name=tree.item(tree.selection())['values'][0]
    print(name)
    #cur = conn.cursor()
    if tabla=="libros_table":
        query = 'DELETE FROM ' +tabla+' WHERE id_L = ?'
    elif tabla=="UsuariosBD":
        query = 'DELETE FROM ' +tabla+' WHERE id_U = ?'
    elif tabla=="prestamos_table":
        query = 'DELETE FROM ' +tabla+' WHERE id_P = ?'
    print(query)
    #cur.execute(query,(name,))
    #conn.commit()
    messageDelete = messagebox.askyesno("Confirmación", "¿Quieres eliminar este registro permanentemente?")
    if messageDelete > 0:
        execute_db_query(query, (name,))
        messagebox.showinfo(message="Eliminado con éxito")
        root.destroy()

def execute_db_query(query, parameters=()):
    print(conn)
    print('You have successfully connected to the DatabaseT')
    cursor = conn.cursor()
    query_result = cursor.execute(query, parameters)
    conn.commit()
    return query_result


def edicionDatos(ven_para_cerrar):
    busqueda(ven_para_cerrar,True)


def busqueda(ven_para_cerrar,*editar):
    ven_para_cerrar.withdraw()
    def buscarBD():
      
      #Buscar en base de datos seleccion
      print(tipoBus.get())
      tipoTab.set(varModo.get())
      

      print("tipotab")
      print(tipoTab.get())
      bsq = textBox_buscar.get() #obtinen la busqueda

      
      #Aqui se toma la seleccion del menu y se traduce a las variables de la base
      
      if tipoBus.get() == "BC":
          if tipoTab.get() == "Usuario":
              tabla = "UsuariosBD"
              statement = f"SELECT id_U, Nombre, Apellido_Paterno, Apellido_Materno, Edad, Genero, Escolaridad, Ocupacion, Discapacidad, Tipo_Usuario, Num_Tarjeta FROM UsuariosBD WHERE Nombre LIKE '%{bsq}%' OR Apellido_Paterno LIKE '%{bsq}%' OR Apellido_Materno LIKE '%{bsq}%' OR Edad LIKE '%{bsq}%' OR Genero LIKE '%{bsq}%' OR Escolaridad LIKE '%{bsq}%' OR Ocupacion LIKE '%{bsq}%' OR Discapacidad LIKE '%{bsq}%' OR Tipo_Usuario LIKE '%{bsq}%' OR Num_Tarjeta LIKE '%{bsq}%';"
          elif tipoTab.get() == "Prestamo":
              tabla = "prestamos_table"
              statement = f"SELECT * FROM {tabla} WHERE Fecha_Inicial LIKE '%{bsq}%' OR Fecha_Final LIKE '%{bsq}%' OR Estado LIKE '%{bsq}%';"
          elif tipoTab.get() == "Libro":
              tabla = "libros_table"
              statement = f"SELECT * FROM {tabla} WHERE Autor LIKE '%{bsq}%' OR Titulo LIKE '%{bsq}%' OR Clave LIKE '%{bsq}%' OR Coleccion LIKE '%{bsq}%' OR Num_ejemplar LIKE '%{bsq}%' OR Volumen LIKE '%{bsq}%' OR Num_adquisicion LIKE '%{bsq}%' OR Num_tarjeta_libro LIKE '%{bsq}%' OR ISBN LIKE '%{bsq}%' OR Clasificacion LIKE '%{bsq}%';"
      else:
          tabla = tipoBus.get()
          
          if tipoTab.get() == "Id":
              columna = "id_U"
          elif tipoTab.get() == "Nombre":
              columna = "Nombre"
          elif tipoTab.get() == "Apellido Paterno":
              columna = "Apellido_Paterno"
          elif tipoTab.get() == "Apellido Materno":
              columna = "Apellido_Materno"    
          elif tipoTab.get() == "Edad":
              columna = "Edad"
          elif tipoTab.get() == "Fecha Inicial":
              columna = "Fecha_Inicial"  
          elif tipoTab.get() == "Fecha Final":
              columna = "Fecha_Final"  
          elif tipoTab.get() == "Libros":
              columna = "Libros"   
          elif tipoTab.get() == "Estado":
              columna = "Estado"   
          elif tipoTab.get() == "Autor":
              columna = "Autor"
          elif tipoTab.get() == "Título":
              columna = "Titulo"
          elif tipoTab.get() == "Clave":
              columna = "Clave"    
          elif tipoTab.get() == "Colección":
              columna = "Coleccion"
          elif tipoTab.get() == "# ejemplar":
              columna = "Num_ejemplar"  
          elif tipoTab.get() == "Volumen":
              columna = "Volumen"
          elif tipoTab.get() == "# Adquisición":
              columna = "Num_adquisicion"  
          elif tipoTab.get() == "# Tarjeta":
              columna = "Num_tarjeta_libro"   
          elif tipoTab.get() == "ISBN":
              columna = "ISBN"  
          elif tipoTab.get() == "Clasificación":
              columna = "Clasificacion"  
            
          statement = f"SELECT * FROM {tabla} WHERE {columna} LIKE '%{bsq}%';"
          
            
      #statement = f"SELECT * FROM {tabla} WHERE {columna} LIKE '%{bsq}%';"
      
      
      tabla_busqueda = tkinter.Tk()
      tabla_busqueda.geometry("1000x500")
      
      
      #seleccion formato tabla a mostrar
      
      if tipoBus.get() == "BC":
          if tipoTab.get() == "Usuario":
              mostrarUsuario(tabla_busqueda, statement,editar)
          elif tipoTab.get() == "Prestamo":
              mostrarPrestamo(tabla_busqueda, statement,editar)
          elif tipoTab.get() == "Libro":
              mostrarLibro(tabla_busqueda, statement,editar)
              
      elif tipoBus.get() == "UsuariosBD":
          mostrarUsuario(tabla_busqueda, statement,editar)
          print("gotr")
      elif tipoBus.get() == "prestamos_table":
          mostrarPrestamo(tabla_busqueda, statement,editar)        
      elif tipoBus.get() == "libros_table":
          mostrarLibro(tabla_busqueda, statement,editar)
      
      
      #mostrarUsuario(tabla_busqueda, statement,editar) #HACER OTRA FUNCION PARA MOSTRAR TODAS LAS TABLAS
      
      return
  
    def regresar():
        """
        Metodo para regresar a la ventana anterior
        """
        ven_para_cerrar.deiconify()
        ventana7.destroy()

    ventana7=tkinter.Tk()
    ventana7.geometry( "600x650")

    if not editar:
        texto6 = tkinter.Label(ventana7, text = "Búsqueda", font = ("Arial", 30)).place( x = 270, y = 400)
    else:
        texto6 = tkinter.Label(ventana7, text = "Edición", font = ("Arial", 30)).place( x = 270, y = 400)
        
    boton_menu5 = tkinter.Button(ventana7, text = "Regresar", command=regresar).place(x = 330, y = 300)  
    
    
    bsq = StringVar()
    
    tipoBus = StringVar()
    
    tipoTab = StringVar()
    
    textBox_buscar = tkinter.Entry(ventana7, textvariable = bsq)
    
    textBox_buscar.place(x = 230 , y = 200)
    
    #boton_buscar = tkinter.Button(ventana7, text = "Buscar",command = buscarBD).place(x = 400, y = 200)
    
    
 
    # Seleccionar busqueda
    
    def selDes(event):
        
        def vModo():
            
            ventanaModoTrans = OptionMenu(ventana7, varModo, *opciones2)
            ventanaModoTrans.config(width=20)
            ventanaModoTrans.place(x = 350, y = 120)
            
            
            
        
        if varDes.get() == 'Base Completa':
            opciones2 = ['Usuario','Prestamo', 'Libro']
            varModo.set('Seleccionar rubro')
            tipoBus.set("BC")
            vModo()
            
        elif varDes.get() == 'Usuario':
            opciones2 = ['Id', 'Nombre','Apellido Paterno','Apellido Materno','Edad']
            varModo.set('Seleccionar rubro')
            tipoBus.set("UsuariosBD")
            vModo()
            
        elif varDes.get() == 'Prestamo':
            opciones2 = ['Fecha Inicial', 'Fecha Final','Libros','Estado']
            varModo.set('Seleccionar rubro')
            tipoBus.set("prestamos_table")
            vModo()
            
        elif varDes.get() == 'Libro':
            opciones2 = ['Autor', 'Título','Clave','Colección', '# ejemplar', 'Volumen', '# Adquisición', '# Tarjeta', 'ISBN', 'Clasificación']
            varModo.set('Seleccionar rubro')
            tipoBus.set("libros_table")
            vModo()
        
        
        
            
    #----------------------
    
    varDes = StringVar(ventana7)
    varDes.set('Seleccionar tabla')

    varModo = StringVar(ventana7)
    varModo.set('Seleccionar rubro')
    

    opciones = ['Base Completa', 'Usuario','Prestamo', 'Libro']
    ventanaDeslizante = OptionMenu(ventana7, varDes, *opciones, command=selDes)
    ventanaDeslizante.config(width=20)
    ventanaDeslizante.place(x = 80, y = 120)
    
    
    #tipoBus = StringVar()
    
    boton_buscar = tkinter.Button(ventana7, text = "Buscar",command = buscarBD).place(x = 400, y = 200)

main_account_screen() # call the main_account_screen() function
