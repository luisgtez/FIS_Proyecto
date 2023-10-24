from util.database import DataBase

class GestorModel:
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
   
    def gestorEstado(self):
        
        results = {}
        
        consulta_total_activos = "SELECT COUNT(*) FROM Deportista as TotalActivos;"
        results["total_activos"] = self.db.executeQuery(consulta_total_activos)[0]["COUNT(*)"]

        consulta_perfil = """
                        SELECT
                            SUM(CASE WHEN Premium = 1 THEN 1 ELSE 0 END) AS TotalPremium,
                            SUM(CASE WHEN Premium = 0 THEN 1 ELSE 0 END) AS TotalFree
                        FROM Deportista;
                        """     
        resultados_perfil = self.db.executeQuery(consulta_perfil)[0]
        results["total_premium"] = resultados_perfil["TotalPremium"]
        results["total_free"] = resultados_perfil["TotalFree"]
        
        consulta_por_sexo = """
        SELECT
            Sexo,
            (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Deportista)) AS Porcentaje
        FROM Deportista
        GROUP BY Sexo;
        """
        
        results["resultados_sexo"] = self.db.executeQuery(consulta_por_sexo)
        
        consulta_por_edad = """
        SELECT
            CASE
                WHEN strftime('%Y', 'now') - strftime('%Y', FechaNacimiento) < 30 THEN '<30'
                WHEN strftime('%Y', 'now') - strftime('%Y', FechaNacimiento) BETWEEN 30 AND 49 THEN '30-49'
                ELSE '>50'
            END AS RangoEdad,
            (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Deportista)) AS Porcentaje
        FROM Deportista
        GROUP BY RangoEdad;
        """
        
        
        results["resultados_edad"] = self.db.executeQuery(consulta_por_edad)

        return results
    
    # Obtiene el estado de forma de los deportistas
    def gestorEstadoForma(self):
        
        query="""
                SELECT Deportista.ID,
                CASE
                    WHEN AVG(CASE WHEN strftime('%Y-%m-%d', 'now', '-1 month') <= Actividad.Fecha THEN 1 ELSE 0 END) /
                        AVG(CASE WHEN Deportista.ID = Actividad.DeportistaID THEN 1 ELSE 0 END) < 1 THEN 'Decreciente'
                    WHEN AVG(CASE WHEN strftime('%Y-%m-%d', 'now', '-1 month') <= Actividad.Fecha THEN 1 ELSE 0 END) /
                        AVG(CASE WHEN Deportista.ID = Actividad.DeportistaID THEN 1 ELSE 0 END) = 1 THEN 'Buena'
                    ELSE 'Muy Buena'
                END AS EstadoForma
                FROM Deportista
                LEFT JOIN Actividad ON Deportista.ID = Actividad.DeportistaID
                GROUP BY Deportista.ID;
            """
        res = self.db.executeQuery(query)
        return res