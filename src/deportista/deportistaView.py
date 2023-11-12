from deportista.deportistaModel import DeportistaModel
from gestor.gestorView import GestorView
from util.Utils import utils

import datetime
import os
import pandas as pd
import shutil



class DeportistaView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los deportistas que estarán
    representadas en la clase DeportistaModel (DeportistaModel.py)
    '''
     
    def __init__ (self):
        self.deportista = DeportistaModel() #Crea un objeto model que se invocará desde esta vista
        self.gestor_view = GestorView() #Crea un objeto model que se invocará desde esta vista
        
    #Vista para la HU Registrar una nueva actividad
    def addActivity(self):
        '''Método que permite insertar una nueva actividad en la base de datos.
        
        El deportista se identifica mediante su correo electrónico y se mostrarán sus datos. A continuación, se solicitarán los datos de la actividad a insertar, se comprobará que son correctos y se insertará la actividad en la base de datos.
        '''
        # Inicio de sesion
        
        # Llama a la vista de inicio de sesion, si devuelve None es que no se ha iniciado sesion correctamente
        idDeportista = self.inicio_sesion_view()
        if idDeportista==None:
            return
        
        # Introdcir los datos de la actividad
        print("\nIntrodcir los datos de la actividad")
        try:
        # Fecha
        
            # Pedimos la fecha
            fecha = input ("Fecha (AAAA-MM-DD), dejar vacío si quieres que la fecha sea igual a la actual: ")
            # Si no se ha introducido nada, la fecha es la actual
            if fecha=="":
                fecha = datetime.datetime.now().strftime("%Y-%m-%d")
            # Si se ha introducido algo, comprobamos que tiene el formato correcto
            else:
                # Convertimos la fecha a datetime para comprobar que tiene el formato correcto
                try:
                    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').strftime("%Y-%m-%d")
                    
                # Si hay un error, mostramos un mensaje de error y salimos de la funcion
                except ValueError:
                    print ("Error en el formato de la fecha, debe tener el formato AAAA-MM-DD")
                    return
                
                # Si no hay error y se convierte correctamente, comprobamos que la fecha no es mayor que la actual
                if fecha>datetime.datetime.now().strftime("%Y-%m-%d"):
                    # En tal caso, mostramos un mensaje de error y salimos de la funcion
                    print("Error en el formato de la fecha, no puede ser mayor que la actual")
                    return
                
        # Duracion en horas
        
            # Pedimos la duracion en horas
            duracion_horas = input ("Duracion en horas: ")

            # Intentamos convertir la duracion a float y cambiar la coma por punto
            try:
                duracion_horas.replace(",",".")
                duracion_horas = float(duracion_horas)
            
            # Si da error, mostramos un mensaje de error y salimos de la funcion
            except ValueError:
                print ("Error en el formato de la duracion, debe ser un numero entero o decimal")
                return
            
            # Si no hay error, comprobamos que la duracion es positiva
            if duracion_horas < 0:
                # En tal caso, mostramos un mensaje de error y salimos de la funcion
                print ("Error en el formato de la duracion, debe ser un numero entero o decimal positivo")
                return
            
        # Localizacion
            
            # Pedimos la localizacion, en este caso puede ser cualquier cosa
            localizacion = input ("Localizacion: ")
            
        # Distancia en kms
            
            # Pedimos la distancia en kms
            distancia_kms = input ("Distancia en kms: ")
            
            # Intentamos convertir la distancia a float y cambiar la coma por punto
            try:
                distancia_kms = float(distancia_kms)
                
            # Si da error, mostramos un mensaje de error y salimos de la funcion
            except ValueError:
                print ("Error en el formato de la distancia, debe ser un numero entero o decimal")
                return
            
            # Si no hay error, comprobamos que la distancia es positiva
            if distancia_kms < 0:
                print ("Error en el formato de la distancia, debe ser un numero entero o decimal positivo")
                return

        # FC max y min
            
            # Pedimos la FC max
            FC_max = input ("FC max (opcional): ")
            
            # Si no se ha introducido nada, la FC max es None
            if FC_max=="":
                FC_max = None
            
            # Si se ha introducido algo, comprobamos que tiene el formato correcto
            else:
                # Intentamos convertir la FC max a int
                try :
                    FC_max = int(FC_max)
                
                # Si da error, mostramos un mensaje de error y salimos de la funcion
                except ValueError:
                    print ("Error en el formato de la FC max, debe ser un numero entero")
                    return
                
                # Si no hay error, comprobamos que la FC max es negativa
                if FC_max < 0:
                    # Si es negativa, mostramos un mensaje de error y salimos de la funcion
                    print ("Error en el formato de la FC max, debe ser un numero entero positivo")
                    return
            
            # Pedimos la FC min y seguimos el mismo proceso que con la FC max
            FC_min = input ("FC min (opcional): ")
            if FC_min=="":
                FC_min = None
            else:
                try :
                    FC_min = int(FC_min)
                except ValueError:
                    print ("Error en el formato de la FC min, debe ser un numero entero")
                    return
                if FC_min < 0:
                    print ("Error en el formato de la FC min, debe ser un numero entero positivo")
                    return
            
            
        # Tipo de actividad
            
            # Llamamos al metodo para escoger el tipo de actividad
            tipo_actividad_id = self.escoger_tipo_actividad()
            
        # Subtipo de actividad
            
            # Llamamos al metodo para escoger el subtipo de actividad
            subtipo_actividad_id = self.escoger_subtipo_actividad(tipo_actividad_id)
            
        except:
            # Si en algun momento hay un error, mostramos un mensaje de error y salimos de la funcion
            print ("Error en los datos introducidos")
            return   
         
        #Invocación al metodo para insertar la actividad
        self.deportista.insertActivity(fecha=fecha,duracion_horas=duracion_horas,localizacion=localizacion,distancia_kms=distancia_kms,FC_max=FC_max,FC_min=FC_min,tipo_actividad_id=tipo_actividad_id,idDeportista=idDeportista,subtipo_actividad_id=subtipo_actividad_id)
        
        # Obtenemos el nombre del tipo y subtipo de actividad
        tipo_actividad = self.deportista.mapTiposActividad()[tipo_actividad_id]
        subtipo_actividad = self.deportista.mapSubtiposActividad(tipo_actividad_id)[subtipo_actividad_id]
        
        # Mostramos un mensaje al usuario para indicar que se ha insertado la actividad correctamente
        print(f"Se ha insertado la actividad correctamente: {fecha}, {duracion_horas}, {localizacion}, {distancia_kms}, {FC_max}, {FC_min}, {tipo_actividad}, {subtipo_actividad}")
           
    #Vista para la HU Resumen básico sobre mi actividad deportiva a lo largo del tiempo, incluyendo el estado de forma
    def showSummary(self):
        '''
        El deportista se identifica mediante su correo electrónico y se mostrarán sus datos. A continuación, se genera un listado con tipo de actividad, número de sesiones y total distancia, y se mostrará el indicativo sobre el estado de forma del deportista.
        '''
        # Inicio de sesion
        
        # Llama a la vista de inicio de sesion, si devuelve None es que no se ha iniciado sesion correctamente
        idDeportista = self.inicio_sesion_view()
        if idDeportista==None:
            return
        
        # Mostramos el resumen de actividad
        print("\nResumen de actividad: ")

        #Invocación al modelo para obtener el resumen
        res = self.deportista.getSummary(idDeportista)

        # Convertir ID de tipo de actividad a su nombre
        for dict in res:
            dict["TipoActividad"] = self.deportista.mapTiposActividad()[dict["TipoActividadID"]]
            del dict["TipoActividadID"]
        
        # Obtener estado de forma del deportista
        estado_forma = self.gestor_view.getEstadoFormaView()[idDeportista]
        
        # Reordenamos las columnas
        res = [{key: dict[key] for key in ["TipoActividad", "NumeroSesiones", "DistanciaTotal"]} for dict in res]
        
        # Mostramos el resumen con el método printTable de la clase utils
        utils.printTable(res)
        
        # Mostramos el estado de forma
        print(f"Estado de forma: {estado_forma}")

   # Vista para la HU comparación con otro deportista (para Premium)
    def showComparacion(self):
        
        correoDeportista = input("Introduce tu correo: ")
        idDeportista = self.deportista.getIdDeportista(correoDeportista) 

        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
        
        else:
            premium=self.deportista.premium(idDeportista)
            premium = premium[0].get("Premium")
            if premium==False:
                print("Esta funcionalidad solo se permite para deportistas Premium")
            else:
                correoDeportistaComparar = input("Indique el correo del deportista con quien se quiere comparar: ")
                idDeportistaComparar = self.deportista.getIdDeportista(correoDeportistaComparar)
                if idDeportistaComparar==None:
                    print("No existe el deportista con correo",correoDeportistaComparar)
                else:
                    # Deportista premium
                    nombre,apellidos=self.deportista.getNombreCompletoDeportista(correoDeportista)
                    print(f"Iniciado sesion: {correoDeportista}")
                    print(f"\n¡Bienvenido {nombre} {apellidos}!" )
                    print("Iniciando comparacion")
                    sexo,fecha=self.deportista.getSexoFecha(idDeportista)
                    print("Aquí tienes tus datos:")
                    print(f"Nombre: {nombre} Apellidos: {apellidos}")
                    print(f"Sexo: {sexo} Fecha de nacimiento: {fecha}")
                    res = self.deportista.getSummary(idDeportista)
                    for dict in res:
                        print(f"Tipo de actividad: {dict['TipoActividad']}\n -------------------------- \n\tNumero de sesiones: {dict['NumeroSesiones']} \n\tTotal distancia: {dict['DistanciaTotal']} kms \n --------------------------")

                    # Deportista a comparar
                    nombre2,apellidos2=self.deportista.getNombreCompletoDeportista(correoDeportistaComparar)
                    print(f"Datos del deportista a comparar de correo {correoDeportistaComparar}")
                    print(f"Nombre: {nombre2} Apellidos: {apellidos2}")
                    sexo2,fecha2=self.deportista.getSexoFecha(idDeportistaComparar)
                    print(f"Sexo: {sexo2} Fecha de nacimiento: {fecha2}")
                    res2 = self.deportista.getSummary(idDeportistaComparar)
                    for dict in res2:
                        print(f"Tipo de actividad: {dict['TipoActividad']}\n -------------------------- \n\tNumero de sesiones: {dict['NumeroSesiones']} \n\tTotal distancia: {dict['DistanciaTotal']} kms \n --------------------------")
                                
    def showActividadesEnPeriodo(self):
        print("#"*20)
        correoDeportista = str(input("Introducir tu correo: "))

        fecha_inicio = input ("Fecha de inicio (AAAA-MM-DD), dejar vacío si quieres que la fecha sea igual a la actual: ")
        if fecha_inicio=="":
                fecha_inicio = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').strftime("%Y-%m-%d")
            except ValueError:
                    print ("Error en el formato de la fecha, debe tener el formato AAAA-MM-DD")
                    return
        fecha_fin = input ("Fecha de inicio (AAAA-MM-DD), dejar vacío si quieres que la fecha sea igual a la actual: ")
        if fecha_fin=="":
                fecha_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').strftime("%Y-%m-%d")
            except ValueError:
                    print ("Error en el formato de la fecha, debe tener el formato AAAA-MM-DD")
                    return
                
        if fecha_inicio>fecha_fin:
            print("Error en el formato de la fecha, la fecha de inicio no puede ser mayor que la fecha de fin")
            return
        
        idDeportista = self.deportista.getIdDeportista(correoDeportista)
        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
        else:
            nombre,apellidos = self.deportista.getNombreCompletoDeportista(correoDeportista)
            print(f"Iniciado sesion: {correoDeportista}")
            print(f"\n¡Bienvenido {nombre} {apellidos}!" )
            
            print(f"\nResumen de actividad entre {fecha_inicio} y {fecha_fin}: ")
            print ("----------------------------------")
        res = self.deportista.getActividadesEnPeriodo(idDeportista, fecha_inicio, fecha_fin)
        self.printResults(res)
        
    #ver los detalles de las actividades de un tipo realizadas por un deportista (Premium)
    def showActividadesDeportistaTipo(self):

        correoDeportista = input("Introduce tu correo: ")
        idDeportista = self.deportista.getIdDeportista(correoDeportista) 

        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
            return
        else:
            premium=self.deportista.premium(idDeportista)
            premium = premium[0].get("Premium")
            
            if premium==False:
                print("Esta funcionalidad solo se permite para deportistas Premium")
                return
        
        print("#"*20)
        correoDeportista = str(input("Introducir el correo del deportista: "))

        idDeportista = self.deportista.getIdDeportista(correoDeportista)
        
        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
            return
        else:
            nombre,apellidos = self.deportista.getNombreCompletoDeportista(correoDeportista)
        
        tipo_actividad = input (f"Tipo de actividad (carrera o natación): ")
        #Quitar espacios en blanco, saltos de linea y tabuladores, y convertir a minusculas sin acentos
        tipo_actividad = tipo_actividad.strip().lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        actividades = ["carrera", "natacion"]                
        if tipo_actividad not in actividades:
            print (f"Error en el tipo de actividad, debe ser una de estas:{actividades}")
            return
        print(f"\nActividades de {tipo_actividad} realizadas por {nombre} {apellidos}: ")
        print ("----------------------------------")
        if tipo_actividad == "carrera":
           tipo_actividad="Carrera" 
        else:
            tipo_actividad="Natación"
        res = self.deportista.getActividadesDeportistaTipo(idDeportista, tipo_actividad)
        self.printResults(res)           

    #Médodo muy general para imprimir los resultados (res) que vienen del model
    def printResults (self,res):
        if len(res)==0: 
            print ("No hay resultados")
        else:
            #cabecera
            print (list(res[0].keys())) # Imprime nombres de columnas (keys del diccionario)
            print ("----------------------------------")
            #contenido 
            for row in res:
                print ([*row.values()]) # Imprime valor de una fila (values del diccionario)
            print ("----------------------------------")
            
    def importar_csv_view(self):
        '''Método que permite insertar actividades en la base de datos a partir de un csv.
        
        El deportista se identifica mediante su correo electrónico y se mostrarán sus datos. A continuación, se solicitará el nombre del csv a importar, se comprobará que existe y tiene el formato correcto, y se insertarán las actividades en la base de datos.
        '''
        # Inicio de sesion
        id_deportista = self.inicio_sesion_view()
        if id_deportista==None:
            return
        
        # Cargamos el csv
        csv = input("Introduce el nombre del csv: ")
        
        # Quitamos espacios en blanco, dividimos por el punto y añadimos csv para que en caso de que no lo tenga ponerlo
        csv = csv.strip().split(".")[0]+".csv"
        
        # Comprobamos que existe el csv
        if not os.path.isfile(csv):
            print("No existe el csv")
            return
        
        # Comprobamos que el csv tiene el formato correcto
        try:
            df = pd.read_csv(csv)
        # Si hay un error, mostramos un mensaje de error y salimos de la funcion
        except:
            print("Error al leer el csv")
            return
        
        
        # Comprobamos que el csv tiene las columnas correctas
        columnas = ['Fecha', 'DuracionHoras', 'Localizacion', 'DistanciaKms','TipoActividadID', 'FCMax', 'FCMin', 'SubtipoActividadID']
        # Para cada columna, comprobamos que está en el csv
        for columna in columnas:
            # Si no está, mostramos un mensaje de error y salimos de la funcion
            if columna not in df.columns:
                print(f"El csv no tiene la columna {columna}")
                print(f"Las columnas del csv deben ser:\n {columnas}")
                return
        
        # Comprobamos que el csv tiene los tipos de datos correctos
        try:
            df["DuracionHoras"] = pd.to_numeric(df["DuracionHoras"])
            df["DistanciaKms"] = pd.to_numeric(df["DistanciaKms"])
            df["FCMax"] = pd.to_numeric(df["FCMax"])
            df["FCMin"] = pd.to_numeric(df["FCMin"])
            df["TipoActividadID"] = pd.to_numeric(df["TipoActividadID"])
            df["SubtipoActividadID"] = pd.to_numeric(df["SubtipoActividadID"])
        # Si hay un error, mostramos un mensaje de error y salimos de la funcion
        except:
            print("Error en el formato de los datos del csv")
            return

        # Insertamos las actividades
        try:
            # Hacer copia de base de datos
            shutil.copyfile("AppDB.db", "AppDB_copia.db")
            
            # Para cada fila del csv, insertamos la actividad            
            for index, row in df.iterrows():
                
                # Comprobamos que la fecha no es mayor que la actual
                fecha = row["Fecha"]
                if fecha=="":
                    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                if fecha>datetime.datetime.now().strftime("%Y-%m-%d"):
                    print(f"Error en la fila {index+1}, la fecha no puede ser mayor que la actual")
                    return
                
                # Obtenemos los datos de la fila
                duracion_horas = row["DuracionHoras"]
                localizacion = row["Localizacion"]
                distancia_kms = row["DistanciaKms"]
                tipo_actividad_id = row["TipoActividadID"]
                fc_max = row["FCMax"]
                fc_min = row["FCMin"]
                subtipo_actividad_id = row["SubtipoActividadID"]
                
                # Insertamos la actividad
                self.deportista.insertActivity(fecha,duracion_horas,localizacion,distancia_kms,fc_max,fc_min,tipo_actividad_id,id_deportista,subtipo_actividad_id)
            
            # Si todo ha ido bien, mostramos un mensaje de éxito
            print(f"Se han insetado {len(df)} actividades correctamente, {id}")
            
            # Como todo ha ido bien, borramos la copia de la base de datos
            os.remove("AppDB_copia.db")
        
        # Si en alguna fila hay un error, mostramos un mensaje de error y volvemos a la base de datos anterior
        except:
            # Como ha habido un error, volvemos a la base de datos anterior
            # Borramos la base de datos actual
            os.remove("AppDB.db")
            # Restauramos la copia de la base de datos
            shutil.copyfile("AppDB_copia.db", "AppDB.db")
            # Borramos la copia de la base de datos
            os.remove("AppDB_copia.db")
            # Mostramos un mensaje de error al usuario y devolvemos None
            print("Ha ocurrido un error al insertar las actividades")
            return None
        
    def inicio_sesion_view(self):
        '''Método que permite iniciar sesion en la aplicación.
        
        Se solicitará el correo electrónico del deportista y se comprobará que existe en la base de datos. Si existe, se mostrarán los datos del deportista y se devolverá su id. Si no existe, se mostrará un mensaje de error y se devolverá None.
        '''
        
        # Pedimos el correo del deportista
        print("#"*20)
        correoDeportista = input ("Introducir tu correo: ")
        
        # Obtenemos el id del deportista
        idDeportista = self.deportista.getIdDeportista(correoDeportista)
        if idDeportista==None:
            # Si no existe el deportista, mostramos un mensaje de error y devolvemos None
            print ("No existe el deportista con correo:",correoDeportista)
            return None

        # Obtenemos el nombre y apellidos del deportista
        nombre,apellidos = self.deportista.getNombreCompletoDeportista(correoDeportista)
        
        # Mostramos un mensaje de bienvenida
        print(f"Iniciado sesion: {correoDeportista}")
        print(f"\n¡Bienvenido {nombre} {apellidos}!" )
        # Devolvemos el id del deportista
        return idDeportista
    
    def escoger_tipo_actividad(self):
        '''Método que permite escoger el tipo de actividad al deportista, mostrandole todos y dandole a escoger en base a un número.
        
        Se mostrarán los tipos de actividad disponibles y se solicitará el tipo de actividad. Si el tipo de actividad no es correcto, se mostrará un mensaje de error y se volverá a solicitar el tipo de actividad.
        '''
        # Obtenemos los tipos de actividad
        tipos = self.deportista.mapTiposActividad()
        
        # Ensñamos los tipos de actividad y sus ids
        print("Tipos de actividad:")
        for key,value in tipos.items():
            print(f"{key}: {value}")
        tipo_actividad = input("Introduce el tipo de actividad: ")
        
        # Intentamos convertir el tipo de actividad a int
        try:
            tipo_actividad = int(tipo_actividad)
        
        # Si da error, mostramos un mensaje de error y volvemos a pedir el tipo de actividad
        except:
            print("El tipo de actividad debe ser un número")
            return self.escoger_tipo_actividad()
        
        # Si el tipo de actividad no está en los tipos de actividad, mostramos un mensaje de error y volvemos a pedir el tipo de actividad
        if tipo_actividad not in tipos.keys():
            print("El tipo de actividad no es correcto")
            return self.escoger_tipo_actividad()
        
        # Devolvemos el tipo de actividad escogido
        return tipo_actividad  
    
    def escoger_subtipo_actividad(self, tipo_actividad_id):
        '''Método que permite escoger el subtipo de actividad al deportista, mostrandole todos y dandole a escoger en base a un número.	
        
        Se mostrarán los subtipos de actividad disponibles y se solicitará el subtipo de actividad. Si el subtipo de actividad no es correcto, se mostrará un mensaje de error y se volverá a solicitar el subtipo de actividad.
        '''
        # Obtenemos los subtipos de actividad
        subtipos = self.deportista.mapSubtiposActividad(tipo_actividad_id)
        
        # Ensñamos los subtipos de actividad y sus ids
        print("Subtipos de actividad:")
        for key,value in subtipos.items():
            print(f"{key}: {value}")
            
        # Pedimos el subtipo de actividad
        subtipo_actividad = input("Introduce el subtipo de actividad: ")
        
        # Intentamos convertir el subtipo de actividad a int
        try:
            subtipo_actividad = int(subtipo_actividad)
        
        # Si da error, mostramos un mensaje de error y volvemos a pedir el subtipo de actividad
        except:
            print("El subtipo de actividad debe ser un número")
            return self.escoger_subtipo_actividad(tipo_actividad_id)
        
        # Si el subtipo de actividad no está en los subtipos de actividad, mostramos un mensaje de error y volvemos a pedir el subtipo de actividad
        if subtipo_actividad not in subtipos.keys():
            print("El subtipo de actividad no es correcto")
            return self.escoger_subtipo_actividad(tipo_actividad_id)
        
        # Devolvemos el subtipo de actividad escogido
        return subtipo_actividad 