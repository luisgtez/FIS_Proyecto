
import sys
from gestor.gestorModel import GestorModel

class GestorView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los deportistas que estarán
    representadas en la clase DeportistaModel (DeportistaModel.py)
    '''
     
    def __init__ (self):
        self.gestor = GestorModel() #Crea un objeto model que se invocará desde esta vista
        
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        # self.choices = { "1": self.addActivity,
        #                  "2": self.showSummary,
        #                  "3": self.quit
        #                }
    
    # def displayMenu (self):
    #     print("#"*20)
    #     print(""" Opciones: \n
    #           1.- Registrar nueva actividad
    #           2.- Resumen de actividad
    #           3.- Salir 
    #           """)
    
    #Muestra la lista de opciones y permite la selección
    # def run (self):
    #     while True:
    #         self.displayMenu()
    #         choice = input("Introducir opción: ")
    #         action = self.choices.get(choice)
    #         if action:
    #             action()
    #         else:
    #             print("{0} no es una opción valida\n".format(choice))


    def gestorEstadoview(self):
        resultados = self.gestor.gestorEstado()
        
        total_activos = resultados["total_activos"]
        total_premium = resultados["total_premium"]
        total_free = resultados["total_free"]
        resultados_sexo = resultados["resultados_sexo"]
        resultados_edad = resultados["resultados_edad"]
                
        print("#"*20)
        print("Total de deportistas activos:", total_activos)
        print("Porcentaje de perfiles Premium:", total_premium / (total_premium + total_free) * 100, "%")
        print("Porcentaje de perfiles Free:", total_free / (total_premium + total_free) * 100, "%")
        print("Porcentaje por sexo:")
        for resultado_sexo in resultados_sexo:
            print(f"\t{resultado_sexo['Sexo']}: {resultado_sexo['Porcentaje']:.2f}%")
        print("Porcentaje por rango de edad:")
        for resultado_edad in resultados_edad:
            print(f"\t{resultado_edad['RangoEdad']}: {resultado_edad['Porcentaje']:.2f}%")

    # def quit(self):
    #     print("Cerrando opciones.")
    #     sys.exit(0)

    # #Médodo muy general para imprimir los resultados (res) que vienen del model
    # def printResults (self,res):
    #     if len(res)==0: 
    #         print ("No hay resultados")
    #     else:
    #         #cabecera
    #         print (list(res[0].keys())) # Imprime nombres de columnas (keys del diccionario)
    #         print ("----------------------------------")
    #         #contenido 
    #         for row in res:
    #             print ([*row.values()]) # Imprime valor de una fila (values del diccionario)
    #         print ("----------------------------------")

    # Vista para la HU de ver estado de forma 
    def getEstadoFormaView(self):
        
        resultados=self.gestor.gestorEstadoForma()

        for deportista in resultados:
            id=deportista["ID"]
            estadoforma=deportista["EstadoForma"]
            print(f"ID: {id}")
            print(f"Estado de forma: {estadoforma}")