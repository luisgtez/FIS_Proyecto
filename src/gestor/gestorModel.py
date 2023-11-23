from util.database import DataBase

class GestorModel:
    '''
    Clase que representa los objetos de negocio (model) relativos a las funcionalidades de 
    los deportistas. Varios métodos de esta clase se invocarán desde la vista (DeportistaView), y los resultados
    se devolverán nuevamente a la vista para su visualización
    '''
    
    def __init__ (self):
        self.db = DataBase ("AppDB.db")
   
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
    def gestorEstadoForma(self, idDeportista):
        
        query=f"""
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
                WHERE Deportista.ID = {idDeportista}
                GROUP BY Deportista.ID;
            """
        res = self.db.executeQuery(query)
        estado_forma = res[0]["EstadoForma"]
        return estado_forma
    
    def getMasActivos(self):
        consulta = """
                    SELECT
                        D.Nombre || ' ' || D.Apellidos AS NombreDeportista,
                        D.FechaAlta,
                        COUNT(A.ID) AS TotalActividades
                    FROM
                        Deportista D
                    LEFT JOIN
                        Actividad A ON D.ID = A.DeportistaID
                    GROUP BY
                        D.ID, D.Nombre, D.Apellidos, D.FechaAlta
                    ORDER BY
                        TotalActividades DESC; 
                    """
        res = self.db.executeQuery(consulta)
        return res
    
    def existeID(self, idDeportista):
        '''
        Método que comprueba si existe un deportista con el ID especificado
        '''
        # Creamos una query para obtener el campo Premium de la tabla Deportista
        query="""
                select ID from Deportista 
                where Deportista.ID=?"""
        
        # Ejecutamos la query 
        res = self.db.executeQuery(query,idDeportista)
        
        # Si la query devuelve algún resultado, el ID existe
        if len(res) > 0:
            return True
        else:
            return False
        
        
    '''
    HU #23655
    '''
    def añadirTipo(self, tipo, MET):
        query = f"""
                INSERT INTO TipoActividad (ID, Tipo, MET) VALUES (null, ?, ?);
                """
        self.db.executeQuery(query, tipo, MET)
        
    def añadirSubtipo(self, subtipo, tipo):
        query = f"""
                INSERT INTO SubtipoActividad (ID, Subtipo, TipoActividadID) VALUES (null, ?, ?);
                """
        self.db.executeQuery(query, subtipo, tipo)
        