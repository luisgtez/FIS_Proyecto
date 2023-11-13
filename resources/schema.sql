--Primero se deben borrar todas las tablas (de detalle a maestro) y lugeo añadirlas (de maestro a detalle)

drop table if exists Deportista;
drop table if exists Actividad;
drop table if exists TipoActividad;
drop table if exists Premium;
drop table if exists SubtipoActividad;

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
    TipoActividadID INTEGER,
    SubtipoActividadID INTEGER,
    DeportistaID INTEGER,
    FOREIGN KEY (DeportistaID) REFERENCES Deportista(ID),
    FOREIGN KEY (TipoActividadID) REFERENCES TipoActividad(ID)
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