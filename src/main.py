
from util.database import DataBase
from deportista.deportistaView import DeportistaView

'''
    Inicialización de la aplicación: 
    Crea el esquema de la BBDD, realiza una carga inicial de datos en la BD y muestra un menú
'''
DBNAME = "AppDB.db"
SCHEMA = "resources/schema.sql"
DATA = "resources/data.sql"

# Conexión a la base de datos DBNAME, si no existe la crea
db = DataBase(DBNAME)
db.executeScript(SCHEMA)  # Genera el esquema ejecutando el script SCHEMA
db.executeScript(DATA)  # Carga incial de datos especificada en el script DATA

DeportistaView().run()  # Muestra el menú de opciones
