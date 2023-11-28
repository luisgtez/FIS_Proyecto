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
                        
                        "7": self.deportista.showActividadesDeportistaTipo,
                        "8": self.deportista.showComparacion,
                        
                        "9":self.entidad.showRegistro,
                        "10": self.entidad.addActividadEntidad,
                            
                        "11": self.gestor.gestorEstadoview,
                        "12": self.gestor.masActivos,
                        "13": self.gestor.añadirTipoActividad_view,
                        "14": self.gestor.añadirSubtipoActividad_view,
                        
                        "15": self.quit
                          }
        
    def displayMenu (self):
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
              
              ----- Deportista Premium ------------------------
              7.- Resumen de actividad de deportista por tipo
              8.- Comparar con deportista

              ----- Entidad -----------------------------------
              9.- Registrar nueva entidad
              10.- Registrar nueva actividad programada
              
              ----- Gestor ------------------------------------
              11.- Datos Deportistas
              12.- Deportistas más activos
              13.- Añadir Tipo de Actividad
              14.- Añadir Subtipo de Actividad
              """)
        print("#"*20)
        print("15.- Salir")
        
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
