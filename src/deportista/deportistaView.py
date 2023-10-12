
import sys
from deportista.deportistaModel import DeportistaModel


class DeportistaView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los deportistas que estarán
    representadas en la clase DeportistaModel (DeportistaModel.py)
    '''
     
    def __init__ (self):
        self.deportista = DeportistaModel () #Crea un objeto model que se invocará desde esta vista
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        self.choices = { "1": self.addActivity,
                         "2": self.quit
                       }
    
    def displayMenu (self):
        print("#"*20)
        print(""" Opciones: \n
              1.- Registrar nueva actividad
              2.- Salir 
              """)
    
    #Muestra la lista de opciones y permite la selección
    def run (self):
        while True:
            self.displayMenu()
            choice = input("Introducir opción: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} no es una opción valida\n".format(choice))
    
    #Vista para la HU Registrar una nueva actividad
    def addActivity(self):
        print("#"*20)
        correoDeportista = input ("Introducir tu correo: ")
        #Invocación al modelo para obtener el id de la compañia
        idDeportista = self.deportista.getIdDeportista(correoDeportista)
        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
        else:
            nombre,apellidos = self.deportista.getNombreCompletoDeportista(correoDeportista)
            print(f"Iniciado sesion: {correoDeportista}")
            print(f"¡Bienvenido {nombre} {apellidos}!" )
            
            print("\nIntrodcir los datos de la actividad")
            fecha = input ("Fecha: ")
            duracion_horas = input ("Duracion en horas: ")
            localizacion = input ("Localizacion: ")
            distancia_kms = input ("Distancia en kms: ")
            FC_max = input ("FC max (opcional): ")
            FC_min = input ("FC min (opcional): ")
            tipo_actividad = input (f"Tipo de actividad : ")
            
            #Invocación al modelo para insertar la actividad
            self.deportista.insertActivity(fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad,idDeportista)
            print(f"Se ha registrado la actividad de {tipo_actividad} el {fecha} en {localizacion} con una duracion de {duracion_horas} horas y una distancia de {distancia_kms} kms")
            
            
            
            
            
    def quit(self):
        print("Cerrando opciones.")
        sys.exit(0)

    #Médodo muy general para imprimir los resultados (res) que vienen del model
    def printResults (self,res):
        if len(res)==0: 
            print ("No hay resultados")
        else:
            #cabecera
            print (list(res[0].keys())) # Imprime nombres de columnas (keys del diccionario)
            print ("----------------------------------")
            #contenido 
            for row in res:
                print ([*row.values()]) # Imprime valor de una fila (values del diccionario)
            print ("----------------------------------")


        