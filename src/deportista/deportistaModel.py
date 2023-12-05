from util.database import DataBase
from datetime import  timedelta,datetime
import datetime as dt
from util.Utils import utils

class DeportistaModel:
    '''
    Clase que representa los objetos de negocio (model) relativos a las funcionalidades de 
    los deportistas. Varios métodos de esta clase se invocarán desde la vista (DeportistaView), y los resultados
    se devolverán nuevamente a la vista para su visualización
    '''
    
    def __init__ (self):
        self.db = DataBase ("AppDB.db") # Crea un objeto DataBase con la ruta de la base de datos
        self.utils = utils() # Crea un objeto Utils para utilizar sus métodos

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
    
    def insertActivity(self,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,consumo_calorico,tipo_actividad_id,subtipo_actividad_id,idDeportista, publica = False):
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
        ConsumoCalorico : float
            Consumo calórico de la actividad.
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
                insert into Actividad(ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, ConsumoCalorico, TipoActividadID,SubtipoActividadID, DeportistaID, Publico) values (null,?,?,?,?,?,?,?,?,?,?,?) 
                """ 
        # Ejecutamos la query con los parámetros correspondientes
        self.db.executeUpdateQuery(query,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,consumo_calorico,tipo_actividad_id,subtipo_actividad_id,idDeportista, publica)
        
        # Devolvemos "OK"
        return "OK"
            
    def getSummary_propio(self,idDeportista):
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
    
    def getSummary_otro(self,idDeportista):
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
        # query = select TipoActividadID, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal
        # from Actividad 
        # where Publico=True and where DeportistaID = ?
        # group by TipoActividadID

        query = """select TipoActividadID, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal
                     from Actividad
                        where Publico=True and DeportistaID = ?
                        group by TipoActividadID
                """


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

        queryActividadesIntervalo = """SELECT
                                        A.Fecha,
                                        A.DuracionHoras,
                                        A.Localizacion,
                                        A.DistanciaKms,
                                        A.FCMax,
                                        A.FCMin,
                                        A.ConsumoCalorico,
                                        TA.Tipo,
                                        STA.Subtipo,
                                        A.Publico
                                        FROM Actividad A
                                        JOIN TipoActividad TA ON A.TipoActividadID = TA.ID
                                        JOIN SubtipoActividad STA ON A.SubtipoActividadID = STA.ID
                                        WHERE A.DeportistaID = ? AND A.Fecha BETWEEN ? AND ?"""
        resultActividades = self.db.executeQuery(queryActividadesIntervalo, idDeportista, fecha_inicio, fecha_fin)

        return resultActividades
    
    #Como deportista “Premium” obtener la actividad de otro deportista por tipo de actividad a lo largo del tiempo.
    def getActividadesDeportistaTipo(self, idDeportista, tipoActividadID):
       
        queryActividadesDeportista = "select Fecha, DuracionHoras, DistanciaKms from Actividad where DeportistaID = ? and TipoActividadID = ? and Publico=True order by Fecha desc"
        resultActividades = self.db.executeQuery(queryActividadesDeportista, idDeportista, tipoActividadID)
        
        return resultActividades


    def comprobarExisteObjetivo(self,idDeportista,tipoObjetivo):
        
        # Verificar si ya existe un objetivo para la próxima semana
        queryVerificar = f"select {tipoObjetivo} from Deportista where Deportista.ID = ?"
        resVerificar = self.db.executeQuery(queryVerificar, idDeportista)

        value = resVerificar[0][tipoObjetivo]
        return value
        
    #Como deportista quiero añadir objetivos semanales
    def addObjetivoSemanal(self, idDeportista, tipoObjetivo, valorObjetivo):

        # Creamos la consulta
        query = f"UPDATE Deportista SET {tipoObjetivo} = {valorObjetivo} WHERE Deportista.ID = {idDeportista}"
        self.db.executeUpdateQuery(query)

    
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
    
        
    # función para registrar un deportista premium
    def registrarDeportista(self, nombre, apellidos, correo, fecha_nacimiento, sexo, peso, altura,formapago,facturacion,premium):
        # Obtener la fecha actual como fecha de alta
        fecha_alta = datetime.now().date()

        # Definir los valores iniciales para Premium y Objetivos (pueden ser ajustados según tus requisitos)
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
        
        if premium==True:
            # Obtener el ID del deportista recién registrado
            id_deportista = self.getIdDeportista(correo)
            
            # Insertamos la forma de pago y la facturación a la talba Premium
            query_premium = """
                INSERT INTO Premium(
                    FormaPago, Facturacion, DeportistaID
                ) VALUES (?, ?, ?)
            """
            self.db.executeUpdateQuery(query_premium,formapago,facturacion,id_deportista)

    # función para ver la métrica del consumo calórico para una actividad
    def getConsumoCalorico(self,idDeportista,Actividad_id,horas):
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
        fechaNacimiento = datetime.strptime(fechaNacimiento, '%Y-%m-%d')
        edad = fechaActual.year - fechaNacimiento.year - ((fechaActual.month, fechaActual.day) < (fechaNacimiento.month, fechaNacimiento.day))

        # Calcular el MBR dependiendo del sexo
        if sexo == "Masculino":
            MBR = (10*peso)+(6.25*altura)-(5*edad)+5
        else:
            MBR = (10*peso)+(6.25*altura)-(5*edad)-161
        
        # Otener el MET  y el ID de la actividad
        queryMET = """select MET from TipoActividad 
                      where TipoActividad.ID = ?"""
        res = self.db.executeQuery(queryMET,Actividad_id)
        
        MET = res[0].get("MET")
                   
        # pasar las horas a minutos
        min = horas*60
        # Calcular el consumo calórico
        consumoCalorico = (MBR/24/60)*MET*min

        return consumoCalorico

   
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

    def getActividadesProgramadasPublicas(self):
        '''Método que obtiene las actividades programadas publicas
        
        Devuelve
        -------
        list
            Lista de diccionarios con las actividades programadas publicas.
        '''
        
        # Creamos una query para obtener las actividades programadas que cumplan numplazas > numinscripciones y fecha > fecha actual
        query = """SELECT ActividadEntidad.ID as "Nº Actividad",NombreActividad as "Nombre", Descripcion, Fecha, DuracionDias AS "Duracion Dias", NumPlazas as "Numero de Plazas", Coste FROM ActividadEntidad 
            LEFT JOIN Inscripcion ON ActividadEntidad.ID = Inscripcion.ActividadEntidadID
                GROUP BY ActividadEntidadID 
                HAVING COUNT(Inscripcion.ActividadEntidadID) < ActividadEntidad.NumPlazas
                AND ActividadEntidad.Fecha > DATE();
        """

        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query)
        
        
        # Retornamos el resultado
        return result
    
    def InscribirEnActividad(self, IDDeportista, IDActividad):
        '''Método que inscribe a un deportista en una actividad
        
        Parámetros
        ----------
        IDDeportista : int
            ID del deportista que se quiere inscribir en la actividad.
        IDActividad : int
            ID de la actividad en la que se quiere inscribir el deportista.
            
        Devuelve
        -------
        str
            "OK" si la inscripción se ha realizado correctamente.
        '''
        
        # Creamos una query para inscribir al deportista en la actividad
        query = "INSERT INTO Inscripcion (ID,DeportistaID, ActividadEntidadID) VALUES (null,?,?)"
        
        try:
            # Ejecutamos la query y guardamos el resultado en result
            self.db.executeUpdateQuery(query,IDDeportista,IDActividad)
            
            # Retornamos "OK"
            return "OK"
        except:
            # Retornamos "ERROR"
            return "ERROR"
        
    def getDatosActividad(self,IDActividad):
        '''Método que obtiene los datos de una actividad
        
        Parámetros
        ----------
        IDActividad : int
            ID de la actividad de la que se quieren obtener los datos.
            
        Devuelve
        -------
        dict
            Diccionario con los datos de la actividad.
        '''
        
        # Creamos una query para obtener los datos de la actividad
        query = """SELECT * FROM ActividadEntidad 
                    WHERE ActividadEntidad.ID = ?
        """
        
        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query,IDActividad)
        
        # Retornamos el resultado
        return result
    
    def EstaInscritoEnActividad(self,IDDeportista,IDActividad):
        '''Método que comprueba si un deportista está inscrito en una actividad
        
        Parámetros
        ----------
        IDDeportista : int
            ID del deportista que se quiere comprobar si está inscrito en la actividad.
        IDActividad : int
            ID de la actividad en la que se quiere comprobar si el deportista está inscrito.
            
        Devuelve
        -------
        bool
            True si el deportista está inscrito en la actividad, False en caso contrario.
        '''
        
        # Creamos una query para comprobar si el deportista está inscrito en la actividad
        query = """SELECT * FROM Inscripcion 
                    WHERE DeportistaID = ? AND ActividadEntidadID = ?
        """
        
        # Ejecutamos la query y guardamos el resultado en result
        result = self.db.executeQuery(query,IDDeportista,IDActividad)
        
        # Retornamos True si el resultado tiene al menos un elemento, False en caso contrario
        return len(result)>0
    def actividadesPorSemana(self, idDeportista):
        '''Método que obtiene el número de actividades realizadas por semana.
        
        Parámetros
        ----------
        idDeportista : int
            ID del deportista del que se quiere obtener el número de actividades por semana.
            
        Devuelve
        -------
        str
            Cadena que indica el número de actividades realizadas por semana.
        '''
        # Obtener la fecha actual
        fecha_actual = datetime.now().date()

        # Calcular la fecha de inicio de la semana actual (lunes)
        inicio_semana = fecha_actual - timedelta(days=fecha_actual.weekday())

        # Creamos una query para contar las actividades realizadas desde el inicio de la semana
        query = "select count(*) as NumeroActividades from Actividad where DeportistaID = ? and Fecha >= ?"

        # Ejecutamos la query con los parámetros correspondientes
        resultado = self.db.executeQuery(query, idDeportista, inicio_semana)

        # Devolvemos la cadena con el número de actividades realizadas por semana
        return f"Esta semana has realizado {resultado[0]['NumeroActividades']} actividades."

    def compararConGrupoEdad(self, idDeportista):
        '''Método que compara al deportista premium con otros deportistas de su franja de edad.'''
        # Obtener sexo y fecha de nacimiento del deportista premium
        sexo, fecha_nacimiento = self.getSexoFecha(idDeportista)

        # Obtener el rango de edad para la comparación
        rango_edad = self.obtenerRangoEdad(self.calcularEdad(fecha_nacimiento))

        # Obtener deportistas en el mismo rango de edad y sexo
        deportistas_grupo = self.getDeportistasPorRangoEdad(rango_edad, sexo)

        # Verificar si hay suficientes deportistas en el grupo de edad
        if not deportistas_grupo:
            return None

        # Obtener el resumen de actividades y calorías para la franja de edad
        query = "SELECT COUNT(*) AS NumeroSesiones, AVG(ConsumoCalorico) AS ConsumoCaloricoPromedio FROM Actividad WHERE DeportistaID IN ({})".format(','.join(map(str, deportistas_grupo)))
        resumen_grupo = self.db.executeQuery(query)

        if not resumen_grupo or 'NumeroSesiones' not in resumen_grupo[0]:
            return None

        # Obtener el resumen de actividades y calorías para el deportista premium
        query_deportista_premium = "SELECT COUNT(*) AS TotalActividades, AVG(ConsumoCalorico) AS ConsumoCaloricoPromedio FROM Actividad WHERE DeportistaID = ?"
        resumen_deportista_premium = self.db.executeQuery(query_deportista_premium, idDeportista)

        if not resumen_deportista_premium:
            return None

        # Retornar los resultados
        resultados = {
            "Edad": self.calcularEdad(fecha_nacimiento),
            "TotalActividades": resumen_deportista_premium[0].get('TotalActividades', 0),
            "ConsumoCaloricoPromedio": resumen_deportista_premium[0].get('ConsumoCaloricoPromedio', 0),
            "NumeroSesionesPromedio": resumen_grupo[0].get('NumeroSesiones', 0),
            "ConsumoCaloricoPromedioGrupo": resumen_grupo[0].get('ConsumoCaloricoPromedio', 0)
        }

        return resultados

    def getInscripcionesDeportista(self, deportista_id, premium):
        if premium:
            query="""SELECT
                    AE.NombreActividad,
                    AE.Fecha,
                    AE.DuracionDias,
                    E.NombreEntidad
                    FROM Inscripcion I
                    JOIN ActividadEntidad AE ON I.ActividadEntidadID = AE.ID
                    JOIN Entidad E ON AE.EntidadID = E.ID
                    WHERE I.DeportistaID = ? 
                    ORDER BY AE.Fecha DESC;"""
        else:
            query="""SELECT
                    AE.NombreActividad,
                    AE.Fecha,
                    AE.DuracionDias,
                    AE.Coste,
                    E.NombreEntidad
                    FROM Inscripcion I
                    JOIN ActividadEntidad AE ON I.ActividadEntidadID = AE.ID
                    JOIN Entidad E ON AE.EntidadID = E.ID
                    WHERE I.DeportistaID = ? 
                    ORDER BY AE.Fecha DESC;"""
            
        return self.db.executeQuery(query,deportista_id)

    def seguirDeportista(self,idDeportista,idDeportistaSeguido):
        '''Método que permite a un deportista seguir a otro
        
        Parámetros
        ----------
        idDeportista : int
            ID del deportista que quiere seguir a otro.
        idDeportistaSeguido : int
            ID del deportista que va a ser seguido.
            
        Devuelve
        -------
        str
            "OK" si la inserción se ha realizado correctamente.
        '''
        
        # Creamos una query para insertar los datos en la tabla Seguir
        query = """ 
                insert into SeguirDeportista(ID, DeportistaID, SeguidorID) values (null,?,?) 
                """ 
        # Ejecutamos la query con los parámetros correspondientes
        self.db.executeUpdateQuery(query,idDeportista,idDeportistaSeguido)

        return "OK"

    def getDeportistasComparar(self,idDeportista):
        '''Método que obtiene los deportistas que sigue un deportista
        
        Parámetros
        ----------
        idDeportista : int
            ID del deportista del que se quiere obtener los deportistas que sigue.
            
        Devuelve
        -------
        list
            Lista de diccionarios con los deportistas que sigue un deportista.
        '''
        
        # Creamos una query para obtener los deportistas que sigue un deportista
        query = "select SeguidorID from SeguirDeportista where DeportistaID = ?"
        
        # Ejecutamos la query 
        id = self.db.executeQuery(query,idDeportista)

        # Obtenemos el correo asociado a cada ID
        query = "select CorreoElectronico from Deportista where Deportista.ID = ?"
        deportistas = []
        for i in id:
            res = self.db.executeQuery(query,i.get("SeguidorID"))
            deportistas.append(res[0].get("CorreoElectronico"))
        
        # Retornamos la lista de deportistas
        return deportistas
    
    def getInformeMensual(self,idDeportista,tipoInforme):
        '''Método que obtiene el informe mensual de un deportista
        
        Parámetros
        ----------
        idDeportista : int
            ID del deportista del que se quiere obtener el informe mensual.
        tipoInforme : int
            1- Indica el informe mensual por total de actividades
            2- Indica el informe mensual por tipo de actividad
            
        Devuelve
        -------
        list
            Lista de diccionarios con el informe mensual de un deportista.
        '''
        if tipoInforme == 1:
            # Para este informe se muestra el total de horas de actividad,todas las localizaciones,total de distancia,media FC max y FC min y total consumo calorico
            # Se muestra el informe del mes actual
            query = """select strftime('%m',Fecha) as Mes, TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? and strftime('%m',Fecha) = strftime('%m','now') group by Mes,TipoActividadID"""

            informe = self.db.executeQuery(query,idDeportista)
            # Cambiamos el ID del tipo de actividad por el nombre del tipo de actividad
            for i in informe:
                query = "select Tipo from TipoActividad where TipoActividad.ID = ?"
                res = self.db.executeQuery(query,i.get("TipoActividadID"))
                i["TipoActividadID"] = res[0].get("Tipo")
            return informe
        
        elif tipoInforme == 2:
            # Para este informe se muestran las mismas características de antes pero ahora desglosadas por subtipo de actividad
            # Se agrupan por mes y subtipo de actividad, se indica a su vez el nombre  tipo de actividad
            query = """select strftime('%m',Fecha) as Mes, SubtipoActividadID, TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? and strftime('%m',Fecha) = strftime('%m','now') group by Mes,SubtipoActividadID"""
            informe = self.db.executeQuery(query,idDeportista)
            # Cambiamos el ID del tipo de actividad por el nombre del tipo de actividad y el ID del subtipo de actividad por el nombre del subtipo de actividad
            for i in informe:
                # Seleccionamos el nombre del tipo de actividad asociado al ID del tipo de actividad
                query = "select Tipo from TipoActividad where TipoActividad.ID = ?"
                res = self.db.executeQuery(query,i.get("TipoActividadID"))
                i["TipoActividadID"] = res[0].get("Tipo")
                # Seleccionamos el nombre del subtipo de actividad asociado al ID del subtipo de actividad
                query = "select Subtipo from SubtipoActividad where SubtipoActividad.ID = ?"
                res = self.db.executeQuery(query,i.get("SubtipoActividadID"))
                i["SubtipoActividadID"] = res[0].get("Subtipo")
            return informe
        else:
            return None
    
    def getInformeAnual(self,idDeportista,tipoInforme):
        '''Método que obtiene el informe anual de un deportista
        
        Parámetros
        ----------
        idDeportista : int
            ID del deportista del que se quiere obtener el informe anual.
        tipoInforme : int
            1- Indica el informe anual por total de actividades
            2- Indica el informe anual por tipo de actividad
            
        Devuelve
        -------
        list
            Lista de diccionarios con el informe anual de un deportista.
        '''
        if tipoInforme == 1:
            # Para este informe se muestra el total de horas de actividad,todas las localizaciones,total de distancia,media FC max y FC min y total consumo calorico
            # Mostramos el informe del año actual
            query = """select strftime('%Y',Fecha) as Año, TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? and strftime('%Y',Fecha) = strftime('%Y','now') group by Año,TipoActividadID"""

            informe = self.db.executeQuery(query,idDeportista)
            # Cambiamos el ID del tipo de actividad por el nombre del tipo de actividad
            for i in informe:
                query = "select Tipo from TipoActividad where TipoActividad.ID = ?"
                res = self.db.executeQuery(query,i.get("TipoActividadID"))
                i["TipoActividadID"] = res[0].get("Tipo")
            return informe
        
        elif tipoInforme == 2:
            # Para este informe se muestran las mismas características de antes pero ahora desglosadas por subtipo de actividad
            query = """select strftime('%Y',Fecha) as Año, SubtipoActividadID, TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? and strftime('%Y',Fecha) = strftime('%Y','now') group by Año,SubtipoActividadID"""

            informe = self.db.executeQuery(query,idDeportista)
            # Cambiamos el ID del tipo de actividad por el nombre del tipo de actividad y el ID del subtipo de actividad por el nombre del subtipo de actividad
            for i in informe:
                # Seleccionamos el nombre del tipo de actividad asociado al ID del tipo de actividad
                query = "select Tipo from TipoActividad where TipoActividad.ID = ?"
                res = self.db.executeQuery(query,i.get("TipoActividadID"))
                i["TipoActividadID"] = res[0].get("Tipo")
                # Seleccionamos el nombre del subtipo de actividad asociado al ID del subtipo de actividad
                query = "select Subtipo from SubtipoActividad where SubtipoActividad.ID = ?"
                res = self.db.executeQuery(query,i.get("SubtipoActividadID"))
                i["SubtipoActividadID"] = res[0].get("Subtipo")
            return informe
        else:
            return None
        
   
    def getObjetivos(self, idDeportista):
        query = """
            SELECT ObjetivoHoras, ObjetivoCantidad
            FROM Deportista
            WHERE ID = ?
        """
        result = self.db.executeQuery(query, idDeportista)
        
        if result:
            return [{"ObjetivoHoras": result[0]["ObjetivoHoras"], "ObjetivoCantidad": result[0]["ObjetivoCantidad"]}]
        else:
            return []

    def calcularProgresoObjetivo(self, idDeportista, tipo_objetivo):
        if tipo_objetivo == "ObjetivoHoras":
            query = """
                SELECT COALESCE(SUM(DuracionHoras), 0) as TotalHoras
                FROM Actividad
                WHERE DeportistaID = ?
            """
            total_horas = self.db.executeQuery(query, idDeportista)[0]["TotalHoras"]

            objetivos = self.getObjetivos(idDeportista)
            objetivo_horas = objetivos[0]["ObjetivoHoras"] if objetivos else None

            if objetivo_horas is None:
                print(f"Error: No se encontró el objetivo de horas para el deportista con ID {idDeportista}")
                return {"error": True, "message": "Objetivo de horas no encontrado."}

            progreso_horas = total_horas / objetivo_horas if objetivo_horas > 0 else 0
            return progreso_horas

        elif tipo_objetivo == "ObjetivoCantidad":
            query = """
                SELECT COALESCE(COUNT(*), 0) as TotalActividades
                FROM Inscripcion
                WHERE DeportistaID = ?
            """
            total_actividades = self.db.executeQuery(query, idDeportista)[0]["TotalActividades"]

            objetivos = self.getObjetivos(idDeportista)
            objetivo_cantidad = objetivos[0]["ObjetivoCantidad"] if objetivos else None

            if objetivo_cantidad is None:
                print(f"Error: No se encontró el objetivo de cantidad para el deportista con ID {idDeportista}")
                return {"error": True, "message": "Objetivo de cantidad no encontrado."}

            progreso_cantidad = total_actividades / objetivo_cantidad if objetivo_cantidad > 0 else 0
            return progreso_cantidad

        else:
            print(f"Error: Tipo de objetivo no válido: {tipo_objetivo}")
            return {"error": True, "message": "Tipo de objetivo no válido."}
        
    def calcularEdad(self, fecha_nacimiento):
        '''Método que calcula la edad a partir de la fecha de nacimiento.
        
        Parámetros
        ----------
        fecha_nacimiento : str
            Fecha de nacimiento en formato 'YYYY-MM-DD'.
        
        Devuelve
        -------
        int
            Edad del deportista.
        '''
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        fecha_actual = datetime.now()
        edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        return edad

    def obtenerRangoEdad(self, edad):
        '''Método que obtiene el rango de edad para la comparación.
        
        Parámetros
        ----------
        edad : int
            Edad del deportista.
        
        Devuelve
        -------
        str
            Rango de edad ('<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+').
        '''
        if edad < 18:
            return '<18'
        elif 18 <= edad <= 24:
            return '18-24'
        elif 25 <= edad <= 34:
            return '25-34'
        elif 35 <= edad <= 44:
            return '35-44'
        elif 45 <= edad <= 54:
            return '45-54'
        elif 55 <= edad <= 64:
            return '55-64'
        else:
            return '65+'

    def getDeportistasPorRangoEdad(self, rango_edad, sexo):
        '''Obtiene deportistas en el mismo rango de edad y sexo.'''
        query = "SELECT ID, FechaNacimiento FROM Deportista WHERE Sexo = ?"
        deportistas = self.db.executeQuery(query, sexo)

        deportistas_grupo = []
        for deportista in deportistas:
            edad = self.calcularEdad(deportista['FechaNacimiento'])
            if self.obtenerRangoEdad(edad) == rango_edad:
                deportistas_grupo.append(deportista['ID'])

        return deportistas_grupo  
    
    ############################################
    def getNumeroActividadesSieteDias(self, id_deportista):
        # Obtener la fecha actual
        fecha_actual = self.getFechaActual()

        # Calcular la fecha hace siete días
        fecha_hace_siete_dias = fecha_actual - dt.timedelta(days=7)

        # Crear la query para contar el número de actividades en el periodo de siete días
        query = """SELECT COUNT(*) as NumActividades 
                   FROM Actividad 
                   WHERE Actividad.DeportistaID = ? 
                         AND Actividad.Fecha BETWEEN ? AND ?"""
        
        # Ejecutar la query y obtener el resultado
        res = self.db.executeQuery(query, id_deportista, fecha_hace_siete_dias, fecha_actual)

        # Obtener el número de actividades desde el resultado
        num_actividades = res[0].get("NumActividades")

        return num_actividades

    def mostrarProgreso(self, id_deportista):
        num_actividades = self.getNumeroActividadesSieteDias(id_deportista)
        mensaje = f"En los últimos siete días has realizado {num_actividades} actividades."
        return mensaje
    
    def getFechaActual(self):
        return dt.date.today()
