import sqlite3
#Historia de usuario:
"""""
Como gestor quiero conocer el estado y perfiles de los deportistas registrados por varios parámetros.
Se mostrarán los siguientes datos de los deportas registrados en la plataforma:
total deportistas activos, porcentaje perfil “Free” y “Premium”,
porcentaje por sexo y porcentaje por rango de edad (<30, 30-49,>50)
"""
# Conectar a la base de datos SQLite
conexion = sqlite3.connect('AppDB.db')  
cursor = conexion.cursor()

# Consulta para obtener el total de deportistas activos
consulta_total_activos = "SELECT COUNT(*) FROM Deportista;"
cursor.execute(consulta_total_activos)
total_activos = cursor.fetchone()[0]

# Consulta para obtener el porcentaje de perfiles "Free" y "Premium"
consulta_perfil = """
SELECT
    SUM(CASE WHEN Premium = 1 THEN 1 ELSE 0 END) AS TotalPremium,
    SUM(CASE WHEN Premium = 0 THEN 1 ELSE 0 END) AS TotalFree
FROM Deportista;
"""
cursor.execute(consulta_perfil)
resultados_perfil = cursor.fetchone()
total_premium = resultados_perfil[0]
total_free = resultados_perfil[1]

# Consulta para obtener el porcentaje por sexo
consulta_por_sexo = """
SELECT
    Sexo,
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Deportista)) AS Porcentaje
FROM Deportista
GROUP BY Sexo;
"""
cursor.execute(consulta_por_sexo)
resultados_sexo = cursor.fetchall()

# Consulta para obtener el porcentaje por rango de edad
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
cursor.execute(consulta_por_edad)
resultados_edad = cursor.fetchall()

# Cerrar la conexión a la base de datos
conexion.close()

# Imprimir los resultados
print("Total de deportistas activos:", total_activos)
print("Porcentaje de perfiles Premium:", total_premium / (total_premium + total_free) * 100, "%")
print("Porcentaje de perfiles Free:", total_free / (total_premium + total_free) * 100, "%")
print("Porcentaje por sexo:")
for resultado_sexo in resultados_sexo:
    print(f"{resultado_sexo[0]}: {resultado_sexo[1]:.2f}%")
print("Porcentaje por rango de edad:")
for resultado_edad in resultados_edad:
    print(f"{resultado_edad[0]}: {resultado_edad[1]:.2f}%")
