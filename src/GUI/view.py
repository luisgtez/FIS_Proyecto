import sys
from deportista.deportistaView import DeportistaView
from gestor.gestorView import GestorView
import datetime

class View:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los deportistas que estarán
    representadas en la clase DeportistaModel (DeportistaModel.py)
    '''
     
    def __init__ (self):
        self.deportista = DeportistaView () #Crea un objeto model que se invocará desde esta vista
        self.gestor = GestorView() #Crea un objeto model que se invocará desde esta vista
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        self.choices = { "1": self.deportista.addActivity,
                         "2": self.deportista.showSummary,
                         "3": self.gestor.gestorEstadoview,
                         "4":self.gestor.getEstadoFormaView,
                         "5":self.deportista.showComparacion,
                         "6": self.quit
                       }
        
    def displayMenu (self):
        print("#"*20)
        print(""" Opciones: \n
              1.- Registrar nueva actividad
              2.- Resumen de actividad
              3.- Datos Deportistas (Gestor)
              4.- Estado de Forma Deportistas (Gestor)
              5.- Comparar con deportista (Premium)
              6.- Salir 
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