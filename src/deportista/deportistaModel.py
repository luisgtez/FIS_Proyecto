from util.database import DataBase

class DeportistaModel:
    '''
    Clase que representa los objetos de negocio (model) relativos a las funcionalidades de 
    los deportistas. Varios métodos de esta clase se invocarán desde la vista (DeportistaView), y los resultados
    se devolverán nuevamente a la vista para su visualización
    '''
    
    def __init__ (self):
        self.db = DataBase ("AppDB.db") # Crea un objeto DataBase con la ruta de la base de datos

    def getIdDeportista(self,correoDeportista):
        '''Método que obtiene el ID de un deportista a partir de su correo electrónico.
        
        Parámetros
        ----------
        correoDeportista : str
            Correo electrónico del deportista del que se quiere obtener el ID.
        
        Devuelve
        -------
        int or None
            ID del deportista si existe en la base de datos, None en caso contrario.
        '''
        # Creamos una query para obtener el ID del deportista a partir de su correo electrónico
        query = """select id from Deportista where Deportista.CorreoElectronico = ?"""
        
        # Ejecutamos la query, guardamos el resultado en res
        res = self.db.executeQuery(query,correoDeportista)
        
        # Comprobamos que el resultado tiene un único elemento
        if len(res)==1:
            # Si tiene un único elemento, devolvemos el ID del deportista
            return res[0].get("ID")
        
        else:
            # Si no tiene un único elemento, devolvemos None
            return None
    
    def getNombreCompletoDeportista(self,correoDeportista):
        '''Método que obtiene el nombre y apellidos de un deportista a partir de su correo electrónico	
        
        Parámetros
        ----------
        correoDeportista : str
            Correo electrónico del deportista del que se quiere obtener el nombre y apellidos.
        
        Devuelve
        -------
        str or None
            Nombre del deportista si existe en la base de datos, None en caso contrario.
        '''
        # Creamos una query para obtener el nombre y apellidos del deportista a partir de su correo electrónico
        query = """select Nombre, Apellidos from Deportista
                   where Deportista.CorreoElectronico = ?
                """
        
        # Ejecutamos la query, guardamos el resultado en res
        res = self.db.executeQuery(query,correoDeportista)
        
        # Comprobamos que el resultado tiene un único elemento
        if len(res)==1:
            # Si tiene un único elemento, devolvemos el nombre y apellidos del deportista
            return res[0].get("Nombre"),res[0].get("Apellidos")
        else:
            # Si no tiene un único elemento, devolvemos None
            return None,None
    
    def insertActivity(self,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad_id,subtipo_actividad_id,idDeportista):
        '''Método que inserta una actividad en la base de datos
        
        Parámetros
        ----------
        fecha : str
            Fecha de la actividad.
        duracion_horas : float
            Duración de la actividad en horas.
        localizacion : str
            Localización de la actividad.
        distancia_kms : float
            Distancia recorrida en la actividad en kilómetros.
        FC_max : int
            Frecuencia cardíaca máxima alcanzada en la actividad.
        FC_min : int
            Frecuencia cardíaca mínima alcanzada en la actividad.
        tipo_actividad_id : int
            ID del tipo de actividad.
        subtipo_actividad_id : int
            ID del subtipo de actividad.
        idDeportista : int  
            ID del deportista que realiza la actividad.
        
        Devuelve
        -------
        str
            "OK" si la inserción se ha realizado correctamente.
        '''
        # Creamos una query para insertar los datos en la tabla Actividad
        query = """ 
                insert into Actividad(ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, TipoActividadID,SubtipoActividadID, DeportistaID) values (null,?,?,?,?,?,?,?,?,?) 
                """ 
        # Ejecutamos la query con los parámetros correspondientes
        self.db.executeUpdateQuery(query,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad_id,subtipo_actividad_id,idDeportista)
        
        # Devolvemos "OK"
        return "OK"
            
    def getSummary(self,idDeportista):
        '''Método que obtiene un resumen de las actividades realizadas por un deportista
        
        Parámetros
        ----------
        idDeportista : int
            ID del deportista del que se quiere obtener el resumen de actividades.
            
        Devuelve
        -------
        list
            Lista de diccionarios con el resumen de las actividades realizadas por el deportista.
        '''
        
        # Creamos una query para obtener el resumen de las actividades realizadas por el deportista
        query = "select TipoActividadID, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal from Actividad where DeportistaID = ? group by TipoActividadID"
        
        # Ejecutamos la query y la retornamos
        return self.db.executeQuery(query,idDeportista)
    
    def premium(self,idDeportista):
        '''Método que comprueba si un deportista es premium
        
        Parámetros
        ----------
        idDeportista : int
            ID del deportista del que se quiere comprobar si es premium.
            
        Devuelve
        -------
        bool
            True si el deportista es premium, False en caso contrario.
        '''
        # Creamos una query para obtener el campo Premium de la tabla Deportista
        query="""
                select Premium from Deportista 
                where Deportista.ID=?"""
        
        # Ejecutamos la query y retornamos el resultado
        return self.db.executeQuery(query,idDeportista)
    
    # Obtener sexo y fecha de nacimiento de un deportista
    def getSexoFecha(self,idDeportista):
        query="""
                select Sexo,FechaNacimiento from Deportista
                where Deportista.ID=?"""
        res = self.db.executeQuery(query,idDeportista)
        if len(res)==1:
            return res[0].get("Sexo"),res[0].get("FechaNacimiento")
        else:
            return None,None
        
    #obtener los detalles de las actividades realizadas por un deportista en un periodo de tiempo
    def getActividadesEnPeriodo(self, idDeportista, fecha_inicio, fecha_fin):

        queryActividadesIntervalo = """select Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, TipoActividad
                                       from Actividad where DeportistaID = ? and Fecha between ? and ?"""
        resultActividades = self.db.executeQuery(queryActividadesIntervalo, idDeportista, fecha_inicio, fecha_fin)

        return resultActividades
    
    #Como deportista “Premium” obtener la actividad de otro deportista por tipo de actividad a lo largo del tiempo.
    def getActividadesDeportistaTipo(self, idDeportista, tipoActividad):
       
        queryActividadesDeportista = "select Fecha, DuracionHoras, DistanciaKms from Actividad where DeportistaID = ? and TipoActividad = ? order by Fecha desc"
        resultActividades = self.db.executeQuery(queryActividadesDeportista, idDeportista, tipoActividad)
        
        return resultActividades
    
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
        '''Método que obtiene los subtipos de actividad unicos
        
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