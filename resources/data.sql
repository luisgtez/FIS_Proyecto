PRAGMA encoding = "UTF-8";


    -- Insert data into the Deportista table
INSERT INTO Deportista (ID, Nombre, Apellidos, CorreoElectronico, FechaAlta, Premium, Sexo, FechaNacimiento, Altura, Peso, ObjetivoHoras, ObjetivoCantidad)
VALUES
    (1, 'Juan', 'Perez', 'juan.perez@example.com', '2023-01-15', 1, 'Masculino', '2004-12-23', 175, 70.5, 3.5, 10),
    (2, 'Maria', 'Gomez', 'maria.gomez@example.com', '2023-02-20', 0, 'Femenino', '1968-03-21', 160, 62.2, 2.0, 8),
    (3, 'Pedro', 'Lopez', 'pedro.lopez@example.com', '2023-03-10', 1, 'Masculino', '1979-04-06', 180, 80.0, 4.0, 12),
    (4, 'Ana', 'Rodriguez', 'ana.rodriguez@example.com', '2023-04-05', 0, 'Femenino', '2003-12-09', 165, 55.8, 2.5, 8),
    (5, 'Luis', 'Martinez', 'luis.martinez@example.com', '2023-05-12', 1, 'Masculino', '2003-12-04', 170, 68.3, 3.0, 9),
    (6, 'Example', 'Examplez', 'example@example.com', '2023-06-01', 0, 'Masculino', '2003-10-22', 185, 75.0, 2.5, 7),
    (7, 'PExample', 'PExamplez', 'pexample@example.com', '2023-06-01', 1, 'Masculino', '2003-10-22', 185, 75.0, 2.5, 7);


-- Insert data into the Premium table
INSERT INTO Premium (ID, DeportistaID, FormaPago, Facturacion)
VALUES
    (1, 1, 'Tarjeta', 'Mensual'),
    (2, 3, 'Banco', 'Mensual'),
    (3, 5, 'Tarjeta', 'Mensual');


-- Insert data into the Actividad table
INSERT INTO Actividad (ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, TipoActividadID, DeportistaID)
VALUES
    (1, '2023-01-20', 1.5, 'Parque Central', 5.2, 180, 120, 1, 1),
    (2, '2023-02-05', 2.0, 'Gimnasio FitLife', 6.2, 160, 100, 2, 2),
    (3, '2023-03-15', 1.0, 'Pista de atletismo', 10.0, 190, 130, 2, 3),
    (4, '2023-04-10', 1.5, 'Paseo Marítimo', 7.8, 175, 115, 1, 4),
    (5, '2023-05-02', 2.5, 'Bosque Nacional', 12.3, 195, 140, 1, 5),
    (6, '2023-01-25', 1.0, 'Piscina Municipal', 2.3, 160, 100, 1, 1),
    (7, '2023-03-01', 2.5, 'Gimnasio FitLife', 5, 185, 125, 2, 3),
    (8, '2023-04-20', 1.2, 'Parque Central', 4.0, 170, 110, 2, 4),
    (9, '2023-05-10', 3.0, 'Montaña', 15.5, 200, 150, 2, 5),
    (10, '2023-02-15', 1.5, 'Pista de atletismo', 8.0, 175, 120, 1, 2),
    (11, '2023-06-05', 2.0, 'Paseo Marítimo', 8.7, 180, 125, 2, 6),
    (12, '2023-07-20', 1.0, 'Parque Central', 5.0, 170, 120, 2, 6),
    (13, '2023-08-10', 2.5, 'Bosque Nacional', 11.0, 185, 130, 1, 6),
    (14, '2023-09-15', 1.5, 'Pista de atletismo', 9.0, 175, 120, 2, 6),
    (15, '2023-10-05', 3.0, 'Gimnasio FitLife', 10, 165, 110, 1, 6),
    (16, '2023-06-05', 2.0, 'Paseo Marítimo', 8.7, 180, 125, 2, 7),
    (17, '2023-07-20', 1.0, 'Parque Central', 5.0, 170, 120, 2, 7),
    (18, '2023-08-10', 2.5, 'Bosque Nacional', 11.0, 185, 130, 1, 7),
    (19, '2023-09-15', 1.5, 'Pista de atletismo', 9.0, 175, 120, 2, 7),
    (20, '2023-10-05', 3.0, 'Gimnasio FitLife', 10, 165, 110, 1,7);


-- Insert data into TipoActividad table

INSERT INTO TipoActividad (ID, Tipo, MET,Subtipo)
VALUES
    (1, 'Carrera', 8, NULL),
    (2, 'Natación',9, NULL),
    (3, 'Carrera', 8, 'Montaña');