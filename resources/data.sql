    -- Insert data into the Deportista table
INSERT INTO Deportista (ID, Nombre, Apellidos, CorreoElectronico, FechaAlta, Premium, Sexo, FechaNacimiento, Altura, Peso, ObjetivoHoras, ObjetivoCantidad)
VALUES
    (1, 'Juan',      'Perez',     'juan.perez@example.com',    '2023-01-15', True,  'Masculino', '2004-12-23', 175, 70.5, 3.5, 10),
    (2, 'Maria',     'Gomez',     'maria.gomez@example.com',   '2023-02-20', False, 'Femenino',  '1968-03-21', 160, 62.2, 2.0, 8),
    (3, 'Pedro',     'Lopez',     'pedro.lopez@example.com',   '2023-03-10', True,  'Masculino', '1979-04-06', 180, 80.0, 4.0, 12),
    (4, 'Ana',       'Rodriguez', 'ana.rodriguez@example.com', '2023-04-05', False, 'Femenino',  '2003-12-09', 165, 55.8, 2.5, 8),
    (5, 'Luis',      'Martinez',  'luis.martinez@example.com', '2023-05-12', True,  'Masculino', '2003-12-04', 170, 68.3, 3.0, 9),
    (6, 'Example',   'Examplez',  'example@example.com',       '2023-06-01', False, 'Masculino', '2003-10-22', 185, 75.0, 2.5, 7),
    (7, 'PExample',  'PExamplez', 'pexample@example.com',      '2023-06-01', True,  'Masculino', '2003-10-22', 185, 75.0, 2.5, 7),
    (8, 'nombre',    'apellido',  'c',                         '2023-11-11', True,  'Masculino', '2003-10-22', 185, 75.0, 2.5, 7);


-- Insert data into the Premium table
INSERT INTO Premium (ID, DeportistaID, FormaPago, Facturacion)
VALUES
    ( 1,  1, 'Tarjeta', 'Mensual'),
    ( 2,  3, 'Banco',   'Mensual'),
    ( 3,  5, 'Tarjeta', 'Mensual');



-- Insert data into the Actividad table
INSERT INTO Actividad (ID, Fecha, DuracionHoras, Localizacion, DistanciaKms, FCMax, FCMin, ConsumoCalorico, TipoActividadID, SubtipoActividadID, DeportistaID, Publico)
VALUES
    (1, '2023-01-20',  1.5, 'Parque Central',       5.2,    180, 120, 600,   1, 1, 1, True),
    (2, '2023-02-05',  2.0, 'Gimnasio FitLife',     6.2,    160, 100, 500,   2, 1, 2, False),
    (3, '2023-03-15',  1.0, 'Pista de atletismo',   10.0,   190, 130, 870,   2, 2, 3, True),
    (4, '2023-04-10',  1.5, 'Paseo Maritimo',       7.8,    175, 115, 545,   1, 2, 4, False),
    (5, '2023-05-02',  2.5, 'Bosque Nacional',      12.3,   195, 140, 234.6, 1, 1, 5, False),
    (6, '2023-01-25',  1.0, 'Piscina Municipal',    2.3,    160, 100, 678,   1, 1, 1, False),
    (7, '2023-03-01',  2.5, 'Gimnasio FitLife',     5.0,    185, 125, 456,   2, 2, 3, True),
    (8, '2023-04-20',  1.2, 'Parque Central',       4.0,    170, 110, 333,   2, 1, 4, False),
    (9, '2023-05-10',  3.0, 'Montaña',              15.5,   200, 150, 234,   2, 2, 5, False),
    (10, '2023-02-15', 1.5, 'Pista de atletismo',   8.0,    175, 120, 679,   1, 2, 2, False),
    (11, '2023-06-05', 2.0, 'Paseo Maritimo',       8.7,    180, 125, 124,   2, 1, 6, False),
    (12, '2023-07-20', 1.0, 'Parque Central',       5.0,    170, 120, 981,   2, 2, 6, False),
    (13, '2023-08-10', 2.5, 'Bosque Nacional',      11.0,   185, 130, 478,   1, 1, 6, False),
    (14, '2023-09-15', 1.5, 'Pista de atletismo',   9.0,    175, 120, 224,   2, 2, 6, False),
    (15, '2023-10-05', 3.0, 'Gimnasio FitLife',     10.0,   165, 110, 809,   1, 1, 6, False),
    (16, '2023-06-05', 2.0, 'Paseo Maritimo',       8.7,    180, 125, 445,   2, 1, 7, False),
    (17, '2023-07-20', 1.0, 'Parque Central',       5.0,    170, 120, 632,   2, 2, 7, True),
    (18, '2023-08-10', 2.5, 'Bosque Nacional',      11.0,   185, 130, 773,   1, 1, 7, True),
    (19, '2023-09-15', 1.5, 'Pista de atletismo',   9.0,    175, 120, 553,   2, 2, 7, True),
    (20, '2023-10-05', 3.0, 'Gimnasio FitLife',     10.0,   165, 110, 299,   1, 1, 7, False);



-- Insert data into TipoActividad table
INSERT INTO TipoActividad (ID, Tipo, MET)
VALUES
    (1, 'Carrera',              8),
    (2, 'Natacion',             9),
    (3, 'Ciclismo',             7),
    (4, 'Triatlon',             8),
    (5, 'Remo',                 7),
    (6, 'Escalada',             7),
    (7, 'Patinaje',             6),
    (8, 'Esqui',                9),
    (9, 'Caminata',             6),
    (10, 'Deporte de contacto', 10);

-- Insert data into SubtipoActividad table
INSERT INTO SubtipoActividad (ID, Subtipo, TipoActividadID)
VALUES
    (1, 'Montaña',                  1),
    (2, 'Fondo',                    1),
    (3, 'Sprint',                   1),
    (4, 'Piscina',                  2),
    (5, 'Aguas abiertas',           2),
    (6, 'Buceo',                    2),
    (7, 'Spinning',                 3),
    (8, 'Montaña',                  3),
    (9, 'Asfalto',                  3),
    (10, 'Sprint',                  4),
    (11, 'Olimpico',                4),
    (12, 'Larga distancia',         4),
    (13, 'Maquina',                 5),
    (14, 'Aguas abiertas',          5),
    (15, 'Competicion',             5),
    (16, 'Rocodromo',               6),
    (17, 'Deportiva',               6),
    (18, 'Libre',                   6),
    (19, 'En linea',                7),
    (20, 'Sobre hielo',             7),
    (21, 'Acrobatico',              7),
    (22, 'De fondo',                8),
    (23, 'Descenso',                8),
    (24, 'Acrobatico',              8),
    (25, 'Marcha',                  9),
    (26, 'Ruta',                    9),
    (27, 'Senderismo',              9),
    (28, 'Boxeo',                   10),
    (29, 'Judo',                    10),
    (30, 'Artes marciales mixtas',  10);

-- Insert data into the Entidad table
INSERT INTO Entidad (ID, NombreEntidad)
VALUES
    (1, 'Union Deportiva Asturias'),
    (2, 'Oviedo Club Baloncesto'),
    (3, 'Asociacion Petanca Benalmadena');

-- Insert data into the ActividadEntidad table
INSERT INTO ActividadEntidad (ID, EntidadID, NombreActividad, Descripcion, Fecha, DuracionDias, NumPlazas, Coste)
VALUES
    (1, 1, 'San Silvestre 2023', 'carrera anual de fin de año por la ciudad de Oviedo',                     '2023-12-31', 1, 1000, 5),
    (2, 1, 'Deporte en la calle', 'juegos y actividades de todo tipo en la plaza de la catedral de Oviedo', '2024-1-28',  5, 500,  5),
    (3, 2, 'Torneo OCB juevenil', 'torneo de baloncesto por equipos de juveniles',                          '2023-12-10', 3, 50,   10);

