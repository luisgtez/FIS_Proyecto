--Primero se deben borrar todas las tablas (de detalle a maestro) y lugeo añadirlas (de maestro a detalle)

drop table if exists Deportista;
drop table if exists Actividad;
drop table if exists TipoActividad;
drop table if exists Premium;
drop table if exists SubtipoActividad;
drop table if exists Inscripcion;
drop table if exists ActividadEntidad;
drop table if exists Entidad;
drop table if exists SeguirDeportista;

-- Crear la tabla Deportista
CREATE TABLE Deportista(
    ID INTEGER PRIMARY KEY,
    Nombre VARCHAR(255),
    Apellidos VARCHAR(255),
    CorreoElectronico VARCHAR(255) UNIQUE,
    FechaAlta DATE,
    Premium BOOLEAN,
    Sexo VARCHAR(255),
    FechaNacimiento DATE,
    Altura INTEGER,
    Peso DECIMAL(6,3),
    ObjetivoHoras DECIMAL(7,3),
    ObjetivoCantidad INTEGER
);

-- Crear la tabla Premium
CREATE TABLE Premium(
    ID INTEGER PRIMARY KEY,
    DeportistaID INTEGER,
    FormaPago VARCHAR(255),
    Facturacion VARCHAR(255),
    FOREIGN KEY (DeportistaID) REFERENCES Deportista(ID)
);

-- Crear la tabla Actividad
CREATE TABLE Actividad(
    ID INTEGER PRIMARY KEY,
    Fecha DATE,
    DuracionHoras DECIMAL(7, 3),
    Localizacion VARCHAR(255),
    DistanciaKms DECIMAL(6, 3),
    FCMax INTEGER,
    FCMin INTEGER,
    ConsumoCalorico DECIMAL(7, 3),
    TipoActividadID INTEGER,
    SubtipoActividadID INTEGER,
    DeportistaID INTEGER,
    Publico BOOLEAN,
    FOREIGN KEY (DeportistaID) REFERENCES Deportista(ID),
    FOREIGN KEY (TipoActividadID) REFERENCES TipoActividad(ID),
    FOREIGN KEY (SubtipoActividadID) REFERENCES SubtipoActividad(ID)
);

-- Crear la tabla TipoActividad
CREATE TABLE TipoActividad(
    ID INTEGER PRIMARY KEY,
    Tipo VARCHAR(255),
    MET INTEGER
);

-- Crear la tabla SubtipoActividad
CREATE TABLE SubtipoActividad(
    ID INTEGER PRIMARY KEY,
    Subtipo VARCHAR(255),
    TipoActividadID INTEGER,
    FOREIGN KEY(TipoActividadID) REFERENCES TipoActividad(ID)
);
-- Crear la tabla Entidad
CREATE TABLE Entidad(
    ID INTEGER PRIMARY KEY,
    NombreEntidad VARCHAR(255)
);

-- Crear la tabla ActividadEntidad
CREATE TABLE ActividadEntidad(
    ID INTEGER PRIMARY KEY,
    EntidadID INTEGER,
    NombreActividad VARCHAR(255),
    Descripcion VARCHAR(255),
    Fecha DATE,
    DuracionDias INTEGER,
    NumPlazas INTEGER,
    Coste DECIMAL(6, 3),
    FOREIGN KEY (EntidadID) REFERENCES Entidad(ID)
  
);

-- Crear la tabla Inscripcion
CREATE TABLE Inscripcion(
    ID INTEGER PRIMARY KEY,
    DeportistaID INTEGER,
    ActividadEntidadID INTEGER,
    FOREIGN KEY (DeportistaID) REFERENCES Deportista(ID),
    FOREIGN KEY (ActividadEntidadID) REFERENCES ActividadEntidad(ID)
  
);

-- Crear la tabla SeguirDeportista
CREATE TABLE SeguirDeportista(
    ID INTEGER PRIMARY KEY,
    DeportistaID INTEGER,
    SeguidorID INTEGER,
    FOREIGN KEY(DeportistaID) REFERENCES Deportista(ID),
    FOREIGN KEY(SeguidorID) REFERENCES Deportista(ID)
);