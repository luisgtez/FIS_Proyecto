
import sys
from deportista.deportistaModel import DeportistaModel
import datetime
from pprint import pprint

class DeportistaView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los deportistas que estarán
    representadas en la clase DeportistaModel (DeportistaModel.py)
    '''
     
    def __init__ (self):
        self.deportista = DeportistaModel () #Crea un objeto model que se invocará desde esta vista
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        # self.choices = { "1": self.addActivity,
        #                  "2": self.showSummary,
        #                  "3": self.quit
        #                }
    
    # def displayMenu (self):
    #     print("#"*20)
    #     print(""" Opciones: \n
    #           1.- Registrar nueva actividad
    #           2.- Resumen de actividad
    #           3.- Salir 
    #           """)
    
    #Muestra la lista de opciones y permite la selección
    # def run (self):
    #     while True:
    #         self.displayMenu()
    #         choice = input("Introducir opción: ")
    #         action = self.choices.get(choice)
    #         if action:
    #             action()
    #         else:
    #             print("{0} no es una opción valida\n".format(choice))
    
    #Vista para la HU Registrar una nueva actividad
    def addActivity(self):
        print("#"*20)
        correoDeportista = input ("Introducir tu correo: ")
        #Invocación al modelo para obtener el id de la compañia
        idDeportista = self.deportista.getIdDeportista(correoDeportista)
        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
        else:
            nombre,apellidos = self.deportista.getNombreCompletoDeportista(correoDeportista)
            print(f"Iniciado sesion: {correoDeportista}")
            print(f"\n¡Bienvenido {nombre} {apellidos}!" )
            
            print("\nIntrodcir los datos de la actividad")
            try:
            # Fecha
                fecha = input ("Fecha (AAAA-MM-DD), dejar vacío si quieres que la fecha sea igual a la actual: ")
                if fecha=="":
                    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                else:
                    try:
                        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').strftime("%Y-%m-%d")
                    except ValueError:
                        print ("Error en el formato de la fecha, debe tener el formato AAAA-MM-DD")
                        return
            # Duracion en horas
                duracion_horas = input ("Duracion en horas: ")

                try:
                    duracion_horas.replace(",",".")
                    duracion_horas = float(duracion_horas)
                except ValueError:
                    print ("Error en el formato de la duracion, debe ser un numero entero o decimal")
                    return
                
                if duracion_horas < 0:
                    print ("Error en el formato de la duracion, debe ser un numero entero o decimal positivo")
                    return
                
                # Localizacion
                localizacion = input ("Localizacion: ")
                
                # Distancia en kms
                distancia_kms = input ("Distancia en kms: ")
                try:
                    distancia_kms = float(distancia_kms)
                except ValueError:
                    print ("Error en el formato de la distancia, debe ser un numero entero o decimal")
                    return
                
                if distancia_kms < 0:
                    print ("Error en el formato de la distancia, debe ser un numero entero o decimal positivo")
                    return
    
                # FC max y min
                FC_max = input ("FC max (opcional): ")
                if FC_max=="":
                    FC_max = None
                    
                else:
                    try :
                        FC_max = int(FC_max)
                    except ValueError:
                        print ("Error en el formato de la FC max, debe ser un numero entero")
                        return
                    if FC_max < 0:
                        print ("Error en el formato de la FC max, debe ser un numero entero positivo")
                        return
                
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
                
                tipo_actividad = input (f"Tipo de actividad (carrera o natación): ")
                #Quitar espacios en blanco, saltos de linea y tabuladores, y convertir a minusculas sin acentos
                tipo_actividad = tipo_actividad.strip().lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                actividades = ["carrera", "natacion"]
                
                if tipo_actividad not in actividades:
                    print (f"Error en el tipo de actividad, debe ser una de estas:{actividades}")
                    return

                dict_actividad = {"carrera":"Carrera", "natacion":"Natacion"}
                tipo_actividad = dict_actividad.get(tipo_actividad)
            except:
                print ("Error en los datos introducidos")
                return    
            #Invocación al modelo para insertar la actividad
            self.deportista.insertActivity(fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad,idDeportista)
            
            tipo_actividad = "Natación" if tipo_actividad == "Natacion" else tipo_actividad
            
            print(f"\nSe ha registrado la actividad de \"{tipo_actividad}\" el \"{fecha}\" en \"{localizacion}\" con una duracion de \"{duracion_horas}\" horas y una distancia de \"{distancia_kms}\" kms")
            
    #Vista para la HU Resumen básico sobre mi actividad deportiva a lo largo del tiempo, incluyendo el estado de forma
    def showSummary(self):
        '''
        El deportista se identifica mediante su correo electrónico y se mostrarán sus datos. A continuación, se genera un listado con tipo de actividad, número de sesiones y total distancia, y se mostrará el indicativo sobre el estado de forma del deportista.
        '''
        print("#"*20)
        correoDeportista = input ("Introducir tu correo: ")
        #Invocación al modelo para obtener el id de la compañia
        idDeportista = self.deportista.getIdDeportista(correoDeportista)
        
        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
        else:
            nombre,apellidos = self.deportista.getNombreCompletoDeportista(correoDeportista)
            print(f"Iniciado sesion: {correoDeportista}")
            print(f"\n¡Bienvenido {nombre} {apellidos}!" )
            
            print("\nResumen de actividad: ")
            print ("----------------------------------")

            #Invocación al modelo para obtener el resumen
            res = self.deportista.getSummary(idDeportista)
            for dict in res:
                tipo_actividad = dict.get("TipoActividad")
                tipo_actividad = "Natación" if tipo_actividad == "Natacion" else tipo_actividad
                print(f"Tipo de actividad: {tipo_actividad}\n -------------------------- \n\tNumero de sesiones: {dict['NumeroSesiones']} \n\tTotal distancia: {dict['DistanciaTotal']} kms \n --------------------------")

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

    # Vista para la HU de consumo calorico
    def showConsumoCalorico(self):

        correoDeportista = input("Introduce tu correo: ")
        idDeportista = self.deportista.getIdDeportista(correoDeportista) 

        # Comprobamos que el deportista existe
        if idDeportista==None:
            print ("No existe el deportista con correo:",correoDeportista)
            return
        
        # Actividad que quiere ver consumo calorico
        actividad = input("Introduce actividad para ver consumo calorico: ")

        # Comprobar que la actividad es valida
        query = "SELECT DISTINCT TipoActividad FROM TipoActividad"
        tipo_actividad = self.deportista.query(query)
        tipo_actividad = [x.get("TipoActividad") for x in tipo_actividad]

        if actividad not in tipo_actividad:
            print("Actividad no valida")
            return

        res = self.deportista.getConsumoCalorico(idDeportista,actividad)

        print(f"El consumo calorico para la actividad {actividad} es de {res[0].get('ConsumoCalorico')} calorias por minuto")

    # Vista para la HU de registrar deportista Premium
    def showDeportistaPremium(self):
        print('Registrar deportista premium')
        nombre = input('Introduce tu nombre: ')
        apellidos = input('Introduce tus apellidos: ')
        correo = input('Introduce tu correo: ')
        fecha_nacimiento = input('Introduce tu fecha de nacimiento (AAAA-MM-DD): ')
        sexo = input('Introduce tu sexo (Masculino/Femenino): ')
        peso = input('Introduce tu peso: ')
        altura = input('Introduce tu altura: ')
        facturacion = input('Introduce tu facturacion (solo se permite Mensual): ')  
        formadepago = input('Introduce tu forma de pago (Tarjeta/Transferecia): ')
        if formadepago == 'Tarjeta':
            nombrepropietario = input('Introduce el nombre del propietario de la tarjeta: ')
            numtarjeta = input('Introduce tu numero de tarjeta: ')
            caducidad = input('Introduce la caducidad de tu tarjeta (AAAA-MM-DD): ')
            cvv = input('Introduce el cvv de tu tarjeta: ')
            self.deportista.registrarDeportistaPremium(nombre, apellidos, correo, fecha_nacimiento, sexo, peso, altura, formadepago, facturacion)
            print('Deportista registrado correctamente')
            print('Datos de pago')
            print(f'Nombre: {nombrepropietario}')
            print(f'Numero de tarjeta: {numtarjeta}')
        elif formadepago == 'Transferencia':
            self.deportista.registrarDeportistaPremium(nombre, apellidos, correo, fecha_nacimiento, sexo, peso, altura, formadepago, facturacion)
            print('Deportista registrado correctamente')
            print('Datos de pago')
            print('Transferencia realizada correctamente')
        else:
            print('Forma de pago no valida')
            


              
    # def quit(self):
    #     print("Cerrando opciones.")
    #     sys.exit(0)

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