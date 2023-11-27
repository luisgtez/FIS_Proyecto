from util.database import DataBase
from datetime import datetime, timedelta

class EntidadModel:
    '''
    Clase que representa los objetos de negocio (model) relativos a las funcionalidades de 
    las entidades. Varios métodos de esta clase se invocarán desde la vista (EntidadView), y los resultados
    se devolverán nuevamente a la vista para su visualización
    '''
    
    def __init__ (self):
        self.db = DataBase ("AppDB.db") # Crea un objeto DataBase con la ruta de la base de datos

    def InsertActividadEntidad(self, idEntidad, nombreActividad, descripcion, fecha, duracion_dias, numPlazas, coste):
        '''Método que inserta una actividadEntidad en la base de datos
        
        Parámetros
        ----------
        idEntidad : int  
            ID de la entidad que programa la actividad.
        nombreActividad : str
            Nombre de la actividad.
        descripcion : str
            Breve descripción de la actividad.
        fecha : str
            Fecha de la actividad.
        duracion_dias : integer
            Duración de la actividad en días.
        numPlazas : integer
            Número de plazas disponibles en la actividad.
        coste: decimal
            Coste de la actividad para usuarios free.
        
        
        Devuelve
        -------
        str
            "OK" si la inserción se ha realizado correctamente.
        '''
        # Creamos una query para insertar los datos en la tabla Actividad
        query = """ 
                insert into ActividadEntidad(ID, EntidadID, NombreActividad, Descripcion, Fecha, DuracionDias, NumPlazas, Coste) values (null,?,?,?,?,?,?,?) 
                """ 
        # Ejecutamos la query con los parámetros correspondientes
        self.db.executeUpdateQuery(query,idEntidad,nombreActividad,descripcion,fecha,duracion_dias,numPlazas, coste)
        
        # Devolvemos "OK"
        return "OK"
    
    def registrarEntidad(self, nombre):
        # Obtener la fecha actual como fecha de alta
        fecha_alta = datetime.now().date()

        # Insertar la nueva entidad en la tabla Entidad
        query_insert = """
            INSERT INTO Entidad(
                ID,
                NombreEntidad
            ) VALUES (null,?)
        """
        self.db.executeUpdateQuery(
            query_insert,
            nombre
        )


        # Mostrar justificante con los datos proporcionados y la fecha de alta
        print("Justificante de Registro:")
        print(f"Nombre de Entidad: {nombre}")
        print(f"Fecha de Alta: {fecha_alta}")
        print("\nGuarde esta información para futuras referencias.")

        print("Registro exitoso. ¡Bienvenido a la aplicación!")

        
    
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
