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
    
    def insertActivity(self,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,consumo_calorico,tipo_actividad_id,subtipo_actividad_id,idDeportista):
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
                insert into Actividad(ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, ConsumoCalorico, TipoActividadID,SubtipoActividadID, DeportistaID) values (null,?,?,?,?,?,?,?,?,?,?) 
                """ 
        # Ejecutamos la query con los parámetros correspondientes
        self.db.executeUpdateQuery(query,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,consumo_calorico,tipo_actividad_id,subtipo_actividad_id,idDeportista)
        
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

        queryActividadesIntervalo = """SELECT
                                        A.Fecha,
                                        A.DuracionHoras,
                                        A.Localizacion,
                                        A.DistanciaKms,
                                        A.FCMax,
                                        A.FCMin,
                                        A.ConsumoCalorico,
                                        TA.Tipo,
                                        STA.Subtipo
                                        FROM Actividad A
                                        JOIN TipoActividad TA ON A.TipoActividadID = TA.ID
                                        JOIN SubtipoActividad STA ON A.SubtipoActividadID = STA.ID
                                        WHERE A.DeportistaID = ? AND A.Fecha BETWEEN ? AND ?"""
        resultActividades = self.db.executeQuery(queryActividadesIntervalo, idDeportista, fecha_inicio, fecha_fin)

        return resultActividades
    
    #Como deportista “Premium” obtener la actividad de otro deportista por tipo de actividad a lo largo del tiempo.
    def getActividadesDeportistaTipo(self, idDeportista, tipoActividadID):
       
        queryActividadesDeportista = "select Fecha, DuracionHoras, DistanciaKms from Actividad where DeportistaID = ? and TipoActividadID = ? order by Fecha desc"
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
                      where TipoActividad.ID= ?"""
        res = self.db.executeQuery(queryMET,Actividad_id)
        MET = res[0].get("MET")
            
        # pasar las horas a minutos
        min = horas*60
        # Calcular el consumo calórico
        consumoCalorico = (MBR/24/60)*MET*min

        # Insertamos ese valor en la tabla Actividad
        #query_cc = """update Actividad set ConsumoCalorico = ? 
        #              where Actividad.ID = ?"""
        #self.db.executeUpdateQuery(query_cc,consumoCalorico,Actividad_id)

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
            # Se agrupan por mes y el nombre del tipo de actividad
            query= """select strftime('%m',Fecha) as Mes, TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? group by Mes,TipoActividadID"""
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
            query= """select strftime('%m',Fecha) as Mes, SubtipoActividadID, TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? group by Mes, SubtipoActividadID"""
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
            query= """select strftime('%Y',Fecha) as Año,TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? group by Año,TipoActividadID"""
            informe = self.db.executeQuery(query,idDeportista)
            # Cambiamos el ID del tipo de actividad por el nombre del tipo de actividad
            for i in informe:
                query = "select Tipo from TipoActividad where TipoActividad.ID = ?"
                res = self.db.executeQuery(query,i.get("TipoActividadID"))
                i["TipoActividadID"] = res[0].get("Tipo")
            return informe
        
        elif tipoInforme == 2:
            # Para este informe se muestran las mismas características de antes pero ahora desglosadas por subtipo de actividad
            query= """select strftime('%Y',Fecha) as Año, SubtipoActividadID, TipoActividadID, sum(DuracionHoras) as DuracionTotal, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal, avg(FCMax) as FCMaxMedia, avg(FCMin) as FCMinMedia, sum(ConsumoCalorico) as ConsumoCaloricoTotal from Actividad where DeportistaID = ? group by Año, SubtipoActividadID"""
            informe = self.db.executeQuery(query,idDeportista)
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


