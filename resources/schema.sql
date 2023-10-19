--Primero se deben borrar todas las tablas (de detalle a maestro) y lugo anyadirlas (de maestro a detalle)

drop table if exists Deportista;
drop table if exists Actividad;

-- Crear la tabla Deportista
CREATE TABLE Deportista(
    ID INTEGER PRIMARY KEY,
    Nombre VARCHAR(255),
    Apellidos VARCHAR(255),
    CorreoElectronico VARCHAR(255) UNIQUE,
    FechaAlta DATE,
    Premium BOOLEAN,
    Sexo VARCHAR(255),
    FechaNacimiento DATE
);

-- Crear la tabla Actividad
CREATE TABLE Actividad(
    ID INTEGER PRIMARY KEY,
    Fecha DATE,
    DuracionHoras DECIMAL(5, 2),
    Localizacion VARCHAR(255),
    DistanciaKms DECIMAL(5, 2),
    FCMax INT,
    FCMin INT,
    TipoActividad VARCHAR(50),
    DeportistaID INT,
    FOREIGN KEY (DeportistaID) REFERENCES Deportista(ID)
);
