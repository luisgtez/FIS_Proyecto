import sqlite3

# conectar a la base de datos
conn = sqlite3.connect('AppDB.db')
cursor=conn.cursor()

# consulta para obtener el estado de forma por cada deportista
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

# ejecutamos la consulta y guardamos los resultados
cursor.execute(query)
results = cursor.fetchall()

# mostramos los resultados
for deportista in results:
    id, estadoforma = deportista
    print(f"ID: {id}")
    print(f"Estado de forma: {estadoforma}")

# cerramos conexión
cursor.close()
conn.close()

