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
        self.utils = utils()
    
    # Vista para la HU para ver estadisticas de los usuarios registrados
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
        
        idDeportista = input("Introduzca el ID del deportista: ")
        # Comprobamos que el ID es un entero
        try:
            idDeportista = int(idDeportista)
        except ValueError:
            print("El ID del deportista debe ser un entero")
            return
        
        # Comprobamos que el ID existe en la base de datos
        if not self.gestor.existeID(idDeportista):
            print("El ID del deportista no existe en la base de datos")
            return
        
        # Obtenemos el estado de forma del deportista
        estado_forma = self.gestor.gestorEstadoForma(idDeportista)
        
        # Mostramos el estado de forma del deportista
        print(f"Estado de forma del deportista con ID {idDeportista}: {estado_forma}")

    def masActivos(self):
    # Mostrar los resultados por consola
        resultados = self.gestor.getMasActivos()
        # for fila in resultados:
        #     nombre_deportista, fecha_alta, total_actividades = fila["NombreDeportista"], fila["FechaAlta"], fila["TotalActividades"]
        #     print(f"Nombre: {nombre_deportista}, Fecha de Alta: {fecha_alta}, Total de Actividades: {total_actividades}")
        utils.printTable(resultados)

    '''
    HU #23655
    '''
    def añadirTipoActividad_view(self):
        
        tipos = self.utils.tiposActividad()
        
        print("Estos son los tipos de actividad ya guardados:")
        for tipo in tipos:
            print(f"\t{tipo}")
        
        tipo = input("Introduzca el tipo de actividad: ")
        while tipo in tipos:
            print("El tipo de actividad ya existe")
            tipo = input("Introduzca el tipo de actividad: ")
        
        MET = input("Introduzca el MET de la actividad: ")
        
        while not MET.isnumeric():
            print("El MET debe ser un número")
            MET = input("Introduzca el MET de la actividad: ")
        
        MET = int(MET)
        
        self.gestor.añadirTipo(tipo, MET)
        print("Tipo añadido correctamente")
        
    def añadirSubtipoActividad_view(self):
        
        print("Elige a que tipo de actividad quieres añadir un subtipo:")
        tipos = self.utils.tiposActividad()
        for i, tipo in enumerate(tipos):
            print(f"\t{i+1}: {tipo}")
            
        opcion = input("Introduzca el número de la opción: ")
        while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > len(tipos):
            print("Opción no válida")
            opcion = input("Introduzca el número de la opción: ")
            
        opcion = int(opcion)
        tipo = tipos[opcion-1]
        
        map_tipos = self.utils.mapTiposActividad()
        invert_map_tipos = {v:k for k,v in map_tipos.items()}
        
        tipo_id = invert_map_tipos[tipo]
        subtipos = self.utils.subtiposActividad(tipo_id)
        
        if subtipos == []:
            print(f"No hay subtipos de '{tipo}' guardados")
        else:
            print(f"Estos son los subtipos de '{tipo}' ya guardados:")
            for subtipo in subtipos:
                print(f"\t{subtipo}")
            
        subtipo = input("Introduzca el subtipo de actividad: ")
        
        while subtipo in subtipos:
            print("El subtipo de actividad ya existe")
            subtipo = input("Introduzca el subtipo de actividad: ")
            
        self.gestor.añadirSubtipo(subtipo, tipo_id)
        print("Subtipo añadido correctamente")
    
    '''
    HU #23773
    '''  
    def inscripcionesEntidades(self):
        print("#"*20)
        res=self.gestor.getTotalInscripcionesEntidades()
        print("Total de inscripciones de cada entidad colaboradora:")
        
        utils.printTable(res)
        # for dict in res:
        #     print(f"Entidad: {dict['NombreEntidad']} | Inscripciones Totales: {dict['TotalInscripciones']}")