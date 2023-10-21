-- Insert data into the Deportista table
INSERT INTO Deportista (ID, Nombre, Apellidos, CorreoElectronico, FechaAlta, Premium,Sexo,FechaNacimiento)
VALUES
    (1, 'Juan', 'Perez', 'juan.perez@example.com', '2023-01-15', TRUE,"Masculino", "2004-12-23"),
    (2, 'Maria', 'Gomez', 'maria.gomez@example.com', '2023-02-20', FALSE,"Femenino", "1968-03-21"),
    (3, 'Pedro', 'Lopez', 'pedro.lopez@example.com', '2023-03-10', TRUE,"Masculino", "1979-04-06"),
    (4, 'Ana', 'Rodriguez', 'ana.rodriguez@example.com', '2023-04-05', FALSE,"Femenino", "2003-12-09"),
    (5, 'Luis', 'Martinez', 'luis.martinez@example.com', '2023-05-12', TRUE,"Masculino", "2003-12-04"),
    (6, 'example', 'examplez', 'example@example.com', '2023-06-01', FALSE,"Masculino", "2003-10-22");

-- Insert data into the Actividad table
INSERT INTO Actividad (ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, TipoActividad, DeportistaID)
VALUES
    (1, '2023-01-20', 1.5, 'Parque Central', 5.2, 180, 120, 'Natación', 1),
    (2, '2023-02-05', 2.0, 'Gimnasio FitLife', 6.2, 160, 100, 'Carrera', 2),
    (3, '2023-03-15', 1.0, 'Pista de atletismo', 10.0, 190, 130, 'Carrera', 3),
    (4, '2023-04-10', 1.5, 'Paseo Marítimo', 7.8, 175, 115, 'Natación', 4),
    (5, '2023-05-02', 2.5, 'Bosque Nacional', 12.3, 195, 140, 'Natación', 5),
    (6, '2023-01-25', 1.0, 'Piscina Municipal', 2.3, 160, 100, 'Natación', 1),
    (7, '2023-03-01', 2.5, 'Gimnasio FitLife', 5, 185, 125, 'Carrera', 3),
    (8, '2023-04-20', 1.2, 'Parque Central', 4.0, 170, 110, 'Carrera', 4),
    (9, '2023-05-10', 3.0, 'Montaña', 15.5, 200, 150, 'Carrera', 5),
    (10, '2023-02-15', 1.5, 'Pista de atletismo', 8.0, 175, 120, 'Natación', 2),
    (11, '2023-06-05', 2.0, 'Paseo Marítimo', 8.7, 180, 125, 'Carrera', 6),
    (12, '2023-07-20', 1.0, 'Parque Central', 5.0, 170, 120, 'Carrera', 6),
    (13, '2023-08-10', 2.5, 'Bosque Nacional', 11.0, 185, 130, 'Natación', 6),
    (14, '2023-09-15', 1.5, 'Pista de atletismo', 9.0, 175, 120, 'Carrera', 6),
    (15, '2023-10-05', 3.0, 'Gimnasio FitLife', 10, 165, 110, 'Natación', 6);
