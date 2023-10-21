
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
                
                fecha = input ("Fecha (AAAA-MM-DD), dejar vacío si quieres que la fecha sea igual a la actual: ")
                if fecha=="":
                    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                else:
                    try:
                        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').strftime("%Y-%m-%d")
                    except ValueError:
                        print ("Error en el formato de la fecha, debe tener el formato AAAA-MM-DD")
                        return
                
                duracion_horas = input ("Duracion en horas: ")
                try:
                    duracion_horas.replace(",",".")
                    duracion_horas = float(duracion_horas)
                except ValueError:
                    print ("Error en el formato de la duracion, debe ser un numero entero o decimal")
                    return
                
                localizacion = input ("Localizacion: ")
                
                distancia_kms = input ("Distancia en kms: ")
                try:
                    distancia_kms = float(distancia_kms)
                except ValueError:
                    print ("Error en el formato de la distancia, debe ser un numero entero o decimal")
                    return

                FC_max = input ("FC max (opcional): ")
                if FC_max=="":
                    FC_max = None
                else:
                    try :
                        FC_max = int(FC_max)
                    except ValueError:
                        print ("Error en el formato de la FC max, debe ser un numero entero")
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
                
                tipo_actividad = input (f"Tipo de actividad (carrera o natación): ")
                #Quitar espacios en blanco, saltos de linea y tabuladores, y convertir a minusculas sin acentos
                tipo_actividad = tipo_actividad.strip().lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                actividades = ["carrera", "natacion"]                
                if tipo_actividad not in actividades:
                    print (f"Error en el tipo de actividad, debe ser una de estas:{actividades}")
                    return
                
            except:
                print ("Error en los datos introducidos")
                return    
            #Invocación al modelo para insertar la actividad
            self.deportista.insertActivity(fecha,duracion_horas,localizacion,distancia_kms,FC_max,FC_min,tipo_actividad,idDeportista)
            
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
                print(f"Tipo de actividad: {dict['TipoActividad']}\n -------------------------- \n\tNumero de sesiones: {dict['NumeroSesiones']} \n\tTotal distancia: {dict['DistanciaTotal']} kms \n --------------------------")
            
            
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