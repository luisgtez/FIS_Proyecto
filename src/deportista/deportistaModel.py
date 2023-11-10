from util.database import DataBase

class DeportistaModel:
    '''
    Clase que representa los objetos de negocio (model) relativos a las funcionalidades de 
    los deportistas. Varios métodos de esta clase se invocarán desde la vista (DeportistaView), y los resultados
    se devolverán nuevamente a la vista para su visualización
    '''
    
    def __init__ (self):
        self.db = DataBase ("AppDB.db")
    
    # #Obtiene la lista de empleados para una compañia especificada por su nombre
    # def getAllEmployees (self,companyName):
    #     query = """select Company.name as Compania, Employee.id as IdEmpleado, Employee.name as NombreEmpleado, Employee.salary as Salario 
    #                from Company inner join Employee on Company.id=Employee.idCompany
    #                where Compania = ? order by Employee.id asc
    #             """
    #     return self.db.executeQuery(query,companyName)
    
    # #Obtiene resumen (total empleados y media de salario) para una compañia especificada por su nombre
    # def getSummaryEmployees (self, companyName): 
    #     query = """select count(Employee.id) as total, avg(Employee.salary) as average
    #                from Company inner join Employee on Company.id=Employee.idCompany
    #                where Company.name = ?
    #                group by (Company.id)
    #             """
    #     return  self.db.executeQuery(query,companyName)
    
    # #Obtiene el salario medio de todos los empleado por compañia
    # def getAvgSalary (self):
    #     query = """select Company.name, avg(Employee.salary) as avgSalary
    #               from Company left join Employee on Company.id=Employee.idCompany
    #               group by (Company.id)
    #             """
    #     return self.db.executeQuery(query)
    
    #Inserción de lo datos de un empleado (name,salary,birthdate) en una compañia
    #Notar que no es necesario indicar explícitamente el valor de la clave del empleado (id),
    # #ya que cuando éste es null, sqlite lo genera de forma autoincremental
    # def insertEmploye (self,name,salary,birthDate,idCompany):
    #     query = """
    #             insert into Employee(id,name,salary,birthDate,idCompany) values (null,?,?,?,?) 
    #             """
    #     self.db.executeUpdateQuery(query,name,salary,birthDate,idCompany)
    

    #Obtiene el id de un deportista especificado por su correo.
    def getIdDeportista(self,correoDeportista):
        query = """select id from Deportista where Deportista.CorreoElectronico = ?"""
        res = self.db.executeQuery(query,correoDeportista)
        if len(res)==1:
            return res[0].get("ID")
        else:
            return None
    
    #Obtiene el nombre y apellidos de un deportista especificado por su correo.
    def getNombreCompletoDeportista(self,correoDeportista):
        query = """select Nombre, Apellidos from Deportista
                   where Deportista.CorreoElectronico = ?
                """
        res = self.db.executeQuery(query,correoDeportista)
        if len(res)==1:
            return res[0].get("Nombre"),res[0].get("Apellidos")
        else:
            return None,None
    
    #Inserción de lo datos de una actividad (fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad,idCompany) de un deportista. ID se genera de forma autoincremental al ser null
    def insertActivity(self,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad,idDeportista):
        tipo_actividad = "Natacion" if tipo_actividad == "Natación" else tipo_actividad
        query = """
                insert into Actividad(ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, TipoActividad, DeportistaID) values (null,?,?,?,?,?,?,?,?) 
                """
        self.db.executeUpdateQuery(query,fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad,idDeportista)
        
    def getSummary(self,idDeportista):
        # query = """select TipoActividad, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal
        #            from Actividad
        #            where DeportistaID = ?
        #            group by TipoActividad
        #         """
        query = "select TipoActividad, count(*) as NumeroSesiones, sum(DistanciaKms) as DistanciaTotal from Actividad where DeportistaID = ? group by TipoActividad"
        return self.db.executeQuery(query,idDeportista)
    
    # Comprobar que el deportista es Premium
    def premium(self,idDeportista):
        query="""
                select Premium from Deportista 
                where Deportista.ID=?"""
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
