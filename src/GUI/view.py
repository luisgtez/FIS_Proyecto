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
                        "2": self.deportista.importar_csv_view,
                        "3": self.deportista.inscribir_actividad,
                        "4": self.deportista.showInscripcionesDeportista,
                        "5": self.deportista.showSummary,
                        "6": self.deportista.showActividadesEnPeriodo,
                        "7": self.deportista.addObjetivoSemanalView,
                        "8": self.deportista.mostrarProgresoObjetivos,
                        "9": self.deportista.showInforme,
                        "10": self.deportista.showSeguir,

                        "11": self.deportista.showActividadesDeportistaTipo,
                        "12":self.deportista.showComparacion,
                        "13": self.deportista.mostrarComparacionGrupoEdad,
                        
                        "14": self.entidad.showRegistro,
                        "15": self.entidad.addActividadEntidad,
                        "16": self.entidad.showInscripcionesActividad,
                        
                        "17": self.gestor.gestorEstadoview,
                        "18": self.gestor.masActivos,
                        "19": self.gestor.añadirTipoActividad_view,
                        "20": self.gestor.añadirSubtipoActividad_view,
                        "21": self.gestor.inscripcionesEntidades,
                        
                        "22": self.quit
                          }

    def displayMenu(self):
        print("#"*20)
        print(""" Opciones: \n
                ----- Deportista ---------------------------------
                0.- Registrar nuevo deportista
                
                1.- Registrar nueva actividad
                2.- Importar actividades CSV
                3.- Inscribirme en una actividad programada
                4.- Enseñar inscripciones de un deportista
                5.- Resumen de actividad
                6.- Resumen de actividad entre dos fechas
                7.- Añadir objetivo semanal
                8.- Mostrar progreso de objetivos
                9.- Informe de actividad
                10.- Seguir a un deportista
                
                ----- Deportista Premium ------------------------
                11.- Resumen de actividad de deportista por tipo
                12.- Comparar con deportista
                13.- Comparar con deportistas de mi grupo de edad
                
                
                ----- Entidad -----------------------------------
                14.- Registrar nueva entidad
                15.- Registrar nueva actividad programada
                16.- Mostrar inscripciones de una actividad programada
                
                ----- Gestor ------------------------------------
                17.- Datos Deportistas
                18.- Deportistas más activos
                19.- Añadir Tipo de Actividad
                20.- Añadir Subtipo de Actividad
                21.- Monstrar Inscripciones de cada Entidad
                
                22.- Salir
                
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
