-- Insert data into the Deportista table
INSERT INTO Deportista (ID, Nombre, Apellidos, CorreoElectronico, FechaAlta, Premium)
VALUES
    (1, 'Juan', 'Perez', 'juan.perez@example.com', '2023-01-15', TRUE),
    (2, 'Maria', 'Gomez', 'maria.gomez@example.com', '2023-02-20', FALSE),
    (3, 'Pedro', 'Lopez', 'pedro.lopez@example.com', '2023-03-10', TRUE),
    (4, 'Ana', 'Rodriguez', 'ana.rodriguez@example.com', '2023-04-05', FALSE),
    (5, 'Luis', 'Martinez', 'luis.martinez@example.com', '2023-05-12', TRUE),
    (6, 'example', 'examplez', 'example@example.com', '2023-06-01', FALSE);

-- Insert data into the Actividad table
INSERT INTO Actividad (ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, TipoActividad, DeportistaID)
VALUES
    (1, '2023-01-20', 1.5, 'Parque Central', 5.2, 180, 120, 'Carrera', 1),
    (2, '2023-02-05', 2.0, 'Gimnasio FitLife', NULL, 160, 100, 'Entrenamiento', 2),
    (3, '2023-03-15', 1.0, 'Pista de atletismo', 10.0, 190, 130, 'Correr', 3),
    (4, '2023-04-10', 1.5, 'Paseo Marítimo', 7.8, 175, 115, 'Caminata', 4),
    (5, '2023-05-02', 2.5, 'Bosque Nacional', 12.3, 195, 140, 'Senderismo', 5),
    (6, '2023-01-25', 1.0, 'Piscina Municipal', NULL, 160, 100, 'Natación', 1),
    (7, '2023-03-01', 2.5, 'Gimnasio FitLife', NULL, 185, 125, 'Entrenamiento', 3),
    (8, '2023-04-20', 1.2, 'Parque Central', 4.0, 170, 110, 'Carrera', 4),
    (9, '2023-05-10', 3.0, 'Montaña', 15.5, 200, 150, 'Senderismo', 5),
    (10, '2023-02-15', 1.5, 'Pista de atletismo', 8.0, 175, 120, 'Correr', 2);