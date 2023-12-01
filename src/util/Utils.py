from util.database import DataBase
import re

class utils:
    
    def __init__(self) -> None:
        self.db = DataBase("AppDB.db")
    
    def printTable(res):
        # Si la lista está vacía, no hay resultados
        if len(res) == 0:
            print("No hay resultados")
            return
        
        # Get maximum length of each column
        max_len = {}
        for key in res[0].keys():
            max_len[key] = len(key)

        for dict in res:
            for key, value in dict.items():
                if len(str(value)) > max_len[key]:
                    max_len[key] = len(str(value))
        # Print top row of table
        print("+" + "-" * (sum(max_len.values()) + 2 * len(max_len)) + "+")
        # Print header
        print("|", end=" ")
        for key in res[0].keys():
            print(key.ljust(max_len[key]), end=" |")
        print()
        print("|" + "-" * (sum(max_len.values()) + 2 * len(max_len) ) + "|")


        # Print content
        for i, dict in enumerate(res):
            print("|", end=" ")
            for key, value in dict.items():
                print(str(value).ljust(max_len[key]), end=" |")
            print()

            # Print line of -- and | between rows
            if i < len(res) - 1:
                print("|" + "-" * (sum(max_len.values()) + 2 * len(max_len)) + "|")


        print("+" + "-" * (sum(max_len.values()) + 2 * len(max_len)) + "+")

    def comprobarExisteCorreo(self,correo):
        query = "SELECT CorreoElectronico FROM Deportista"
        
        res = self.db.executeQuery(query)
        
        for row in res:
            if row["CorreoElectronico"] == correo:
                return True
        
        return False
    
    def comprobarCorreoEscrito(self,correo):
        reg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(reg,correo)
    
    def mapTiposActividad(self):
        '''Método que obtiene los tipos de actividad unicos
        
        Devuelve
        -------
        dict
            Diccionario con los tipos de actividad unicos. Clave: ID del tipo de actividad, Valor: Tipo de actividad.
        '''
        # Creamos una query para obtener los tipos de actividad unicos
        query = "SELECT DISTINCT Tipo, ID FROM TipoActividad"
        
        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query)
        
        # Creamos un diccionario con los tipos de actividad unicos
        tipos_actividad = {dict_values["ID"] : dict_values["Tipo"] for dict_values in result}
        
        # Retornamos el diccionario
        return tipos_actividad
    
    def mapSubtiposActividad(self,TipoActividad):
        
        '''Método que obtiene los subtipos de actividad unicos de un tipo de actividad
        
        Parámetros
        ----------
        TipoActividad : int
            ID del tipo de actividad del que se quiere obtener los subtipos.
            
        Devuelve
        -------
        dict
            Diccionario con los subtipos de actividad unicos. Clave: ID del subtipo de actividad, Valor: Subtipo de actividad.
        '''
        
        # Creamos una query para obtener los subtipos de actividad unicos
        query = "SELECT DISTINCT Subtipo, ID FROM SubtipoActividad where TipoActividadID = ?"
        
        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query,TipoActividad)
        
        # Creamos un diccionario con los subtipos de actividad unicos
        subtipos_actividad = {dict_values["ID"] : dict_values["Subtipo"] for dict_values in result}
        
        # Retornamos el diccionario
        return subtipos_actividad
    
    def tiposActividad(self):
        '''
        Método que obtiene los tipos de actividad de la base de datos unicos
        '''
        # Creamos una query para obtener los tipos de actividad unicos
        query = "SELECT DISTINCT Tipo FROM TipoActividad"
        
        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query)
        
        # Creamos una lista con los tipos de actividad unicos
        tipos_actividad = [dict_values["Tipo"] for dict_values in result]
        
        # Retornamos la lista
        return tipos_actividad
    
    def subtiposActividad(self,TipoActividad):
        '''
        Método que obtiene los distintos subtipos de actividad de la base de datos unicos de un tipo de actividad
        '''
        
        # Creamos una query para obtener los subtipos de actividad unicos
        query = "SELECT DISTINCT Subtipo FROM SubtipoActividad where TipoActividadID = ?"
        
        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query,TipoActividad)
        
        # Creamos una lista con los subtipos de actividad unicos
        subtipos_actividad = [dict_values["Subtipo"] for dict_values in result]
        
        # Retornamos la lista
        return subtipos_actividad
    
    '''
    HU #23773
    '''  
    def mapEntidades(self):
        '''Método que obtiene las entidades
        
        Devuelve
        -------
        dict
            Diccionario con las entidades. Clave: ID de la entidad, Valor: entidad.
        '''
        # Creamos una query para obtener los tipos de actividad unicos
        query = "SELECT DISTINCT ID, NombreEntidad FROM Entidad"
        
        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query)
        
        # Creamos un diccionario con los tipos de actividad unicos
        entidades = {dict_values["ID"] : dict_values["NombreEntidad"] for dict_values in result}
        
        # Retornamos el diccionario
        return entidades
        
    def mapActividadesEntidad(self, idEntidad):
            '''Método que obtiene las actividades de una entidad
            
            Devuelve
            -------
            dict
                Diccionario con las actividades de una entidad. Clave: ID de la actividad, Valor: Nombre de la actividad.
            '''
            # Creamos una query para obtener las actividades de la entidad
            query = "SELECT ID, NombreActividad FROM ActividadEntidad WHERE EntidadID = ?;"
            
            # Ejecutamos la query y guardamos el resultado en result
            result = self.db.executeQuery(query, idEntidad)
            
            # Creamos un diccionario con las actividades de la entidad
            actividades = {dict_values["ID"] : dict_values["NombreActividad"] for dict_values in result}
            
            # Retornamos el diccionario
            return actividades
