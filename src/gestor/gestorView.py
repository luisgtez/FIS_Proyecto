from gestor.gestorModel import GestorModel
from util.Utils import utils

class GestorView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los deportistas que estarán
    representadas en la clase DeportistaModel (DeportistaModel.py)
    '''
     
    def __init__ (self):
        self.gestor = GestorModel() #Crea un objeto model que se invocará desde esta vista
        
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

    # Vista para la HU de ver estado de forma 
    def getEstadoFormaView(self):
        
        resultados=self.gestor.gestorEstadoForma()
        
        estado_forma = {}
        for dict in resultados:
            estado_forma[dict["ID"]] = dict["EstadoForma"]
        return estado_forma      
            
    def masActivos(self):
    # Mostrar los resultados por consola
        resultados = self.gestor.getMasActivos()
        # for fila in resultados:
        #     nombre_deportista, fecha_alta, total_actividades = fila["NombreDeportista"], fila["FechaAlta"], fila["TotalActividades"]
        #     print(f"Nombre: {nombre_deportista}, Fecha de Alta: {fecha_alta}, Total de Actividades: {total_actividades}")
        utils.printTable(resultados)
