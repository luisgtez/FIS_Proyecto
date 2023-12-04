from deportista.deportistaModel import DeportistaModel
from gestor.gestorView import GestorView
from gestor.gestorModel import GestorModel
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
        self.gestor_model = GestorModel() #Crea un objeto model que se invocará desde esta vista
        self.utils = utils()
        
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
            
            if self.deportista.premium(idDeportista)[0].get("Premium")==True:
                publica = input("¿Quieres que la actividad sea pública? S/N: ")
                while publica not in ["S", "N"]:
                    print("Respuesta no válida")
                    publica = input("¿Quieres que la actividad sea pública? S/N: ")
                publica = True if publica == "S" else False
            else:
                print("La actividad será publica. Para poder elegir si la actividad es pública o no, debes ser deportista premium")
                publica = True
                                    
        
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

        # Calculamos el consumo calorico de dicha actividad para guardarla en el registro
        consumo_calorico = self.deportista.getConsumoCalorico(idDeportista,tipo_actividad_id,duracion_horas)
        
        #Invocación al metodo para insertar la actividad
        self.deportista.insertActivity(fecha=fecha,duracion_horas=duracion_horas,localizacion=localizacion,distancia_kms=distancia_kms,FC_max=FC_max,FC_min=FC_min,consumo_calorico=consumo_calorico,tipo_actividad_id=tipo_actividad_id,idDeportista=idDeportista,subtipo_actividad_id=subtipo_actividad_id, publica=publica)
        
        # Obtenemos el nombre del tipo y subtipo de actividad
        tipo_actividad = self.deportista.mapTiposActividad()[tipo_actividad_id]
        subtipo_actividad = self.deportista.mapSubtiposActividad(tipo_actividad_id)[subtipo_actividad_id]
        
        # Mostramos un mensaje al usuario para indicar que se ha insertado la actividad correctamente
        print(f"Se ha insertado la actividad correctamente la actividad con fecha {fecha}, duracion {duracion_horas} horas, localizacion {localizacion}, distancia {distancia_kms} kms, FC max {FC_max}, FC min {FC_min},consumo calórico {consumo_calorico}, tipo de actividad {tipo_actividad} y subtipo de actividad {subtipo_actividad}")


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
        

        #Invocación al modelo para obtener el resumen
        res = self.deportista.getSummary_propio(idDeportista)

        # Si no tiene actividades, mostramos un mensaje de error y salimos de la funcion
        if len(res)==0:
            print("No hay actividades")
            return
        
        # Mostramos el resumen
        print("\nResumen de actividad: \n")
        
        # Convertir ID de tipo de actividad a su nombre
        for dict in res:
            dict["TipoActividad"] = self.deportista.mapTiposActividad()[dict["TipoActividadID"]]
            del dict["TipoActividadID"]
        
        # Obtener estado de forma del deportista
        estado_forma = self.gestor_model.gestorEstadoForma(idDeportista)
        
        # Reordenamos las columnas
        res = [{key: dict[key] for key in ["TipoActividad", "NumeroSesiones", "DistanciaTotal"]} for dict in res]
        
        # Redondeamos la distancia a 2 decimales
        for dict in res:
            dict["DistanciaTotal"] = round(dict["DistanciaTotal"],3)
            
        # Mostramos el resumen con el método printTable de la clase utils
        utils.printTable(res)
        
        # Mostramos el estado de forma
        print(f"Estado de forma: {estado_forma}")

    # Vista para la HU de seguir deportistas (Premium)
    def showSeguir(self):
        idDeportista = self.inicio_sesion_view()
        if idDeportista==None:
            print("No se ha iniciado sesion correctamente")
            return
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
                
                # Comprobamos que el deportista a seguir sea free 
                else:
                    premium=self.deportista.premium(idDeportistaComparar)
                    premium = premium[0].get("Premium")
                    if premium==True:
                        print("El deportista a seguir es Premium,se seguirán sus actividades públicas")
                        self.deportista.seguirDeportista(idDeportista,idDeportistaComparar)

                    else:
                        self.deportista.seguirDeportista(idDeportista,idDeportistaComparar)
                        print("Se ha seguido al deportista con correo",correoDeportistaComparar)
    
    def showComparacion(self):
        idDeportista = self.inicio_sesion_view()
        # Obtenemos el correo del deportista
        if idDeportista==None:
            print("No se ha iniciado sesion correctamente")
            return
        else:
            premium=self.deportista.premium(idDeportista)
            premium = premium[0].get("Premium")
            if premium==False:
                print("Esta funcionalidad solo se permite para deportistas Premium")
            else:      
                # Deportista premium
                print("Iniciando comparacion")
                sexo,fecha=self.deportista.getSexoFecha(idDeportista)
                print("Aquí tienes tus datos:")
                print(f"Sexo: {sexo} Fecha de nacimiento: {fecha}")
                res = self.deportista.getSummary_propio(idDeportista)
                #for dict in res:
                    #tipo_actividad_nombre = self.deportista.mapTiposActividad()[dict["TipoActividadID"]]
                        # print(f"Tipo de actividad: {tipo_actividad_nombre}\n -------------------------- \n\tNumero de sesiones: {dict['NumeroSesiones']} \n\tTotal distancia: {dict['DistanciaTotal']} kms \n --------------------------")
                for dict in res:
                    dict["TipoActividad"] = self.deportista.mapTiposActividad()[dict["TipoActividadID"]]
                    del dict["TipoActividadID"]
                res = [{key: dict[key] for key in ["TipoActividad", "NumeroSesiones", "DistanciaTotal"]} for dict in res]
                utils.printTable(res)

                # Datos deportista a comparar
                deportistas_comparar = self.deportista.getDeportistasComparar(idDeportista)
                for deportistaCorreo in deportistas_comparar:
                    idDeportistaComparar = self.deportista.getIdDeportista(deportistaCorreo)
                    nombre2,apellidos2=self.deportista.getNombreCompletoDeportista(deportistaCorreo)
                    print(f"Datos del deportista a comparar de correo {deportistaCorreo}:")
                    print(f"Nombre: {nombre2} Apellidos: {apellidos2}")
                    sexo2,fecha2=self.deportista.getSexoFecha(idDeportistaComparar)
                    print(f"Sexo: {sexo2} Fecha de nacimiento: {fecha2}")
                    res2 = self.deportista.getSummary_otro(idDeportistaComparar)
                    # for dict in res2:
                    #     tipo_actividad_nombre = self.deportista.mapTiposActividad()[dict["TipoActividadID"]]
                        # print(f"Tipo de actividad: {tipo_actividad_nombre}\n -------------------------- \n\tNumero de sesiones: {dict['NumeroSesiones']} \n\tTotal distancia: {dict['DistanciaTotal']} kms \n --------------------------")
                    # Change tipo_actividad_id to tipo_actividad_nombre
                    for dict in res2:
                        dict["TipoActividad"] = self.deportista.mapTiposActividad()[dict["TipoActividadID"]]
                        del dict["TipoActividadID"]
                    # Change columns order
                    res2 = [{key: dict[key] for key in ["TipoActividad", "NumeroSesiones", "DistanciaTotal"]} for dict in res2]
                    utils.printTable(res2)


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
        fecha_fin = input ("Fecha de fin (AAAA-MM-DD), dejar vacío si quieres que la fecha sea igual a la actual: ")
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
        # self.printResults(res)
        utils.printTable(res)
        
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
        
        
        tipo_actividad = self.escoger_tipo_actividad()
        
        tipo_actividad_nombre = self.deportista.mapTiposActividad()[tipo_actividad]
        
        print(f"\nActividades de {tipo_actividad_nombre} realizadas por {nombre} {apellidos}: ")
        print ("----------------------------------")
        res = self.deportista.getActividadesDeportistaTipo(idDeportista, tipo_actividad)
        # self.printResults(res)    
        utils.printTable(res)       

    # Vista para la HU de registrar deportista 
    def showRegistro(self):
        print('Registrar deportista')
        fechaAlta = datetime.datetime.now().strftime("%Y-%m-%d")
        premium = input('¿Quieres ser deportista premium? (Si/No): ')
        if premium not in ['Si', 'No']:
            print('Respuesta no valida')
            return
        
        premium = True if premium == 'Si' else False
        
        nombre = input('Introduce tu nombre: ')
        apellidos = input('Introduce tus apellidos: ')
        
        correo = input('Introduce tu correo: ')
        while not self.utils.comprobarCorreoEscrito(correo):
            print('Correo no valido')
            correo = input('Introduce tu correo: ')
        
        
        if self.utils.comprobarExisteCorreo(correo):
            print('Ya existe un deportista con ese correo')
            return
        
        
        fecha_nacimiento = input('Introduce tu fecha de nacimiento (AAAA-MM-DD): ')
        try:
            fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime("%Y-%m-%d")
        except:
            print('Fecha de nacimiento no valida')
            return
        
        if fecha_nacimiento>datetime.datetime.now().strftime("%Y-%m-%d"):
            print('Fecha de nacimiento futura no valida')
            return
        
        sexo = input('Introduce tu sexo (Masculino/Femenino): ')
        while sexo not in ['Masculino', 'Femenino']:
            print('Sexo no valido')
            sexo = input('Introduce tu sexo (Masculino/Femenino): ')
        
        peso = input('Introduce tu peso: ')
        try:
            peso = float(peso)
        except:
            print('Peso no valido')
            return
        
        altura = input('Introduce tu altura: ')
        try:
            altura = float(altura)
        except:
            print('Altura no valida')
            return
        
        if not premium:
            self.deportista.registrarDeportista(nombre, apellidos, correo, fecha_nacimiento, sexo, peso, altura, premium=premium, facturacion=None, formapago=None)
            print('Deportista registrado correctamente')
            print('Justificante de registro')
            print(f'Nombre: {nombre}')
            fecha = datetime.datetime.now().date()
            print(f'Se le mandará un correo a {correo} con el justificante de registro a fecha {fecha}')
        
        if premium == True:
            # Facturacion (Mensual)
            print('Facturacion:')
            print('1. Mensual')
            facturacion = input('Introduce tu facturacion (solo se permite Mensual): ')
            while facturacion not in ['1']:
                print('Facturacion no valida')
                facturacion = input('Introduce tu facturacion (solo se permite Mensual): ')
            
            # Forma de pago (Tarjeta o Transferencia)
            print('Forma de pago:')
            print('1. Tarjeta')
            print('2. Transferencia')
            formadepago = input('Introduce tu forma de pago: ')
            # Si no escoge ninguna de las opciones se le indica y vuelve a preguntar
            while formadepago not in ['1', '2']:
                print('Forma de pago no valida')
                formadepago = input('Introduce tu forma de pago: ')
            # Tarjeta
            if formadepago == '1':
                nombrepropietario = input('Introduce el nombre del propietario de la tarjeta: ')
                numtarjeta = input('Introduce tu numero de tarjeta: ')
                caducidad = input('Introduce la caducidad de tu tarjeta (AAAA-MM-DD): ')
                cvv = input('Introduce el cvv de tu tarjeta: ')
                self.deportista.registrarDeportista(nombre, apellidos, correo, fecha_nacimiento, sexo, peso, altura, formadepago, facturacion, premium=premium)
                print('Datos de pago')
                print(f'Nombre: {nombrepropietario}')
                print(f'Numero de tarjeta: {numtarjeta}')
            # Transferencia
            else:
                print("Mandar transferencia a la cuenta ES 1234 5678 9012 3456 7890")
                self.deportista.registrarDeportista(altura=altura, correo=correo, fecha_nacimiento=fecha_nacimiento,apellidos=apellidos,facturacion=facturacion, formapago=formadepago, nombre=nombre, peso=peso, premium=premium, sexo=sexo)
                print('Transferencia realizada correctamente')

            # Justificante de registro
            print('Deportista registrado correctamente')
            print('Justificante de registro')
            print(f'Nombre: {nombre}')
            fecha = datetime.datetime.now().date()
            print(f'Se le mandará un correo a {correo} con el justificante de registro a fecha {fecha}')
            

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
        while not os.path.isfile(csv):
            print("No existe el csv")
            csv = input("Introduce el nombre del csv: ")
            csv = csv.strip().split(".")[0]+".csv"
        
        
        # Comprobamos que el csv tiene el formato correcto
        try:
            df = pd.read_csv(csv)
        # Si hay un error, mostramos un mensaje de error y salimos de la funcion
        except:
            print("Ha ocurrido un error inesperado al leer el csv")
            return            
        
        
        # Comprobamos que el csv tiene las columnas correctas
        columnas = ['Fecha', 'DuracionHoras', 'Localizacion', 'DistanciaKms','TipoActividadID', 'FCMax', 'FCMin', 'SubtipoActividadID', "Publica"]
        # Para cada columna, comprobamos que está en el csv
        for columna in columnas:
            # Si no está, mostramos un mensaje de error y salimos de la funcion
            if columna not in df.columns:
                print(f"El csv no tiene la columna {columna}")
                print(f"Las columnas del csv deben ser:\n{columnas}")
                return
        
        # Comprobamos que el csv tiene los tipos de datos correctos
        try:
            df["DuracionHoras"] = pd.to_numeric(df["DuracionHoras"])
            df["DistanciaKms"] = pd.to_numeric(df["DistanciaKms"])
            df["FCMax"] = pd.to_numeric(df["FCMax"])
            df["FCMin"] = pd.to_numeric(df["FCMin"])
            df["TipoActividadID"] = pd.to_numeric(df["TipoActividadID"])
            df["SubtipoActividadID"] = pd.to_numeric(df["SubtipoActividadID"])
            df["Publica"] = df["Publica"].astype("bool")
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
                    print("\nError en el formato de la fecha, no puede ser mayor que la actual")
                    raise Exception
                
                # Obtenemos los datos de la fila
                duracion_horas = row["DuracionHoras"]
                localizacion = row["Localizacion"]
                distancia_kms = row["DistanciaKms"]
                tipo_actividad_id = row["TipoActividadID"]
                fc_max = row["FCMax"]
                fc_min = row["FCMin"]
                subtipo_actividad_id = row["SubtipoActividadID"]
                publica = row["Publica"]

                # Calculamos el consumo calorico de dicha actividad para guardarla en el registro
                consumo_calorico = self.deportista.getConsumoCalorico(id_deportista,tipo_actividad_id,duracion_horas)
                
                # Insertamos la actividad
                self.deportista.insertActivity(fecha=fecha,duracion_horas=duracion_horas,localizacion=localizacion,distancia_kms=distancia_kms,FC_max=fc_max,FC_min=fc_min,consumo_calorico=consumo_calorico,tipo_actividad_id=tipo_actividad_id,idDeportista=id_deportista,subtipo_actividad_id=subtipo_actividad_id, publica=publica)       
                

            # Si todo ha ido bien, mostramos un mensaje de éxito
            print(f"Se han insertado {len(df)}/{len(df)} actividades correctamente")
            
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
            print(f"\nHa ocurrido un error mientras se insertaba la actividad {index+1}")
            print(f"Se devolvera el registro de actividades a su estado anterior al intento de insertar las actividades de {csv}")
            print(f"Por favor, corrige el csv y vuelve a intentarlo (con el documento completo)") 
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
        print(f"\n¡Bienvenido {nombre} {apellidos}!" )
        # Devolvemos el id del deportista
        return idDeportista
    
    def escoger_tipo_actividad(self):
        '''Método que permite escoger el tipo de actividad al deportista, mostrandole todos y dandole a escoger en base a un número.
        
        Se mostrarán los tipos de actividad disponibles y se solicitará el tipo de actividad. Si el tipo de actividad no es correcto, se mostrará un mensaje de error y se volverá a solicitar el tipo de actividad.
        
        Devuelve el tipo de actividad escogido en ID
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
            key = key + 1 - min(subtipos.keys())
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
        
        # Recuperamos el indice del subtipo de actividad
        subtipo_actividad = subtipo_actividad + min(subtipos.keys()) - 1
        
        # Si el subtipo de actividad no está en los subtipos de actividad, mostramos un mensaje de error y volvemos a pedir el subtipo de actividad
        if subtipo_actividad not in subtipos.keys():
            print("El subtipo de actividad no es correcto")
            return self.escoger_subtipo_actividad(tipo_actividad_id)
        
        # Devolvemos el subtipo de actividad escogido
        return subtipo_actividad
    
    def addObjetivoSemanalView(self):
        
        idDeportista = self.inicio_sesion_view()
        if idDeportista==None:
            print("No se ha iniciado sesion correctamente")
            return
        
        print("¿Qué tipo de objetivo quieres introducir?")
        print("1. Cantidad de horas de deporte semanales")
        print("2. Cantidad de actividades realizadas en la semana")
        opcion = input("Selecciona una opción (1 o 2): ")

        if opcion not in ["1", "2"]:
            print("Opción no válida. Debe seleccionar 1 o 2.")
            return False
        
        opcion = "ObjetivoHoras" if opcion == "1" else "ObjetivoCantidad"
        
        # Comprobar si el objetivo ya existe
        objetivo = self.deportista.comprobarExisteObjetivo(idDeportista, opcion)
        
        # Si hay un objetivo ya establecido
        if objetivo != None:
            print(f"Ya tienes un objetivo establecido: {objetivo}")
            cambiar = input("¿Quieres cambiarlo? (Si/No): ")
            
            if cambiar == "No":
                return False
        
        if opcion == "1":
            objetivoHoras = float(input("Introduce la cantidad de horas de deporte semanales que deseas realizar: "))
            self.deportista.addObjetivoSemanal(idDeportista=idDeportista,tipoObjetivo=opcion, valorObjetivo=objetivoHoras)
        else:
            objetivoCantidad = int(input("Introduce la cantidad de actividades realizadas en la semana que deseas alcanzar: "))
            self.deportista.addObjetivoSemanal(idDeportista=idDeportista,tipoObjetivo=opcion, valorObjetivo=objetivoCantidad)

    
    def inscribir_actividad(self):
        
        idDeportista = self.inicio_sesion_view()
        if idDeportista==None:
            print("No se ha iniciado sesion correctamente")
            return
        
        print("Escoge una de las actividades disponibles:")
        actividades = self.deportista.getActividadesProgramadasPublicas()
        
        utils.printTable(actividades)
        num_actividad = input("Introduce el número de la actividad que quieres inscribirte (Pulsa 0 para salir): ")
        
        if num_actividad == "0":
            return
        
        # try:
        #     num_actividad = int(num_actividad)
        # except:
        #     print("Número de actividad no válido")
        #     return
        
        # if num_actividad < 1 or num_actividad > len(actividades):
        #     print("El numero de actividad debe corresponder con una de las actividades disponibles")
        #     return
        
        while True:
            if num_actividad == "0":
                return
            try:
                num_actividad = int(num_actividad)
                
                if num_actividad < 1 or num_actividad > len(actividades):
                    print("El numero de actividad debe corresponder con una de las actividades disponibles")
                    
                elif self.deportista.EstaInscritoEnActividad(idDeportista, num_actividad):
                    print("Ya estás inscrito en esta actividad") 
                    
                else:
                    break
            except:
                print("Número de actividad no válido")
            
            num_actividad = input("Introduce el número de la actividad que quieres inscribirte (Pulsa 0 para salir): ")
        
            
        
        respuesta = self.deportista.InscribirEnActividad(idDeportista, num_actividad)
        if respuesta == "OK":
            datos_actividad = self.deportista.getDatosActividad(num_actividad)[0]
            print(f"Te has inscrito en la actividad '{datos_actividad['NombreActividad']}', recuerda que se celebra el {datos_actividad['Fecha']}, dura {datos_actividad['DuracionDias']} dias y tiene un coste de {datos_actividad['Coste']}€")
        else:
            print("Ha ocurrido un error al inscribirte en la actividad")
            
        return
            
    def mostrarProgresoObjetivos(self):
        '''Método que muestra por pantalla el progreso del deportista en relación con sus objetivos.'''
        idDeportista = self.inicio_sesion_view()
        if idDeportista is None:
            print("No se ha iniciado sesión correctamente.")
            return

        # Obtener el resumen de actividades del deportista
        resumen_actividades = self.deportista.getSummary_propio(idDeportista)

        if not resumen_actividades:
            print("No hay actividades registradas para mostrar progreso.")
            return

        # Obtener los objetivos del deportista
        objetivos = self.deportista.getObjetivos(idDeportista)

        if not objetivos:
            print("No hay objetivos establecidos para mostrar progreso.")
            return

        # Mostrar resumen de actividades
        print("Resumen de actividades:")
        for resumen in resumen_actividades:
            tipo_actividad_id = resumen.get("TipoActividadID")
            tipo_actividad = self.deportista.mapTipoActividad(tipo_actividad_id)
            print(f"{tipo_actividad}: {resumen.get('NumeroSesiones')} sesiones, {resumen.get('DistanciaTotal')} km")

        # Mostrar progreso en relación con los objetivos
        print("\nProgreso de objetivos:")
        for objetivo in objetivos:
            tipo_objetivo = objetivo.get("TipoObjetivo")
            valor_objetivo = objetivo.get("ValorObjetivo")
            progreso = self.deportista.calcularProgresoObjetivo(idDeportista, tipo_objetivo)

            if tipo_objetivo == "ObjetivoHoras":
                print(f"Objetivo de horas semanales: {valor_objetivo} horas, Progreso: {progreso:.2f} horas")
            elif tipo_objetivo == "ObjetivoCantidad":
                print(f"Objetivo de actividades semanales: {valor_objetivo} actividades, Progreso: {progreso} actividades")
            
        

            
        

    def mostrarComparacionGrupoEdad(self, idDeportista):
        '''Método que muestra la comparación del deportista premium con otros deportistas de su franja de edad.'''
        # Obtener la comparación con el grupo de edad desde el modelo
        comparacion = self.deportista.compararConGrupoEdad(idDeportista)

        # Mostrar los resultados en la consola o manejarlos según tus necesidades
        if comparacion:
            print(f"Comparación con deportistas en la franja de edad de {comparacion['Edad']} años:")
            print("Edad\t#Act Promedio\tCC Media")
            print(f"{comparacion['Edad']}\t{comparacion['NumeroSesionesPromedio']:.2f}\t\t{comparacion['ConsumoCaloricoPromedioGrupo']:.2f} kcal")
            
            print(f"\nResumen del deportista premium:")
            print(f"Edad: {comparacion['Edad']} años")
            print(f"Total de actividades: {comparacion['TotalActividades']}")
            print(f"Consumo calórico promedio: {comparacion['ConsumoCaloricoPromedio']:.2f} kcal")
        else:
            print("No hay suficientes datos para realizar la comparación en este grupo de edad.")
            
        

            
        

    
    def showInforme(self):
        idDeportista = self.inicio_sesion_view()
        if idDeportista==None:
            print("No se ha iniciado sesion correctamente")
            return
        
        # Preguntamos que tipo de informe quiere ver
        print("¿Qué informe quieres ver?")
        print("1. Informe de actividades mensual")
        print("2. Informe de actividades anual")
        opcion = input("Selecciona una opción (1 o 2): ")

        if opcion not in ["1", "2"]:
            print("Opción no válida. Debe seleccionar 1 o 2.")
            return False
        
        # Visualizacion de los informes mensauales
        if opcion == '1':
            print("Has seleccionado el informe de actividades mensual")
            print("Seleccione la forma de visualización de las actrividades:")
            print("1. Por total de actividades")
            print("2. Por subtipo de actividad")
            tipoInforme = input("Selecciona una opción (1 o 2): ")

            if tipoInforme not in ["1", "2"]:
                print("Opción no válida. Debe seleccionar 1 o 2.")
                return False
            
            # Visualización informes por total de actividades
            if tipoInforme == '1':
                print("Has seleccionado el informe de actividades mensual por total de actividades")
                # función get para obtener el informe mensual
                informe = self.deportista.getInformeMensual(idDeportista,1)
                #Mostramos el informe en forma de tabla
                utils.printTable(informe)

            
            # Visualización informes por tipo de actividad
            else:
                print("Has seleccionado el informe de actividades mensual por tipo de actividad")
                # función get para obtener el informe mensual
                informe = self.deportista.getInformeMensual(idDeportista,2)
                #Mostramos el informe en forma de tabla
                utils.printTable(informe)

        # Visualizacion de los inormes anuales
        else:
            print("Has seleccionado el informe de actividades anual")
            print("Seleccione la forma de visualización de las actividades:")
            print("1. Por total de actividades")
            print("2. Por subtipo de actividad")
            tipoInforme = input("Selecciona una opción (1 o 2): ")

            if tipoInforme not in ["1", "2"]:
                print("Opción no válida. Debe seleccionar 1 o 2.")
                return False
            
            # Visualización informes por total de actividades
            if tipoInforme == '1':
                print("Has seleccionado el informe de actividades anual por total de actividades")
                # función get para obtener el informe anual
                informe = self.deportista.getInformeAnual(idDeportista,1)
                #Mostramos el informe en forma de tabla
                utils.printTable(informe)
            
            # Visualización informes por tipo de actividad
            else:
                print("Has seleccionado el informe de actividades anual por tipo de actividad")
                # función get para obtener el informe anual 
                informe = self.deportista.getInformeAnual(idDeportista,2)
                #Mostramos el informe en forma de tabla
                utils.printTable(informe)


    def showInscripcionesDeportista(self):
        print("#"*20)
        correoDeportista = input("Introduce tu correo: ")
        
        if not self.utils.comprobarExisteCorreo(correoDeportista):
            print ("No existe el deportista con correo:",correoDeportista)
            return
        
        idDeportista = self.deportista.getIdDeportista(correoDeportista) 

        premium=self.deportista.premium(idDeportista)
        premium = premium[0].get("Premium")

        res = self.deportista.getInscripcionesDeportista(idDeportista, premium)

        print("Actividades a las que te has inscrito:")
        utils.printTable(res)
            
        

            
        