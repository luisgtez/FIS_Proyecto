import sys
from deportista.deportistaView import DeportistaView
from gestor.gestorView import GestorView
from entidad.entidadView import EntidadView

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
                        "1": self.deportista.addActivity,
                        "2": self.deportista.inscribir_actividad,
                        "3": self.deportista.importar_csv_view,
                        "4": self.deportista.showSummary,
                        "5": self.deportista.showActividadesEnPeriodo,
                        "6": self.deportista.addObjetivoSemanalView,
                        "7": self.deportista.showInscripcionesDeportista,
                        "8": self.deportista.showSeguir,
                        "9": self.deportista.showInforme,
                        
                        "10": self.deportista.showActividadesDeportistaTipo,
                        "11": self.deportista.showComparacion,
                        
                        "12":self.entidad.showRegistro,
                        "13": self.entidad.addActividadEntidad,
                        "14": self.entidad.showInscripcionesActividad,
                        
                        "15": self.gestor.gestorEstadoview,
                        "16": self.gestor.masActivos,
                        "17": self.gestor.añadirTipoActividad_view,
                        "18": self.gestor.añadirSubtipoActividad_view,
                        "19": self.gestor.inscripcionesEntidades,
                        
                        "20": self.quit
                          }

    def displayMenu(self):
        print("#"*20)
        print(""" Opciones: \n
                ----- Deportista ---------------------------------
                0.- Registrar nuevo deportista
                
                1.- Registrar nueva actividad
                2.- Inscribirme en una actividad programada
                3.- Importar actividades CSV
                4.- Resumen de actividad
                5.- Resumen de actividad entre dos fechas
                6.- Añadir objetivo semanal
                7.- Enseñar inscripciones de un deportista
                8.- Seguir a un deportista
                9.- Informe de actividad
                
                ----- Deportista Premium ------------------------
                10.- Resumen de actividad de deportista por tipo
                11.- Comparar con deportista
                
                ----- Entidad -----------------------------------
                12.- Registrar nueva entidad
                13.- Registrar nueva actividad programada
                14.- Inscripciones de una Actividad
                
                ----- Gestor ------------------------------------
                15.- Datos Deportistas
                16.- Deportistas más activos
                17.- Añadir Tipo de Actividad
                18.- Añadir Subtipo de Actividad
                19.- Monstrar Inscripciones de cada Entidad
                
                20.- Salir
                """)
        print("#"*20)
        
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
