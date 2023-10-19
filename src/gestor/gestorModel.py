
import sys
from deportista.deportistaModel import DeportistaModel
import datetime

class GestorView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los deportistas que estarán
    representadas en la clase DeportistaModel (DeportistaModel.py)
    '''
     
    def __init__ (self):
        self.deportista = DeportistaModel () #Crea un objeto model que se invocará desde esta vista
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        self.choices = { "1": self.addActivity,
                         "2": self.showSummary,
                         "3": self.quit
                       }
    
    def displayMenu (self):
        print("#"*20)
        print(""" Opciones: \n
              1.- Ver mas activos por orden
              2.- Ver estado de forma
              3.- Salir 
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
  
    #Vista para la HU Resumen básico sobre mi actividad deportiva a lo largo del tiempo, incluyendo el estado de forma
    def showSummary(self):
        '''
        El deportista se identifica mediante su correo electrónico y se mostrarán sus datos. A continuación, se genera un listado con tipo de actividad, número de sesiones y total distancia, y se mostrará el indicativo sobre el estado de forma del deportista.
        '''
        print("#"*20)
        correoDeportista = input ("Introducir tu correo: ")
        #Invocación al modelo para obtener el id de la compañia
        idDeportista = self.deportista.getIdDeportista(correoDeportista)
        
        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
        else:
            nombre,apellidos = self.deportista.getNombreCompletoDeportista(correoDeportista)
            print(f"Iniciado sesion: {correoDeportista}")
            print(f"\n¡Bienvenido {nombre} {apellidos}!" )
            
            print("\nResumen de actividad: ")
            print ("----------------------------------")

            #Invocación al modelo para obtener el resumen
            res = self.deportista.getSummary(idDeportista)
            self.printResults(res)
            
            
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


        