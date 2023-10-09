--Carga inicial de datos. Se cargan de maestro a detalle

-- Insertar datos de deportistas
INSERT INTO Deportista (ID, Nombre, Apellidos, CorreoElectronico, FechaAlta, Premium, EstadoForma)
VALUES
    (1, 'Juan', 'Pérez', 'juan@example.com', '2023-01-15', TRUE, 'Bueno'),
    (2, 'María', 'García', 'maria@example.com', '2023-02-10', FALSE, 'Decreciente'),
    (3, 'Carlos', 'López', 'carlos@example.com', '2023-03-20', TRUE, 'Muy Bueno'),
    (4, 'Laura', 'Martínez', 'laura@example.com', '2023-04-05', TRUE, 'Bueno'),
    (5, 'Pedro', 'Rodríguez', 'pedro@example.com', '2023-05-12', FALSE, 'Decreciente');

-- Insertar datos de actividades
INSERT INTO Actividad (ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, TipoActividad, DeportistaID)
VALUES
    (1, '2023-01-20', 2.5, 'Parque Central', 5.0, 160, 80, 'Carrera', 1),
    (2, '2023-02-05', 1.0, 'Piscina Municipal', 1.5, 140, 70, 'Natación', 2),
    (3, '2023-03-10', 1.5, 'Pista de Atletismo', 3.0, 165, 85, 'Carrera', 1),
    (4, '2023-03-25', 1.5, 'Piscina Municipal', 2.0, 145, 75, 'Natación', 3),
    (5, '2023-04-02', 2.0, 'Parque Central', 6.0, 155, 85, 'Carrera', 1),
    (6, '2023-05-15', 1.0, 'Piscina Municipal', 1.8, 135, 70, 'Natación', 2),
    (7, '2023-05-20', 2.5, 'Pista de Atletismo', 5.0, 170, 88, 'Carrera', 3),
    (8, '2023-06-01', 1.0, 'Piscina Municipal', 1.7, 140, 72, 'Natación', 4),
    (9, '2023-06-10', 1.5, 'Parque Central', 4.0, 150, 78, 'Carrera', 5),
    (10, '2023-06-20', 1.0, 'Pista de Atletismo', 2.5, 160, 80, 'Carrera', 4);
