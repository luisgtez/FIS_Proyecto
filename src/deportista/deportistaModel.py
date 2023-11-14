from util.database import DataBase
from datetime import datetime, timedelta

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


    
    #Como deportista quiero añadir objetivos semanales
    def addObjetivoSemanal(self, idDeportista):
        print("¿Qué tipo de objetivo quieres introducir?")
        print("1. Cantidad de horas de deporte semanales")
        print("2. Cantidad de actividades realizadas en la semana")

        opcion = input("Selecciona una opción (1 o 2): ")

        if opcion not in ["1", "2"]:
            print("Opción no válida. Debe seleccionar 1 o 2.")
            return False

        if opcion == "1":
            objetivoHoras = float(input("Introduce la cantidad de horas de deporte semanales que deseas realizar: "))
            objetivoCantidad = None
        else:
            objetivoCantidad = int(input("Introduce la cantidad de actividades realizadas en la semana que deseas alcanzar: "))
            objetivoHoras = None

        # Verificar si ya existe un objetivo para la próxima semana
        fechaInicio = datetime.now()
        fechaFin = fechaInicio + timedelta(days=7)
        queryVerificar = "select count(*) as countObjetivos from ObjetivoSemanal where DeportistaID = ? and FechaInicio >= ? and FechaFin <= ?"
        resVerificar = self.db.executeQuery(queryVerificar, idDeportista, fechaInicio, fechaFin)

        # Manejar el caso cuando resVerificar es None
        if resVerificar is not None and resVerificar[0].get("countObjetivos", 0) > 0:
            # Ya existe un objetivo para la próxima semana
            print("Ya tienes un objetivo para la próxima semana. No se puede añadir otro.")
            return False

        # Calcular la fecha de inicio y fin del próximo periodo de siete días
        fechaInicio = datetime.now()
        fechaFin = fechaInicio + timedelta(days=7)

        # Insertar el objetivo semanal en la tabla ObjetivoSemanal
        queryInsert = "insert into ObjetivoSemanal(ID, FechaInicio, FechaFin, ObjetivoHoras, ObjetivoCantidad, DeportistaID) values (null,?,?,?,?,?)"
        self.db.executeUpdateQuery(queryInsert, fechaInicio, fechaFin, objetivoHoras, objetivoCantidad, idDeportista)

        print("Objetivo añadido con éxito.")
        return True


    
    # Nueva función para registrar a un deportista de forma gratuita
    def registrarDeportista(self, nombre, apellidos, correo, fecha_nacimiento, sexo, peso, altura):
        # Obtener la fecha actual como fecha de alta
        fecha_alta = datetime.now().date()

        # Definir los valores iniciales para Premium y Objetivos (pueden ser ajustados según tus requisitos)
        premium = False
        objetivo_horas = None
        objetivo_cantidad = None

        # Insertar el nuevo deportista en la tabla Deportista
        query_insert = """
            INSERT INTO Deportista(
                Nombre, Apellidos, CorreoElectronico, FechaAlta, Premium, Sexo,
                FechaNacimiento, Altura, Peso, ObjetivoHoras, ObjetivoCantidad
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.executeUpdateQuery(
            query_insert,
            nombre, apellidos, correo, fecha_alta, premium, sexo,
            fecha_nacimiento, altura, peso, objetivo_horas, objetivo_cantidad
        )

        # Obtener el ID del deportista recién registrado
        id_deportista = self.getIdDeportista(correo)

        # Mostrar justificante con los datos proporcionados y la fecha de alta
        print("Justificante de Registro:")
        print(f"Nombre: {nombre} {apellidos}")
        print(f"Correo Electrónico: {correo}")
        print(f"Fecha de Alta: {fecha_alta}")
        print("\nGuarde esta información para futuras referencias.")

        print("Registro exitoso. ¡Bienvenido a la aplicación!")

        # Devolver el ID del deportista recién registrado
        return id_deportista

<<<<<<< HEAD
    # función para ver la métrica del consumo calórico para una actividad
    def getConsumoCalorico(self,idDeportista,Actividad):
        # Calcular el MBR del deportista 
        queryMBR = """select Peso,Altura,FechaNacimiento,Sexo 
                      from Deportista where Deportista.ID = ?"""
        res = self.db.executeQuery(queryMBR,idDeportista)
        if len(res)==1:
            peso = res[0].get("Peso")
            altura = res[0].get("Altura")
            fechaNacimiento = res[0].get("FechaNacimiento")
            sexo = res[0].get("Sexo")
        else:
            return None
        
        # A partir de la fecha de nacimiento se calcula la edad
        fechaActual = datetime.now()
        edad = fechaActual.year - fechaNacimiento.year - ((fechaActual.month, fechaActual.day) < (fechaNacimiento.month, fechaNacimiento.day))

        # Calcular el MBR dependiendo del sexo
        if sexo == "Masculino":
            MBR = (10*peso)+(6.25*altura)-(5*edad)+5
        else:
            MBR = (10*peso)+(6.25*altura)-(5*edad)-161
        
        # Otener el MET de la actividad
        queryMET = """select MET from TipoActividad 
                      where TipoActividad.Tipo = ?"""
        res = self.db.executeQuery(queryMET,Actividad)
        if len(res)==1:
            MET = res[0].get("MET")
        else:
            return None
        
        # Calcular el consumo calórico
        consumoCalorico = (MBR/24/60)*MET

        return consumoCalorico
    
    # función para registrar un deportista premium
    def registrarDeportistaPremium(self, nombre, apellidos, correo, fecha_nacimiento, sexo, peso, altura,formapago,facturacion):
        # Obtener la fecha actual como fecha de alta
        fecha_alta = datetime.now().date()

        # Definir los valores iniciales para Premium y Objetivos (pueden ser ajustados según tus requisitos)
        premium = True
        objetivo_horas = None
        objetivo_cantidad = None

        # Insertar el nuevo deportista en la tabla Deportista las características básicas
        query_insert = """
            INSERT INTO Deportista(
                Nombre, Apellidos, CorreoElectronico, FechaAlta, Premium, Sexo,
                FechaNacimiento, Altura, Peso, ObjetivoHoras, ObjetivoCantidad
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.db.executeUpdateQuery(
            query_insert,
            nombre, apellidos, correo, fecha_alta, premium, sexo,
            fecha_nacimiento, altura, peso, objetivo_horas, objetivo_cantidad)
        
        # Obtener el ID del deportista recién registrado
        id_deportista = self.getIdDeportista(correo)
        
        # Insertamos la forma de pago y la facturación a la talba Premium
        query_premium = """
            INSERT INTO Premium(
                FormaPago, Facturacion, DeportistaID
            ) VALUES (?, ?, ?)
        """
        self.db.executeUpdateQuery(query_premium,formapago,facturacion,id_deportista)
        
=======
    
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
>>>>>>> 72be3e8bb152d7218298cd09c59666ccae18ceec
