from entidad.entidadModel import EntidadModel
from util.Utils import utils

import datetime
import os
import pandas as pd
import shutil



class EntidadView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a las entidades que estarán
    representadas en la clase EntidadModel (EntidadModel.py)
    '''
     
    def __init__ (self):
        self.entidad = EntidadModel() #Crea un objeto model que se invocará desde esta vista
        self.utils = utils()

    #Vista para la HU Registrar una nueva actividad    
    def addActividadEntidad(self):
        
        '''Método que permite insertar una nueva actividad en la base de datos.
        
        La entidad se identifica escogiendo su nombre de la lista. A continuación, se solicitarán los datos de la actividad a insertar, se comprobará que son correctos y se insertará la actividad en la base de datos.
        '''
        
        # Introdcir los datos de la actividad
        print("\nIntroducir los datos de la actividad")
        try:
        # Entidad
            # Llamamos al metodo para escoger la entidad
            entidad_id = self.escoger_entidad()
        
        # Nombre
            
            # Pedimos el nombre, en este caso puede ser cualquier cosa
            nombreActividad = input ("Nombre de la actividad: ")
            
        # Descripcion
            
            # Pedimos la descripcion, en este caso puede ser cualquier cosa
            descripcion = input ("Descripcion breve de la actividad: ")
        

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
                
                # Si no hay error y se convierte correctamente, comprobamos que la fecha no es anterior a la actual
                if fecha<datetime.datetime.now().strftime("%Y-%m-%d"):
                    # En tal caso, mostramos un mensaje de error y salimos de la funcion
                    print("Error en el formato de la fecha, no puede ser menor que la actual")
                    return
                
        # Duracion en horas
        
            # Pedimos la duracion en horas
            duracion_dias = input ("Duracion en días: ")

            # Intentamos convertir la duracion a int
            try:
                duracion_dias = int(duracion_dias)
            
            # Si da error, mostramos un mensaje de error y salimos de la funcion
            except ValueError:
                print ("Error en el formato de la duracion, debe ser un numero entero")
                return
            
            # Si no hay error, comprobamos que la duracion es positiva
            if duracion_dias < 0:
                # En tal caso, mostramos un mensaje de error y salimos de la funcion
                print ("Error en el formato de la duracion, debe ser un numero entero positivo")
                return
            
        # NumPlazas
            
            # Pedimos el numero de plazas
            numplazas = input ("Número de Plazas: ")
            
            # Intentamos convertir numplazas a int
            try:
                numplazas = int(numplazas)
                
            # Si da error, mostramos un mensaje de error y salimos de la funcion
            except ValueError:
                print ("Error en el formato del número de plazas, debe ser un numero entero")
                return
            
            # Si no hay error, comprobamos que la distancia es positiva
            if numplazas < 0:
                print ("Error en el formato del número de plazas, debe ser un numero entero positivo")
                return
            
        # Coste
            
            # Pedimos el coste
            coste = input ("Coste de la actividad: ")
            
            # Intentamos convertir coste a float
            try:
                coste.replace(",",".")
                coste = float(coste)
                
            # Si da error, mostramos un mensaje de error y salimos de la funcion
            except ValueError:
                print ("Error en el formato del coste, debe ser un numero entero o decimal")
                return
            
            # Si no hay error, comprobamos que la distancia es positiva
            if coste < 0:
                print ("Error en el formato del coste, debe ser un numero entero o decimal positivo")
                return
            
            
        except:
            # Si en algun momento hay un error, mostramos un mensaje de error y salimos de la funcion
            print ("Error en los datos introducidos")
            return   
         
        #Invocación al metodo para insertar la actividad
        self.entidad.InsertActividadEntidad(entidad_id, nombreActividad, descripcion, fecha, duracion_dias, numplazas, coste)
        # Obtenemos el nombre de la entidad
        entidad = self.utils.mapEntidades()[entidad_id]
        
        # Mostramos un mensaje al usuario para indicar que se ha insertado la actividad correctamente
        print(f"Se ha insertado correctamente la actividad {nombreActividad} de {entidad} con fecha {fecha}, duracion {duracion_dias} dias, número de plazas {numplazas} y coste {coste}")
    

    # Vista para la HU de registrar entidad
    def showRegistro(self):
        print('Registrar entidad')
        
        nombre = input('Introduce el nombre de la entidad: ')
        
        if self.utils.comprobarExisteEntidad(nombre):
            print('Ya existe una entidad con ese nombre')
            return
        
        self.entidad.registrarEntidad(nombre)

        print('Entidad registrada correctamente')
    
    '''
    HU #23773
    '''  

    def showInscripcionesActividad(self):
        print("#"*20)
        # Llamamos al metodo para escoger la entidad
        entidad_id = self.escoger_entidad()
        print()
        # Llamamos al metodo para escoger la actividad
        actividad_id = self.escoger_actividad_entidad(entidad_id)
        #obtenemos total inscripciones
        res = self.entidad.getInscripcionesActividad(actividad_id)
        
        entidad = self.entidad.getNombreEntidad(entidad_id)

        
        print()
        print(f"Entidad: {entidad}")
        print(f"Inscripciones de la actividad:")
        utils.printTable(res)

    def escoger_entidad(self):
        '''Método que permite escoger la entidad, mostrandole todas y dandole a escoger en base a un número.
        
        Se mostrarán las entidades disponibles y se solicitará la entidad. Si no es correcta, se mostrará un mensaje de error y se volverá a solicitar el tipo de actividad.
        
        Devuelve la entidad escogida en ID
        '''
        # Obtenemos las entidades
        entidades = self.utils.mapEntidades()
        
        # Ensñamos las entidades y sus ids
        print("Entidades:")
        for key,value in entidades.items():
            print(f"{key}: {value}")
        entidad = input("Introduce la entidad: ")
        
        # Intentamos convertir la entidad a int
        try:
            entidad = int(entidad)
        
        # Si da error, mostramos un mensaje de error y volvemos a pedir la entidad
        except:
            print("La entidad debe ser un número")
            return self.escoger_entidad()
        
        # Si la entidad no está en las entidades, mostramos un mensaje de error y volvemos a pedir la entidad
        if entidad not in entidades.keys():
            print("La entidad no es correcta")
            return self.escoger_entidad()
        
        # Devolvemos la entidad escogida
        return entidad  
    
    def escoger_actividad_entidad(self, idEntidad):
        '''Método que permite escoger una actividad de una entidad, mostrandole todas y dandole a escoger en base a un número.
            
        Se mostrarán las actividades disponibles y se solicitará una. Si no es correcta, se mostrará un mensaje de error y se volverá a solicitar la actividad.
            
        Devuelve la actividad escogida en ID
            '''
        # Obtenemos las actividades
        actividades = self.utils.mapActividadesEntidad(idEntidad)
            
        # Ensñamos las entidades y sus ids
        print("Actividades de la entidad:")
        for key,value in actividades.items():
            key = key + 1 - min(actividades.keys())
            print(f"{key}: {value}")
        actividad = input("Introduce la actividad: ")
            
        # Intentamos convertir la actividad a int
        try:
            actividad = int(actividad)
            
        # Si da error, mostramos un mensaje de error y volvemos a pedir la actividad
        except:
            print("La entidad debe ser un número")
            return self.escoger_entidad()

        # Recuperamos el indice del subtipo de actividad
        actividad = actividad + min(actividades.keys()) - 1    
        # Si la actividad no está en las actividades, mostramos un mensaje de error y volvemos a pedir la actividad
        if actividad not in actividades.keys():
            print("La actividad no es correcta")
            return self.escoger_actividad_entidad(idEntidad)
            
        # Devolvemos la actividad escogida
        return actividad  
        