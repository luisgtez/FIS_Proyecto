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