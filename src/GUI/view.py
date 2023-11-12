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
        self.choices = {"1": self.deportista.addActivity,
                        "2": self.deportista.importar_csv_view,
                        "3": self.deportista.showSummary,
                        "4": self.deportista.showActividadesEnPeriodo,
                        "5": self.deportista.showActividadesDeportistaTipo,
                        "6": self.deportista.showComparacion,
                        "7": self.gestor.gestorEstadoview,
                        "8": self.gestor.getEstadoFormaView,
                        "9": self.gestor.masActivos,
                        "10": self.quit,
                          }
        
    def displayMenu (self):
        print("#"*20)
        print(""" Opciones: \n
                1.- Registrar nueva actividad
                2.- Importar actividades CSV
                3.- Resumen de actividad
                4.- Resumen de actividad entre dos fechas
                5.- Resumen de actividad de deportista por tipo (Premium)
                6.- Comparar con deportista (Premium)
                7.- Datos Deportistas (Gestor)
                8.- Estado de Forma Deportistas (Gestor)
                9.- Deportistas más activos (Gestor)
                10.- Salir
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
