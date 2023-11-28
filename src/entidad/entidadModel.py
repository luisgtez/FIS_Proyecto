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
    
    def getNombreEntidad(self, entidad_id):
        query= """SELECT NombreEntidad 
                FROM Entidad
                WHERE ID = ?;"""
        
        res = self.db.executeQuery(query,entidad_id)
        # Comprobamos que el resultado tiene un único elemento
        if len(res)==1:
        # Si tiene un único elemento, devolvemos el nombre
            return res[0].get("NombreEntidad")
        else:
        # Si no tiene un único elemento, devolvemos None
            return None

    def getNombreActividadEntidad(self, actividad_id):
        query= """SELECT NombreActividad 
                FROM ActividadEntidad
                WHERE ID = ?;"""
        
        res=self.db.executeQuery(query,actividad_id)

        # Comprobamos que el resultado tiene un único elemento
        if len(res)==1:
        # Si tiene un único elemento, devolvemos el nombre
            return res[0].get("NombreActivvidad")
        else:
        # Si no tiene un único elemento, devolvemos None
            return None

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

  
    def getInscripcionesActividad(self, actividad_id):
        #Peticion a la base de datos para obtenerlas inscripciones de la actividad
        query="""SELECT
                I.ID,
                D.CorreoElectronico,
                D.Nombre,
                D.Apellidos
                FROM Deportista D
                JOIN Inscripcion I ON D.ID = I.DeportistaID
                WHERE I.ActividadEntidadID = ?;"""
        
        return self.db.executeQuery(query,actividad_id)

