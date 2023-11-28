import sys
from deportista.deportistaView import DeportistaView
from gestor.gestorView import GestorView
from entidad.entidadView import EntidadView
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
        self.entidad = EntidadView()  #Crea un objeto model que se invocará desde esta vista
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        self.choices = {
                        "0":self.deportista.showRegistro,
                        "1":self.entidad.showRegistro,
                            
                        "2": self.deportista.addActivity,
                        "3": self.entidad.addActividadEntidad,
                        "4": self.deportista.importar_csv_view,
                        "5": self.deportista.showSummary,
                        "6": self.deportista.showActividadesEnPeriodo,
                        "7": self.deportista.showInscripcionesDeportista,
                        "8": self.deportista.addObjetivoSemanalView,
                        "9": self.entidad.showInscripcionesActividad,
                        "10": self.deportista.showActividadesDeportistaTipo,
                        "11": self.deportista.showComparacion,
                        "12": self.gestor.gestorEstadoview,
                        "13": self.gestor.masActivos,
                        "14": self.gestor.añadirTipoActividad_view,
                        "15": self.gestor.añadirSubtipoActividad_view,
                        "16": self.gestor.inscripcionesEntidades,
                        "17": self.deportista.showSeguir,
                        "18": self.deportista.showInforme,
                        "19": self.quit
                          }
        
    def displayMenu (self):
        print("#"*20)
        print(""" Opciones: \n
              0.- Registrar nuevo deportista
              1.- Registrar nueva entidad (Entidad)
              
              2.- Registrar nueva actividad
              3.- Registrar nueva actividad (Entidad)
              4.- Importar actividades CSV
              5. -Resumen de actividad
              6.- Resumen de actividad entre dos fechas
              7.- Histórico de Inscripciones a Actividades
              8.- Añadir objetivo semanal
              9.- Inscripciones de una Actividad (Entidad)
              10.- Resumen de actividad de deportista por tipo (Premium)
              11.- Comparar con deportista (Premium)
              12.- Datos Deportistas (Gestor)
              13.- Deportistas más activos (Gestor)
              14.- Añadir Tipo de Actividad (Gestor)
              15.- Añadir Subtipo de Actividad (Gestor)
              16.- Monstrar Inscripciones de cada Entidad (Gestor)
              17.- Seguir a un deportista (Premium)
              18.- Informe de actividad 
              19.- Salir
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
