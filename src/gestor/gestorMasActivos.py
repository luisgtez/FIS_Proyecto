
import sqlite3

#Historia de usuario:
"""""
Como gestor me interesa mostrar a los deportistas más activos por tipo de actividad 
Criterio de aceptación: A partir del registro de actividades, se mostrará un listado
ordenado en orden decreciente por número de actividades realizadas por el deportista.
El listado contiene el nombre del usuario, fecha de alta y total de actividades
"""
# Conectar a la base de datos SQLite
conexion = sqlite3.connect('AppDB.db')  
cursor = conexion.cursor()

# Consulta SQL para obtener la lista de deportistas más activos
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

# Ejecutar la consulta
cursor.execute(consulta)

# Obtener los resultados
resultados = cursor.fetchall()

# Mostrar los resultados por consola
for fila in resultados:
    nombre_deportista, fecha_alta, total_actividades = fila
    print(f"Nombre: {nombre_deportista}, Fecha de Alta: {fecha_alta}, Total de Actividades: {total_actividades}")

# Cerrar la conexión a la base de datos
conexion.close()
