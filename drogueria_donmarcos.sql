-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-10-2026 a las 16:45:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `drogueria_donmarcos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id_categoria` int(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id_categoria`, `nombre`, `descripcion`) VALUES
(2001, 'Medicamentos', 'Productos farmacéuticos'),
(2002, 'Vitaminas', 'Suplementos vitamínicos'),
(2003, 'Cuidado Personal', 'Productos de higiene'),
(2004, 'Óptica', 'Lentes y accesorios'),
(2005, 'Primeros Auxilios', 'Insumos médicos'),
(2006, 'Dermatología', 'Productos para la piel'),
(2007, 'Analgésicos', 'Medicamentos para el dolor'),
(2008, 'Antibióticos', 'Medicamentos antibacterianos'),
(2009, 'Digestivos', 'Productos para el sistema digestivo'),
(2010, 'Antigripales', 'Productos para síntomas de gripe'),
(2011, 'Higiene Bucal', 'Productos para dientes y boca'),
(2012, 'Bebés', 'Productos para bebés'),
(2013, 'Protección Solar', 'Protectores solares'),
(2014, 'Cabello', 'Productos capilares'),
(2015, 'Maquillaje', 'Productos cosméticos'),
(2016, 'Accesorios Médicos', 'Elementos médicos'),
(2017, 'Desinfectantes', 'Productos desinfectantes'),
(2018, 'Tés', 'Infusiones naturales'),
(2019, 'Suplementos', 'Complementos nutricionales'),
(2020, 'Medición', 'Instrumentos de medición'),
(2021, 'Curaciones', 'Material para curaciones'),
(2022, 'Ortopedia', 'Productos ortopédicos'),
(2023, 'Salud Sexual', 'Productos de salud sexual'),
(2024, 'Repelentes', 'Productos contra insectos'),
(2025, 'Nutrición', 'Productos nutricionales');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas_opticas`
--

CREATE TABLE `citas_opticas` (
  `id_citas` int(50) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `motivo` varchar(200) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `dni_client` int(11) DEFAULT NULL,
  `Dni_usu` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `citas_opticas`
--

INSERT INTO `citas_opticas` (`id_citas`, `fecha`, `hora`, `motivo`, `estado`, `dni_client`, `Dni_usu`) VALUES
(6001, '2026-08-01', '08:00:00', 'Examen visual', 'Programada', 1001, 3003),
(6002, '2026-08-02', '09:00:00', 'Dolor ocular', 'Programada', 1002, 3003),
(6003, '2026-08-03', '10:30:00', 'Control de lentes', 'Finalizada', 1003, 3003),
(6004, '2026-08-04', '11:00:00', 'Vision borrosa', 'Programada', 1004, 3003),
(6005, '2026-08-05', '14:00:00', 'Consulta general', 'Cancelada', 1005, 3003),
(6006, '2026-08-06', '08:30:00', 'Examen visual', 'Programada', 1006, 3007),
(6007, '2026-08-07', '09:30:00', 'Control de lentes', 'Programada', 1007, 3007),
(6008, '2026-08-08', '10:00:00', 'Vision borrosa', 'Finalizada', 1008, 3007),
(6009, '2026-08-09', '11:30:00', 'Dolor ocular', 'Programada', 1009, 3007),
(6010, '2026-08-10', '15:00:00', 'Consulta general', 'Programada', 1010, 3007),
(6011, '2026-08-11', '08:00:00', 'Examen visual', 'Programada', 1011, 3011),
(6012, '2026-08-12', '09:00:00', 'Dolor ocular', 'Programada', 1012, 3011),
(6013, '2026-08-13', '10:30:00', 'Control de lentes', 'Finalizada', 1013, 3011),
(6014, '2026-08-14', '11:00:00', 'Vision borrosa', 'Programada', 1014, 3011),
(6015, '2026-08-15', '14:00:00', 'Consulta general', 'Cancelada', 1015, 3011),
(6016, '2026-08-16', '08:30:00', 'Examen visual', 'Programada', 1016, 3015),
(6017, '2026-08-17', '09:30:00', 'Control de lentes', 'Programada', 1017, 3015),
(6018, '2026-08-18', '10:00:00', 'Vision borrosa', 'Finalizada', 1018, 3015),
(6019, '2026-08-19', '11:30:00', 'Dolor ocular', 'Programada', 1019, 3015),
(6020, '2026-08-20', '15:00:00', 'Consulta general', 'Programada', 1020, 3015),
(6021, '2026-08-21', '08:00:00', 'Examen visual', 'Programada', 1021, 3019),
(6022, '2026-08-22', '09:00:00', 'Dolor ocular', 'Programada', 1022, 3019),
(6023, '2026-08-23', '10:30:00', 'Control de lentes', 'Finalizada', 1023, 3019),
(6024, '2026-08-24', '11:00:00', 'Vision borrosa', 'Programada', 1024, 3019),
(6025, '2026-08-25', '14:00:00', 'Consulta general', 'Programada', 1025, 3019),
(6026, '2026-08-06', '08:00:00', 'Examen visual', 'Programada', 1026, 3029),
(6027, '2026-08-07', '08:30:00', 'Control de lentes', 'Programada', 1027, 3031),
(6028, '2026-08-08', '09:00:00', 'Dolor ocular', 'Programada', 1028, 3037),
(6029, '2026-08-09', '09:30:00', 'Visión borrosa', 'Programada', 1029, 3043),
(6030, '2026-08-10', '10:00:00', 'Examen visual', 'Programada', 1030, 3029),
(6031, '2026-08-11', '10:30:00', 'Control de lentes', 'Programada', 1031, 3031),
(6032, '2026-08-12', '11:00:00', 'Consulta general', 'Programada', 1032, 3037),
(6033, '2026-08-13', '11:30:00', 'Dolor ocular', 'Programada', 1033, 3043),
(6034, '2026-08-14', '12:00:00', 'Examen visual', 'Programada', 1034, 3029),
(6035, '2026-08-15', '13:00:00', 'Visión borrosa', 'Programada', 1035, 3031),
(6036, '2026-08-16', '13:30:00', 'Control de lentes', 'Programada', 1036, 3037),
(6037, '2026-08-17', '14:00:00', 'Examen visual', 'Programada', 1037, 3043),
(6038, '2026-08-18', '14:30:00', 'Dolor ocular', 'Programada', 1038, 3029),
(6039, '2026-08-19', '15:00:00', 'Consulta general', 'Programada', 1039, 3031),
(6040, '2026-08-20', '08:00:00', 'Examen visual', 'Programada', 1040, 3037),
(6041, '2026-08-21', '09:00:00', 'Control de lentes', 'Programada', 1041, 3043),
(6042, '2026-08-22', '10:00:00', 'Visión borrosa', 'Programada', 1042, 3029),
(6043, '2026-08-23', '11:00:00', 'Dolor ocular', 'Programada', 1043, 3031),
(6044, '2026-08-24', '13:00:00', 'Examen visual', 'Programada', 1044, 3037),
(6045, '2026-08-25', '14:00:00', 'Control de lentes', 'Programada', 1045, 3043);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `dni_client` int(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `telefono` int(50) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `direccion` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`dni_client`, `nombre`, `apellido`, `telefono`, `correo`, `direccion`) VALUES
(1001, 'Carlos', 'Pérez', 320000001, 'carlos@gmail.com', 'Cúcuta'),
(1002, 'María', 'Gómez', 320000002, 'maria@gmail.com', 'Villa del Rosario'),
(1003, 'Luis', 'Ramírez', 320000003, 'luis@gmail.com', 'Los Patios'),
(1004, 'Ana', 'Torres', 320000004, 'ana@gmail.com', 'El Zulia'),
(1005, 'Sofía', 'Moreno', 320000005, 'sofia@gmail.com', 'Pamplona'),
(1006, 'Juan', 'Rodríguez', 320000006, 'juan@gmail.com', 'Cúcuta'),
(1007, 'Valentina', 'Hernández', 320000007, 'valentina@gmail.com', 'Villa del Rosario'),
(1008, 'Diego', 'Martínez', 320000008, 'diego@gmail.com', 'Los Patios'),
(1009, 'Camila', 'Díaz', 320000009, 'camila@gmail.com', 'El Zulia'),
(1010, 'Andrés', 'Castro', 320000010, 'andres@gmail.com', 'Pamplona'),
(1011, 'Laura', 'Rojas', 320000011, 'laura@gmail.com', 'Cúcuta'),
(1012, 'Jorge', 'López', 320000012, 'jorge@gmail.com', 'Villa del Rosario'),
(1013, 'Paula', 'Vargas', 320000013, 'paula@gmail.com', 'Los Patios'),
(1014, 'Mateo', 'Sánchez', 320000014, 'mateo@gmail.com', 'El Zulia'),
(1015, 'Daniela', 'Mendoza', 320000015, 'daniela@gmail.com', 'Pamplona'),
(1016, 'Sebastián', 'Guerrero', 320000016, 'sebastian@gmail.com', 'Cúcuta'),
(1017, 'Natalia', 'Ortiz', 320000017, 'natalia@gmail.com', 'Villa del Rosario'),
(1018, 'Miguel', 'Silva', 320000018, 'miguel@gmail.com', 'Los Patios'),
(1019, 'Isabella', 'Ramírez', 320000019, 'isabella@gmail.com', 'El Zulia'),
(1020, 'Samuel', 'Morales', 320000020, 'samuel@gmail.com', 'Pamplona'),
(1021, 'Gabriela', 'Cárdenas', 320000021, 'gabriela@gmail.com', 'Cúcuta'),
(1022, 'Alejandro', 'Vega', 320000022, 'alejandro@gmail.com', 'Villa del Rosario'),
(1023, 'Manuela', 'Navarro', 320000023, 'manuela@gmail.com', 'Los Patios'),
(1024, 'David', 'Pineda', 320000024, 'david@gmail.com', 'El Zulia'),
(1025, 'Sara', 'Molina', 320000025, 'sara@gmail.com', 'Pamplona'),
(1026, 'Daniel', 'Vargas', 315100001, 'daniel.vargas@gmail.com', 'Cúcuta'),
(1027, 'Valentina', 'Rojas', 315100002, 'valentina.rojas@gmail.com', 'Los Patios'),
(1028, 'Miguel', 'Castillo', 315100003, 'miguel.castillo@gmail.com', 'Villa del Rosario'),
(1029, 'Isabella', 'Mendoza', 315100004, 'isabella.mendoza@gmail.com', 'Cúcuta'),
(1030, 'Sebastián', 'Pérez', 315100005, 'sebastian.perez@gmail.com', 'El Zulia'),
(1031, 'Gabriela', 'Suárez', 315100006, 'gabriela.suarez@gmail.com', 'Cúcuta'),
(1032, 'Mateo', 'Ramírez', 315100007, 'mateo.ramirez@gmail.com', 'Los Patios'),
(1033, 'Natalia', 'Torres', 315100008, 'natalia.torres@gmail.com', 'Cúcuta'),
(1034, 'Alejandro', 'Moreno', 315100009, 'alejandro.moreno@gmail.com', 'Villa del Rosario'),
(1035, 'Mariana', 'Gómez', 315100010, 'mariana.gomez@gmail.com', 'Cúcuta'),
(1036, 'Samuel', 'Díaz', 315100011, 'samuel.diaz@gmail.com', 'Los Patios'),
(1037, 'Laura', 'Martínez', 315100012, 'laura.martinez@gmail.com', 'Cúcuta'),
(1038, 'Nicolás', 'Castro', 315100013, 'nicolas.castro@gmail.com', 'El Zulia'),
(1039, 'Camila', 'López', 315100014, 'camila.lopez@gmail.com', 'Cúcuta'),
(1040, 'Juan', 'Hernández', 315100015, 'juan.hernandez@gmail.com', 'Los Patios'),
(1041, 'Sofía', 'Vargas', 315100016, 'sofia.vargas@gmail.com', 'Cúcuta'),
(1042, 'Tomás', 'Rojas', 315100017, 'tomas.rojas@gmail.com', 'Villa del Rosario'),
(1043, 'Luciana', 'Moreno', 315100018, 'luciana.moreno@gmail.com', 'Cúcuta'),
(1044, 'David', 'Torres', 315100019, 'david.torres@gmail.com', 'Los Patios'),
(1045, 'Manuela', 'Ramírez', 315100020, 'manuela.ramirez@gmail.com', 'Cúcuta');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compra`
--

CREATE TABLE `compra` (
  `id_compra` int(50) NOT NULL,
  `fecha` date DEFAULT NULL,
  `total` decimal(12,2) DEFAULT NULL,
  `id_provedor` int(11) DEFAULT NULL,
  `Dni_usu` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `compra`
--

INSERT INTO `compra` (`id_compra`, `fecha`, `total`, `id_provedor`, `Dni_usu`) VALUES
(9001, '2026-06-01', 60000.00, 4001, 3001),
(9002, '2026-06-02', 105000.00, 4002, 3001),
(9003, '2026-06-03', 50000.00, 4003, 3005),
(9004, '2026-06-04', 180000.00, 4004, 3001),
(9005, '2026-06-05', 100000.00, 4005, 3005),
(9006, '2026-06-06', 65000.00, 4006, 3001),
(9007, '2026-06-07', 90000.00, 4007, 3005),
(9008, '2026-06-08', 90000.00, 4008, 3001),
(9009, '2026-06-09', 60000.00, 4009, 3005),
(9010, '2026-06-10', 60000.00, 4010, 3001),
(9011, '2026-06-11', 70000.00, 4011, 3005),
(9012, '2026-06-12', 180000.00, 4012, 3001),
(9013, '2026-06-13', 220000.00, 4013, 3005),
(9014, '2026-06-14', 90000.00, 4014, 3001),
(9015, '2026-06-15', 60000.00, 4015, 3005),
(9016, '2026-06-16', 120000.00, 4016, 3001),
(9017, '2026-06-17', 90000.00, 4017, 3005),
(9018, '2026-06-18', 100000.00, 4018, 3001),
(9019, '2026-06-19', 200000.00, 4019, 3005),
(9020, '2026-06-20', 175000.00, 4020, 3001),
(9021, '2026-06-21', 60000.00, 4021, 3005),
(9022, '2026-06-22', 140000.00, 4022, 3001),
(9023, '2026-06-23', 75000.00, 4023, 3005),
(9024, '2026-06-24', 140000.00, 4024, 3001),
(9025, '2026-06-25', 150000.00, 4025, 3005),
(9026, '2026-07-25', 50000.00, 4026, 3026),
(9027, '2026-07-26', 37500.00, 4027, 3027),
(9028, '2026-07-27', 80000.00, 4028, 3028),
(9029, '2026-07-28', 87500.00, 4029, 3030),
(9030, '2026-07-29', 60000.00, 4030, 3032),
(9031, '2026-07-30', 50000.00, 4031, 3033),
(9032, '2026-07-31', 90000.00, 4032, 3035),
(9033, '2026-08-01', 160000.00, 4033, 3036),
(9034, '2026-08-02', 70000.00, 4034, 3038),
(9035, '2026-08-03', 60000.00, 4035, 3039),
(9036, '2026-08-04', 60000.00, 4036, 3041),
(9037, '2026-08-05', 100000.00, 4037, 3042),
(9038, '2026-08-06', 105000.00, 4038, 3044),
(9039, '2026-08-07', 180000.00, 4039, 3026),
(9040, '2026-08-08', 90000.00, 4040, 3027),
(9041, '2026-08-09', 60000.00, 4041, 3028),
(9042, '2026-08-10', 112500.00, 4042, 3030),
(9043, '2026-08-11', 70000.00, 4043, 3032),
(9044, '2026-08-12', 190000.00, 4044, 3035),
(9045, '2026-08-13', 120000.00, 4045, 3036),
(9046, '2026-10-16', 39500.00, 4010, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_compra`
--

CREATE TABLE `detalle_compra` (
  `id_detalle` int(50) NOT NULL,
  `cantidad` int(50) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(12,2) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `id_compra` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_compra`
--

INSERT INTO `detalle_compra` (`id_detalle`, `cantidad`, `precio_unitario`, `subtotal`, `id_producto`, `id_compra`) VALUES
(10001, 50, 1200.00, 60000.00, 5001, 9001),
(10002, 30, 3500.00, 105000.00, 5002, 9002),
(10003, 20, 2500.00, 50000.00, 5003, 9003),
(10004, 10, 18000.00, 180000.00, 5004, 9004),
(10005, 20, 5000.00, 100000.00, 5005, 9005),
(10006, 10, 6500.00, 65000.00, 5006, 9006),
(10007, 50, 1800.00, 90000.00, 5007, 9007),
(10008, 20, 4500.00, 90000.00, 5008, 9008),
(10009, 50, 1200.00, 60000.00, 5009, 9009),
(10010, 20, 3000.00, 60000.00, 5010, 9010),
(10011, 20, 3500.00, 70000.00, 5011, 9011),
(10012, 10, 18000.00, 180000.00, 5012, 9012),
(10013, 10, 22000.00, 220000.00, 5013, 9013),
(10014, 10, 9000.00, 90000.00, 5014, 9014),
(10015, 10, 6000.00, 60000.00, 5015, 9015),
(10016, 10, 12000.00, 120000.00, 5016, 9016),
(10017, 20, 4500.00, 90000.00, 5017, 9017),
(10018, 20, 5000.00, 100000.00, 5018, 9018),
(10019, 20, 10000.00, 200000.00, 5019, 9019),
(10020, 5, 35000.00, 175000.00, 5020, 9020),
(10021, 20, 3000.00, 60000.00, 5021, 9021),
(10022, 10, 14000.00, 140000.00, 5022, 9022),
(10023, 15, 5000.00, 75000.00, 5023, 9023),
(10024, 20, 7000.00, 140000.00, 5024, 9024),
(10025, 10, 15000.00, 150000.00, 5025, 9025),
(10026, 20, 2500.00, 50000.00, 5026, 9026),
(10027, 25, 1500.00, 37500.00, 5027, 9027),
(10028, 20, 4000.00, 80000.00, 5028, 9028),
(10029, 25, 3500.00, 87500.00, 5029, 9029),
(10030, 20, 3000.00, 60000.00, 5030, 9030),
(10031, 20, 2500.00, 50000.00, 5031, 9031),
(10032, 15, 6000.00, 90000.00, 5032, 9032),
(10033, 10, 16000.00, 160000.00, 5033, 9033),
(10034, 20, 3500.00, 70000.00, 5034, 9034),
(10035, 30, 2000.00, 60000.00, 5035, 9035),
(10036, 20, 3000.00, 60000.00, 5036, 9036),
(10037, 20, 5000.00, 100000.00, 5037, 9037),
(10038, 15, 7000.00, 105000.00, 5038, 9038),
(10039, 10, 18000.00, 180000.00, 5039, 9039),
(10040, 20, 4500.00, 90000.00, 5040, 9040),
(10041, 20, 3000.00, 60000.00, 5041, 9041),
(10042, 25, 4500.00, 112500.00, 5042, 9042),
(10043, 20, 3500.00, 70000.00, 5043, 9043),
(10044, 10, 19000.00, 190000.00, 5044, 9044),
(10045, 10, 12000.00, 120000.00, 5045, 9045),
(10046, 1, 6000.00, 6000.00, 5032, 9046),
(10047, 1, 3000.00, 3000.00, 5021, 9046),
(10048, 1, 4500.00, 4500.00, 5042, 9046),
(10049, 1, 10000.00, 10000.00, 5019, 9046),
(10050, 1, 16000.00, 16000.00, 5033, 9046);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id_detalle` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `id_venta` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id_detalle`, `cantidad`, `precio_unitario`, `subtotal`, `id_venta`, `id_producto`) VALUES
(11001, 2, 2000.00, 4000.00, 7001, 5001),
(11002, 2, 5000.00, 10000.00, 7001, 5002),
(11003, 1, 4000.00, 4000.00, 7001, 5003),
(11004, 1, 7500.00, 7500.00, 7001, 5005),
(11005, 1, 2000.00, 2000.00, 7002, 5001),
(11006, 1, 3000.00, 3000.00, 7002, 5007),
(11007, 1, 5000.00, 5000.00, 7002, 5010),
(11008, 1, 2200.00, 2200.00, 7002, 5009),
(11009, 2, 2000.00, 4000.00, 7003, 5001),
(11010, 1, 3000.00, 3000.00, 7003, 5007),
(11011, 1, 4000.00, 4000.00, 7003, 5003),
(11012, 1, 2200.00, 2200.00, 7003, 5009),
(11013, 1, 7500.00, 7500.00, 7004, 5005),
(11014, 1, 4000.00, 4000.00, 7004, 5003),
(11015, 1, 3000.00, 3000.00, 7004, 5007),
(11016, 1, 5000.00, 5000.00, 7004, 5010),
(11017, 1, 25000.00, 25000.00, 7005, 5004),
(11018, 1, 4000.00, 4000.00, 7005, 5003),
(11019, 1, 5000.00, 5000.00, 7005, 5002),
(11020, 1, 3000.00, 3000.00, 7005, 5007),
(11021, 1, 9500.00, 9500.00, 7006, 5006),
(11022, 1, 5000.00, 5000.00, 7006, 5002),
(11023, 1, 3000.00, 3000.00, 7006, 5007),
(11024, 1, 2200.00, 2200.00, 7006, 5009),
(11025, 1, 3000.00, 3000.00, 7007, 5007),
(11026, 1, 11000.00, 11000.00, 7032, 5038),
(11027, 1, 26000.00, 26000.00, 7032, 5039),
(11028, 1, 3500.00, 3500.00, 7032, 5035),
(11029, 1, 5500.00, 5500.00, 7033, 5041),
(11030, 2, 7000.00, 14000.00, 7033, 5042),
(11031, 1, 6000.00, 6000.00, 7033, 5043),
(11032, 1, 18000.00, 18000.00, 7033, 5045),
(11033, 1, 7000.00, 7000.00, 7034, 5040),
(11034, 1, 5500.00, 5500.00, 7034, 5041),
(11035, 1, 6000.00, 6000.00, 7034, 5043),
(11036, 1, 18000.00, 18000.00, 7034, 5045),
(11037, 2, 7000.00, 14000.00, 7035, 5042),
(11038, 1, 6000.00, 6000.00, 7035, 5043),
(11039, 1, 3500.00, 3500.00, 7035, 5034),
(11040, 1, 12500.00, 12500.00, 7035, 5037),
(11041, 1, 4000.00, 4000.00, 7036, 5026),
(11042, 1, 5000.00, 5000.00, 7036, 5030),
(11043, 1, 6000.00, 6000.00, 7036, 5034),
(11044, 1, 13000.00, 13000.00, 7036, 5038),
(11045, 1, 8000.00, 8000.00, 7037, 5026),
(11046, 1, 6500.00, 6500.00, 7037, 5028),
(11047, 1, 9500.00, 9500.00, 7037, 5032),
(11048, 1, 19000.00, 19000.00, 7037, 5044),
(11049, 1, 5000.00, 5000.00, 7038, 5030),
(11050, 2, 7000.00, 14000.00, 7038, 5042),
(11081, 1, 5000.00, 5000.00, 7021, 5021),
(11082, 1, 3000.00, 3000.00, 7021, 5007),
(11083, 1, 2000.00, 2000.00, 7021, 5001),
(11084, 1, 2200.00, 2200.00, 7021, 5009),
(11085, 1, 20000.00, 20000.00, 7022, 5022),
(11086, 1, 5000.00, 5000.00, 7022, 5002),
(11087, 1, 3000.00, 3000.00, 7022, 5007),
(11088, 1, 2000.00, 2000.00, 7022, 5001),
(11089, 1, 8000.00, 8000.00, 7023, 5023),
(11090, 1, 5000.00, 5000.00, 7023, 5002),
(11091, 1, 3000.00, 3000.00, 7023, 5007),
(11092, 1, 2000.00, 2000.00, 7023, 5001),
(11093, 1, 10000.00, 10000.00, 7024, 5024),
(11094, 1, 5000.00, 5000.00, 7024, 5002),
(11095, 1, 3000.00, 3000.00, 7024, 5007),
(11096, 1, 2000.00, 2000.00, 7024, 5001),
(11097, 1, 22000.00, 22000.00, 7025, 5025),
(11098, 1, 5000.00, 5000.00, 7025, 5002),
(11099, 1, 3000.00, 3000.00, 7025, 5007),
(11100, 1, 2000.00, 2000.00, 7025, 5001),
(11101, 3, 6500.00, 19500.00, 7046, 5028),
(11102, 10, 20000.00, 200000.00, 7047, 1234565432);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimiento_inventario`
--

CREATE TABLE `movimiento_inventario` (
  `id_movimiento` int(50) NOT NULL,
  `tipo_movimiento` varchar(100) DEFAULT NULL,
  `cantidad` int(50) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `motivo` varchar(150) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `Dni_usu` int(11) DEFAULT NULL,
  `id_compra` int(50) DEFAULT NULL,
  `id_venta` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimiento_inventario`
--

INSERT INTO `movimiento_inventario` (`id_movimiento`, `tipo_movimiento`, `cantidad`, `fecha`, `motivo`, `id_producto`, `Dni_usu`, `id_compra`, `id_venta`) VALUES
(8001, 'Entrada', 50, '2026-07-01', 'Compra proveedor', 5001, 3002, NULL, NULL),
(8002, 'Salida', 5, '2026-07-02', 'Venta al cliente', 5002, 3004, NULL, NULL),
(8003, 'Entrada', 30, '2026-07-03', 'Reposicion de inventario', 5003, 3002, NULL, NULL),
(8004, 'Salida', 2, '2026-07-04', 'Venta al cliente', 5004, 3004, NULL, NULL),
(8005, 'Entrada', 20, '2026-07-05', 'Compra proveedor', 5005, 3002, NULL, NULL),
(8006, 'Salida', 3, '2026-07-06', 'Venta al cliente', 5006, 3006, NULL, NULL),
(8007, 'Entrada', 40, '2026-07-07', 'Compra proveedor', 5007, 3008, NULL, NULL),
(8008, 'Salida', 5, '2026-07-08', 'Venta al cliente', 5008, 3006, NULL, NULL),
(8009, 'Entrada', 25, '2026-07-09', 'Reposicion de inventario', 5009, 3008, NULL, NULL),
(8010, 'Salida', 4, '2026-07-10', 'Venta al cliente', 5010, 3006, NULL, NULL),
(8011, 'Entrada', 30, '2026-07-11', 'Compra proveedor', 5011, 3010, NULL, NULL),
(8012, 'Salida', 6, '2026-07-12', 'Venta al cliente', 5012, 3012, NULL, NULL),
(8013, 'Entrada', 20, '2026-07-13', 'Compra proveedor', 5013, 3014, NULL, NULL),
(8014, 'Salida', 3, '2026-07-14', 'Venta al cliente', 5014, 3012, NULL, NULL),
(8015, 'Entrada', 25, '2026-07-15', 'Reposicion de inventario', 5015, 3014, NULL, NULL),
(8016, 'Salida', 4, '2026-07-16', 'Venta al cliente', 5016, 3016, NULL, NULL),
(8017, 'Entrada', 35, '2026-07-17', 'Compra proveedor', 5017, 3018, NULL, NULL),
(8018, 'Salida', 5, '2026-07-18', 'Venta al cliente', 5018, 3020, NULL, NULL),
(8019, 'Entrada', 20, '2026-07-19', 'Compra proveedor', 5019, 3016, NULL, NULL),
(8020, 'Salida', 2, '2026-07-20', 'Venta al cliente', 5020, 3018, NULL, NULL),
(8021, 'Entrada', 40, '2026-07-21', 'Reposicion de inventario', 5021, 3020, NULL, NULL),
(8022, 'Salida', 3, '2026-07-22', 'Venta al cliente', 5022, 3022, NULL, NULL),
(8023, 'Entrada', 15, '2026-07-23', 'Compra proveedor', 5023, 3024, NULL, NULL),
(8024, 'Salida', 4, '2026-07-24', 'Venta al cliente', 5024, 3022, NULL, NULL),
(8025, 'Entrada', 20, '2026-07-25', 'Compra proveedor', 5025, 3024, NULL, NULL),
(8026, 'Salida', 2, '2026-08-01', 'Venta al cliente', 5026, 3026, NULL, NULL),
(8027, 'Salida', 2, '2026-08-02', 'Venta al cliente', 5027, 3027, NULL, NULL),
(8028, 'Salida', 2, '2026-08-03', 'Venta al cliente', 5028, 3028, NULL, NULL),
(8029, 'Salida', 1, '2026-08-04', 'Venta al cliente', 5032, 3030, NULL, NULL),
(8030, 'Entrada', 20, '2026-08-05', 'Compra proveedor', 5030, 3032, NULL, NULL),
(8031, 'Salida', 2, '2026-08-06', 'Venta al cliente', 5028, 3033, NULL, NULL),
(8032, 'Entrada', 15, '2026-08-07', 'Reposición de inventario', 5038, 3035, NULL, NULL),
(8033, 'Salida', 1, '2026-08-08', 'Venta al cliente', 5045, 3036, NULL, NULL),
(8034, 'Entrada', 20, '2026-08-09', 'Compra proveedor', 5034, 3038, NULL, NULL),
(8035, 'Salida', 1, '2026-08-10', 'Venta al cliente', 5044, 3039, NULL, NULL),
(8036, 'Salida', 1, '2026-08-11', 'Venta al cliente', 5038, 3041, NULL, NULL),
(8037, 'Entrada', 25, '2026-08-12', 'Compra proveedor', 5042, 3042, NULL, NULL),
(8038, 'Salida', 1, '2026-08-13', 'Venta al cliente', 5043, 3044, NULL, NULL),
(8039, 'Entrada', 15, '2026-08-14', 'Reposición de inventario', 5029, 3026, NULL, NULL),
(8040, 'Salida', 1, '2026-08-15', 'Venta al cliente', 5039, 3027, NULL, NULL),
(8041, 'Entrada', 20, '2026-08-16', 'Compra proveedor', 5040, 3028, NULL, NULL),
(8042, 'Salida', 1, '2026-08-17', 'Venta al cliente', 5045, 3030, NULL, NULL),
(8043, 'Entrada', 15, '2026-08-18', 'Reposición de inventario', 5032, 3032, NULL, NULL),
(8044, 'Salida', 1, '2026-08-19', 'Venta al cliente', 5035, 3035, NULL, NULL),
(8045, 'Entrada', 10, '2026-08-20', 'Compra proveedor', 5045, 3036, NULL, NULL),
(8046, 'Entrada', 1, '2026-10-16', 'Compra #9046', 5032, NULL, 9046, NULL),
(8047, 'Entrada', 1, '2026-10-16', 'Compra #9046', 5021, NULL, 9046, NULL),
(8048, 'Entrada', 1, '2026-10-16', 'Compra #9046', 5042, NULL, 9046, NULL),
(8049, 'Entrada', 1, '2026-10-16', 'Compra #9046', 5019, NULL, 9046, NULL),
(8050, 'Entrada', 1, '2026-10-16', 'Compra #9046', 5033, NULL, 9046, NULL),
(8051, 'Salida', 3, '2026-10-16', 'Venta #7046', 5028, NULL, NULL, 7046),
(8052, 'Salida', 10, '2026-10-16', 'Venta #7047', 1234565432, NULL, NULL, 7047);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_producto` int(50) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `precio_compra` decimal(10,2) DEFAULT NULL,
  `precio_venta` decimal(10,2) DEFAULT NULL,
  `stock` int(100) DEFAULT NULL,
  `stock_minimo` int(100) DEFAULT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `lote` varchar(50) DEFAULT NULL,
  `registro_sanitario` varchar(50) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `id_provedor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_producto`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `stock`, `stock_minimo`, `fecha_vencimiento`, `lote`, `registro_sanitario`, `id_categoria`, `id_provedor`) VALUES
(5001, 'Acetaminofén', 'Tabletas 500mg', 1200.00, 2000.00, 100, 20, '2027-06-30', 'LOT001', 'RS1001', 2001, 4001),
(5002, 'Vitamina C', 'Tabletas 500mg', 3500.00, 5000.00, 80, 15, '2027-09-15', 'LOT002', 'RS1002', 2002, 4002),
(5003, 'Jabón Antibacterial', 'Higiene personal', 2500.00, 4000.00, 60, 10, '2028-01-10', 'LOT003', 'RS1003', 2003, 4003),
(5004, 'Lentes de Lectura', 'Graduación +2.0', 18000.00, 25000.00, 30, 5, '2029-01-01', 'LOT004', 'RS1004', 2004, 4004),
(5005, 'Venda Elástica', '5 metros', 5000.00, 7500.00, 50, 10, '2028-05-20', 'LOT005', 'RS1005', 2005, 4005),
(5006, 'Crema Hidratante', 'Crema corporal', 6500.00, 9500.00, 45, 10, '2028-07-25', 'LOT006', 'RS1006', 2006, 4006),
(5007, 'Ibuprofeno', 'Tabletas 400mg', 1800.00, 3000.00, 90, 20, '2027-08-12', 'LOT007', 'RS1007', 2007, 4007),
(5008, 'Amoxicilina', 'Capsulas 500mg', 4500.00, 7000.00, 40, 10, '2027-10-10', 'LOT008', 'RS1008', 2008, 4008),
(5009, 'Sal de Frutas', 'Sobres', 1200.00, 2200.00, 65, 15, '2028-02-14', 'LOT009', 'RS1009', 2009, 4009),
(5010, 'Antigripal', 'Tabletas', 3000.00, 5000.00, 55, 12, '2027-09-30', 'LOT010', 'RS1010', 2010, 4010),
(5011, 'Crema Dental', 'Tubo 100ml', 3500.00, 5500.00, 70, 15, '2028-04-20', 'LOT011', 'RS1011', 2011, 4011),
(5012, 'Pañales Bebé', 'Paquete x20', 18000.00, 25000.00, 35, 8, '2028-08-15', 'LOT012', 'RS1012', 2012, 4012),
(5013, 'Protector Solar', 'FPS 50', 22000.00, 30000.00, 25, 5, '2029-02-20', 'LOT013', 'RS1013', 2013, 4013),
(5014, 'Shampoo', 'Frasco 400ml', 9000.00, 13000.00, 50, 10, '2028-06-18', 'LOT014', 'RS1014', 2014, 4014),
(5015, 'Labial', 'Producto cosmético', 6000.00, 9000.00, 40, 8, '2029-01-15', 'LOT015', 'RS1015', 2015, 4015),
(5016, 'Termómetro Digital', 'Medición corporal', 12000.00, 18000.00, 20, 5, '2029-05-10', 'LOT016', 'RS1016', 2016, 4016),
(5017, 'Gel Antibacterial', 'Frasco 250ml', 4500.00, 7000.00, 80, 15, '2028-09-12', 'LOT017', 'RS1017', 2017, 4017),
(5018, 'Té Manzanilla', 'Caja x20', 5000.00, 8000.00, 60, 10, '2028-11-01', 'LOT018', 'RS1018', 2018, 4018),
(5019, 'Multivitamínico', 'Tabletas x30', 10000.00, 15000.00, 46, 10, '2027-12-20', 'LOT019', 'RS1019', 2019, 4019),
(5020, 'Tensiómetro', 'Equipo manual', 35000.00, 48000.00, 15, 3, '2029-06-05', 'LOT020', 'RS1020', 2020, 4020),
(5021, 'Gasas Estériles', 'Paquete x10', 3000.00, 5000.00, 101, 20, '2029-03-15', 'LOT021', 'RS1021', 2021, 4021),
(5022, 'Rodillera Elástica', 'Soporte deportivo', 14000.00, 20000.00, 25, 5, '2029-07-10', 'LOT022', 'RS1022', 2022, 4022),
(5023, 'Preservativos', 'Caja x3', 5000.00, 8000.00, 50, 10, '2029-04-10', 'LOT023', 'RS1023', 2023, 4023),
(5024, 'Repelente', 'Frasco 120ml', 7000.00, 10000.00, 40, 8, '2028-10-20', 'LOT024', 'RS1024', 2024, 4024),
(5025, 'Suplemento Nutricional', 'Polvo 500g', 15000.00, 22000.00, 30, 5, '2028-12-15', 'LOT025', 'RS1025', 2025, 4025),
(5026, 'Ibuprofeno 400mg', 'Tabletas para dolor', 2500.00, 4000.00, 8, 15, '2027-05-20', 'LOT026', 'RS1026', 2001, 4026),
(5027, 'Acetaminofén 650mg', 'Tabletas', 1500.00, 2500.00, 60, 15, '2028-03-15', 'LOT027', 'RS1027', 2001, 4027),
(5028, 'Vitamina D', 'Cápsulas', 4000.00, 6500.00, 4, 15, '2026-10-15', 'LOT028', 'RS1028', 2002, 4028),
(5029, 'Vitamina B12', 'Tabletas', 3500.00, 6000.00, 50, 10, '2028-02-10', 'LOT029', 'RS1029', 2002, 4029),
(5030, 'Alcohol Antiséptico', 'Frasco 500ml', 3000.00, 5000.00, 9, 15, '2027-08-20', 'LOT030', 'RS1030', 2003, 4030),
(5031, 'Gel Antibacterial', 'Frasco 250ml', 2500.00, 4500.00, 45, 10, '2028-01-15', 'LOT031', 'RS1031', 2003, 4031),
(5032, 'Gotas Lubricantes', 'Gotas oculares', 6000.00, 9500.00, 7, 10, '2026-09-20', 'LOT032', 'RS1032', 2004, 4032),
(5033, 'Lentes Lectura +1.5', 'Lentes ópticos', 16000.00, 23000.00, 26, 5, '2029-05-10', 'LOT033', 'RS1033', 2004, 4033),
(5034, 'Gasas Estériles', 'Paquete x10', 3500.00, 6000.00, 10, 20, '2027-11-10', 'LOT034', 'RS1034', 2005, 4034),
(5035, 'Curitas', 'Caja x20', 2000.00, 3500.00, 55, 10, '2028-04-20', 'LOT035', 'RS1035', 2005, 4035),
(5036, 'Naproxeno', 'Tabletas 250mg', 3000.00, 5000.00, 5, 15, '2026-11-10', 'LOT036', 'RS1036', 2001, 4036),
(5037, 'Multivitamínico', 'Tabletas', 5000.00, 8000.00, 35, 10, '2028-06-15', 'LOT037', 'RS1037', 2002, 4037),
(5038, 'Shampoo Medicinal', 'Tratamiento capilar', 7000.00, 11000.00, 8, 10, '2026-10-05', 'LOT038', 'RS1038', 2003, 4038),
(5039, 'Lentes Lectura +2.5', 'Lentes ópticos', 18000.00, 26000.00, 20, 5, '2029-02-15', 'LOT039', 'RS1039', 2004, 4039),
(5040, 'Vendas de Gasa', 'Paquete x5', 4500.00, 7000.00, 12, 15, '2027-09-20', 'LOT040', 'RS1040', 2005, 4040),
(5041, 'Diclofenaco', 'Tabletas 50mg', 3000.00, 5500.00, 7, 12, '2026-09-30', 'LOT041', 'RS1041', 2001, 4041),
(5042, 'Vitamina C 1000mg', 'Tabletas', 4500.00, 7000.00, 41, 10, '2028-07-10', 'LOT042', 'RS1042', 2002, 4042),
(5043, 'Jabón Medicinal', 'Jabón dermatológico', 3500.00, 6000.00, 9, 15, '2026-10-20', 'LOT043', 'RS1043', 2003, 4043),
(5044, 'Lentes Lectura +3.0', 'Lentes ópticos', 19000.00, 28000.00, 18, 5, '2029-03-15', 'LOT044', 'RS1044', 2004, 4044),
(5045, 'Termómetro Digital', 'Termómetro médico', 12000.00, 18000.00, 6, 10, '2028-08-10', 'LOT045', 'RS1045', 2005, 4045),
(1234565432, 'mistolin', 'sirve para limpiar los pisos', 15000.00, 20000.00, 0, 2, NULL, '15', 'no hay', 2004, 4038);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id_provedor` int(50) NOT NULL,
  `nombre_empre` varchar(50) DEFAULT NULL,
  `NIT` varchar(50) DEFAULT NULL,
  `telefono` int(50) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id_provedor`, `nombre_empre`, `NIT`, `telefono`, `correo`, `direccion`) VALUES
(4001, 'Laboratorios Bayer', '900111111', 2147483647, 'ventas@bayer.com', 'Bogotá'),
(4002, 'Genfar', '900222222', 2147483647, 'contacto@genfar.com', 'Cali'),
(4003, 'MK Medic', '900333333', 2147483647, 'info@mkmedic.com', 'Medellín'),
(4004, 'OptiVision', '900444444', 2147483647, 'ventas@optivision.com', 'Barranquilla'),
(4005, 'TecnoSalud', '900555555', 2147483647, 'contacto@tecnosalud.com', 'Bucaramanga'),
(4006, 'FarmaCol', '900666666', 2147483647, 'ventas@farmacol.com', 'Bogotá'),
(4007, 'Medifarma', '900777777', 2147483647, 'contacto@medifarma.com', 'Cali'),
(4008, 'Salud Plus', '900888888', 2147483647, 'ventas@saludplus.com', 'Medellín'),
(4009, 'BioMedic', '900999999', 2147483647, 'info@biomedic.com', 'Cúcuta'),
(4010, 'FarmaVida', '901000000', 2147483647, 'ventas@farmavida.com', 'Bogotá'),
(4011, 'Laboratorios ABC', '901111111', 2147483647, 'contacto@lababc.com', 'Cali'),
(4012, 'Medical Care', '901222222', 2147483647, 'ventas@medicalcare.com', 'Medellín'),
(4013, 'ProSalud', '901333333', 2147483647, 'info@prosalud.com', 'Cúcuta'),
(4014, 'VitalFarma', '901444444', 2147483647, 'ventas@vitalfarma.com', 'Bogotá'),
(4015, 'Farmaceutica Norte', '901555555', 2147483647, 'contacto@farmnorte.com', 'Cúcuta'),
(4016, 'MedSupply', '901666666', 2147483647, 'ventas@medsupply.com', 'Cali'),
(4017, 'NovaMed', '901777777', 2147483647, 'info@novamed.com', 'Medellín'),
(4018, 'Salud Integral', '901888888', 2147483647, 'ventas@saludintegral.com', 'Bogotá'),
(4019, 'Farma Express', '901999999', 2147483647, 'contacto@farmaexpress.com', 'Cúcuta'),
(4020, 'Medical Solutions', '902000000', 2147483647, 'ventas@medicalsolutions.com', 'Cali'),
(4021, 'Distribuciones Salud', '902111111', 2147483647, 'info@disalud.com', 'Medellín'),
(4022, 'Optica Central', '902222222', 2147483647, 'ventas@opticacentral.com', 'Bogotá'),
(4023, 'Farmacia Nacional', '902333333', 2147483647, 'contacto@farmnacional.com', 'Cúcuta'),
(4024, 'BioSalud', '902444444', 2147483647, 'ventas@biosalud.com', 'Cali'),
(4025, 'Medicina Total', '902555555', 2147483647, 'info@medicinatotal.com', 'Medellín'),
(4026, 'Farmacéutica Norte', '900666001', 315600001, 'ventas26@farmnorte.com', 'Cúcuta'),
(4027, 'Salud Total', '900666002', 315600002, 'ventas27@saludtotal.com', 'Bogotá'),
(4028, 'Medicamentos Andinos', '900666003', 315600003, 'contacto28@medandinos.com', 'Medellín'),
(4029, 'BioPharma Colombia', '900666004', 315600004, 'ventas29@biopharma.com', 'Cali'),
(4030, 'Distribuciones Salud', '900666005', 315600005, 'info30@distsalud.com', 'Bucaramanga'),
(4031, 'Medic Plus', '900666006', 315600006, 'ventas31@medicplus.com', 'Bogotá'),
(4032, 'Farmasalud', '900666007', 315600007, 'contacto32@farmasalud.com', 'Cúcuta'),
(4033, 'Vital Pharma', '900666008', 315600008, 'ventas33@vitalpharma.com', 'Medellín'),
(4034, 'Colombia Medical', '900666009', 315600009, 'info34@colmedical.com', 'Cali'),
(4035, 'Insumos del Norte', '900666010', 315600010, 'ventas35@insumosnorte.com', 'Cúcuta'),
(4036, 'ProSalud', '900666011', 315600011, 'contacto36@prosalud.com', 'Bogotá'),
(4037, 'Medical Express', '900666012', 315600012, 'ventas37@medicalexpress.com', 'Cali'),
(4038, 'Farmacia Mayorista', '900666013', 315600013, 'info38@farmmayorista.com', 'Medellín'),
(4039, 'BioMedic', '900666014', 315600014, 'ventas39@biomedic.com', 'Bogotá'),
(4040, 'Salud y Vida', '900666015', 315600015, 'contacto40@saludyvida.com', 'Cúcuta'),
(4041, 'OptiSalud', '900666016', 315600016, 'ventas41@optisalud.com', 'Barranquilla'),
(4042, 'MedSupply', '900666017', 315600017, 'info42@medsupply.com', 'Cali'),
(4043, 'Farmacol Norte', '900666018', 315600018, 'ventas43@farmacol.com', 'Cúcuta'),
(4044, 'Distribuciones Médicas', '900666019', 315600019, 'contacto44@dismedicas.com', 'Bogotá'),
(4045, 'TecnoMedical', '900666020', 315600020, 'ventas45@tecnomedical.com', 'Bucaramanga');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitud_de_registros`
--

CREATE TABLE `solicitud_de_registros` (
  `id_solicitud` bigint(20) NOT NULL,
  `Dni_usu` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` bigint(20) NOT NULL,
  `contrasena_hash` varchar(255) NOT NULL,
  `foto_temporal` varchar(255) DEFAULT NULL,
  `estado` enum('Pendiente','Aprobada','Rechazada') NOT NULL DEFAULT 'Pendiente',
  `fecha_solicitud` timestamp NOT NULL DEFAULT current_timestamp(),
  `revisado_por` varchar(100) DEFAULT NULL,
  `fecha_revision` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `solicitud_de_registros`
--

INSERT INTO `solicitud_de_registros` (`id_solicitud`, `Dni_usu`, `Nombre`, `apellido`, `correo`, `telefono`, `contrasena_hash`, `foto_temporal`, `estado`, `fecha_solicitud`, `revisado_por`, `fecha_revision`) VALUES
(1, 213456789, 'jairo', 'elberth', 'jairo@gmail.com', 3135876, 'pbkdf2_sha256$260000$DGO8XYygxD7Tpxa64bd0Zg$YcSkCTNQuKNVOuhuCtcqzfz7ejmOMISGx-ojrb7jaFA', 'H:\\Downloads\\drogueria_don_marcos\\profile_photos\\request_213456789.jpg', 'Aprobada', '2026-10-16 13:25:30', 'Dorian', '2026-10-16 08:26:34');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `Dni_usu` int(50) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` bigint(20) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `contrasena` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`Dni_usu`, `Nombre`, `apellido`, `correo`, `telefono`, `rol`, `contrasena`) VALUES
(3001, 'Andrés', 'Martínez', 'andres@drogueria.com', 310000001, 'Administrador', 'admin123'),
(3002, 'Laura', 'Rojas', 'laura@drogueria.com', 310000002, 'Empleado', 'emple123'),
(3003, 'Camila', 'Díaz', 'camila@drogueria.com', 310000003, 'Enfermera', 'enfer123'),
(3004, 'Jorge', 'Castro', 'jorge@drogueria.com', 310000004, 'Empleado', 'jorge123'),
(3005, 'Paula', 'López', 'paula@drogueria.com', 310000005, 'Administrador', 'paula123'),
(3006, 'Daniel', 'Vargas', 'daniel@drogueria.com', 310000006, 'Empleado', 'daniel123'),
(3007, 'Natalia', 'Sánchez', 'natalia@drogueria.com', 310000007, 'Enfermera', 'natalia123'),
(3008, 'Miguel', 'Ortiz', 'miguel@drogueria.com', 310000008, 'Empleado', 'miguel123'),
(3009, 'Valeria', 'Silva', 'valeria@drogueria.com', 310000009, 'Administrador', 'valeria123'),
(3010, 'Santiago', 'Morales', 'santiago@drogueria.com', 310000010, 'Empleado', 'santi123'),
(3011, 'Gabriela', 'Cárdenas', 'gabriela@drogueria.com', 310000011, 'Enfermera', 'gabriela123'),
(3012, 'Felipe', 'Vega', 'felipe@drogueria.com', 310000012, 'Empleado', 'felipe123'),
(3013, 'Mariana', 'Navarro', 'mariana@drogueria.com', 310000013, 'Administrador', 'mariana123'),
(3014, 'David', 'Pineda', 'david@drogueria.com', 310000014, 'Empleado', 'david123'),
(3015, 'Sara', 'Molina', 'sara@drogueria.com', 310000015, 'Enfermera', 'sara123'),
(3016, 'Kevin', 'Guerrero', 'kevin@drogueria.com', 310000016, 'Empleado', 'kevin123'),
(3017, 'Juliana', 'Mendoza', 'juliana@drogueria.com', 310000017, 'Administrador', 'juliana123'),
(3018, 'Nicolás', 'Ramírez', 'nicolas@drogueria.com', 310000018, 'Empleado', 'nico123'),
(3019, 'Laura', 'Torres', 'laura@drogueria.com', 310000019, 'Enfermera', 'laura123'),
(3020, 'Esteban', 'Gómez', 'esteban@drogueria.com', 310000020, 'Empleado', 'esteban123'),
(3021, 'Carolina', 'Pérez', 'carolina@drogueria.com', 310000021, 'Administrador', 'caro123'),
(3022, 'Tomás', 'Rojas', 'tomas@drogueria.com', 310000022, 'Empleado', 'tomas123'),
(3023, 'Andrea', 'Díaz', 'andrea@drogueria.com', 310000023, 'Enfermera', 'andrea123'),
(3024, 'Ricardo', 'Castro', 'ricardo@drogueria.com', 310000024, 'Empleado', 'ricardo123'),
(3025, 'Mónica', 'López', 'monica@drogueria.com', 310000025, 'Administrador', 'monica123'),
(3026, 'Ricardo', 'Gómez', 'ricardo2@drogueria.com', 310600001, 'Empleado', 'ricardo123'),
(3027, 'Diana', 'Pérez', 'diana2@drogueria.com', 310600002, 'Empleado', 'diana123'),
(3028, 'Felipe', 'Rojas', 'felipe2@drogueria.com', 310600003, 'Empleado', 'felipe123'),
(3029, 'Andrea', 'Torres', 'andrea2@drogueria.com', 310600004, 'Enfermera', 'andrea123'),
(3030, 'Mauricio', 'Díaz', 'mauricio2@drogueria.com', 310600005, 'Empleado', 'mauricio123'),
(3031, 'Carolina', 'Moreno', 'carolina2@drogueria.com', 310600006, 'Enfermera', 'carolina123'),
(3032, 'Esteban', 'López', 'esteban2@drogueria.com', 310600007, 'Empleado', 'esteban123'),
(3033, 'Juliana', 'Castro', 'juliana2@drogueria.com', 310600008, 'Empleado', 'juliana123'),
(3034, 'Santiago', 'Ramírez', 'santiago2@drogueria.com', 310600009, 'Administrador', 'santiago123'),
(3035, 'Paola', 'Hernández', 'paola2@drogueria.com', 310600010, 'Empleado', 'paola123'),
(3036, 'Cristian', 'Vargas', 'cristian2@drogueria.com', 310600011, 'Empleado', 'cristian123'),
(3037, 'Natalia', 'Gómez', 'natalia2@drogueria.com', 310600012, 'Enfermera', 'natalia123'),
(3038, 'Andrés', 'Castro', 'andres2@drogueria.com', 310600013, 'Empleado', 'andres123'),
(3039, 'Marcela', 'Rojas', 'marcela2@drogueria.com', 310600014, 'Empleado', 'marcela123'),
(3040, 'Jorge', 'Moreno', 'jorge2@drogueria.com', 310600015, 'Administrador', 'jorge123'),
(3041, 'Claudia', 'Torres', 'claudia2@drogueria.com', 310600016, 'Empleado', 'claudia123'),
(3042, 'Kevin', 'Martínez', 'kevin2@drogueria.com', 310600017, 'Empleado', 'kevin123'),
(3043, 'Valeria', 'López', 'valeria2@drogueria.com', 310600018, 'Enfermera', 'valeria123'),
(3044, 'Oscar', 'Ramírez', 'oscar2@drogueria.com', 310600019, 'Empleado', 'oscar123'),
(3045, 'Mónica', 'Díaz', 'monica2@drogueria.com', 310600020, 'Empleado', 'monica123'),
(123456789, 'jairo', 'elverg', 'jario@gmail.com', 320581721, 'Empleado', 'pbkdf2_sha256$260000$I3ZduVnE2QkZZKzpzj_PuA$FolgOJNo5bap9_6-VsPlRkhWCLvunRIwn7BWRdQKCMU'),
(213456789, 'jairo', 'elberth', 'jairo@gmail.com', 3135876, 'Empleado', 'pbkdf2_sha256$260000$DGO8XYygxD7Tpxa64bd0Zg$YcSkCTNQuKNVOuhuCtcqzfz7ejmOMISGx-ojrb7jaFA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `id_venta` int(50) NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `dni_client` int(11) DEFAULT NULL,
  `Dni_usu` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `venta`
--

INSERT INTO `venta` (`id_venta`, `fecha`, `total`, `metodo_pago`, `dni_client`, `Dni_usu`) VALUES
(7001, '2026-07-01', 25500.00, 'Efectivo', 1001, 3002),
(7002, '2026-07-02', 12200.00, 'Nequi', 1002, 3004),
(7003, '2026-07-03', 13200.00, 'Tarjeta', 1003, 3002),
(7004, '2026-07-04', 19500.00, 'Efectivo', 1004, 3004),
(7005, '2026-07-05', 37000.00, 'Transferencia', 1005, 3002),
(7006, '2026-07-06', 19700.00, 'Nequi', 1006, 3006),
(7007, '2026-07-07', 11200.00, 'Efectivo', 1007, 3008),
(7008, '2026-07-08', 17000.00, 'Tarjeta', 1008, 3006),
(7009, '2026-07-09', 20200.00, 'Transferencia', 1009, 3008),
(7010, '2026-07-10', 27000.00, 'Efectivo', 1010, 3006),
(7011, '2026-07-11', 12700.00, 'Nequi', 1011, 3010),
(7012, '2026-07-12', 37000.00, 'Tarjeta', 1012, 3012),
(7013, '2026-07-13', 42000.00, 'Efectivo', 1013, 3014),
(7014, '2026-07-14', 23000.00, 'Transferencia', 1014, 3012),
(7015, '2026-07-15', 19000.00, 'Nequi', 1015, 3014),
(7016, '2026-07-16', 28000.00, 'Efectivo', 1016, 3016),
(7017, '2026-07-17', 17000.00, 'Tarjeta', 1017, 3018),
(7018, '2026-07-18', 18000.00, 'Transferencia', 1018, 3020),
(7019, '2026-07-19', 25000.00, 'Efectivo', 1019, 3016),
(7020, '2026-07-20', 58000.00, 'Nequi', 1020, 3018),
(7021, '2026-07-21', 12200.00, 'Tarjeta', 1021, 3020),
(7022, '2026-07-22', 30000.00, 'Efectivo', 1022, 3022),
(7023, '2026-07-23', 18000.00, 'Transferencia', 1023, 3024),
(7024, '2026-07-24', 20000.00, 'Nequi', 1024, 3022),
(7025, '2026-07-25', 32000.00, 'Efectivo', 1025, 3024),
(7026, '2026-08-01', 28500.00, 'Efectivo', 1026, 3026),
(7027, '2026-08-02', 32000.00, 'Nequi', 1027, 3027),
(7028, '2026-08-03', 26500.00, 'Tarjeta', 1028, 3028),
(7029, '2026-08-04', 41000.00, 'Efectivo', 1029, 3030),
(7030, '2026-08-05', 30000.00, 'Transferencia', 1030, 3032),
(7031, '2026-08-06', 35500.00, 'Nequi', 1031, 3033),
(7032, '2026-08-07', 48500.00, 'Efectivo', 1032, 3035),
(7033, '2026-08-08', 48500.00, 'Tarjeta', 1033, 3036),
(7034, '2026-08-09', 36500.00, 'Efectivo', 1034, 3038),
(7035, '2026-08-10', 36000.00, 'Nequi', 1035, 3039),
(7036, '2026-08-11', 28000.00, 'Efectivo', 1036, 3041),
(7037, '2026-08-12', 43000.00, 'Tarjeta', 1037, 3042),
(7038, '2026-08-13', 43000.00, 'Transferencia', 1038, 3044),
(7039, '2026-08-14', 41500.00, 'Efectivo', 1039, 3026),
(7040, '2026-08-15', 47500.00, 'Nequi', 1040, 3027),
(7041, '2026-08-16', 36000.00, 'Efectivo', 1041, 3028),
(7042, '2026-08-17', 36500.00, 'Tarjeta', 1042, 3030),
(7043, '2026-08-18', 42500.00, 'Efectivo', 1043, 3032),
(7044, '2026-08-19', 21500.00, 'Transferencia', 1044, 3035),
(7045, '2026-08-20', 35000.00, 'Nequi', 1045, 3036),
(7046, '2026-10-16', 19500.00, 'Efectivo', NULL, NULL),
(7047, '2026-10-16', 200000.00, 'Efectivo', NULL, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `citas_opticas`
--
ALTER TABLE `citas_opticas`
  ADD PRIMARY KEY (`id_citas`),
  ADD KEY `dni_client` (`dni_client`),
  ADD KEY `Dni_usu` (`Dni_usu`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`dni_client`);

--
-- Indices de la tabla `compra`
--
ALTER TABLE `compra`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `id_provedor` (`id_provedor`),
  ADD KEY `Dni_usu` (`Dni_usu`);

--
-- Indices de la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_producto` (`id_producto`),
  ADD KEY `id_compra` (`id_compra`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `movimiento_inventario`
--
ALTER TABLE `movimiento_inventario`
  ADD PRIMARY KEY (`id_movimiento`),
  ADD KEY `id_producto` (`id_producto`),
  ADD KEY `Dni_usu` (`Dni_usu`),
  ADD KEY `idx_movimiento_compra` (`id_compra`),
  ADD KEY `idx_movimiento_venta` (`id_venta`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_categoria` (`id_categoria`),
  ADD KEY `id_provedor` (`id_provedor`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id_provedor`);

--
-- Indices de la tabla `solicitud_de_registros`
--
ALTER TABLE `solicitud_de_registros`
  ADD PRIMARY KEY (`id_solicitud`),
  ADD KEY `idx_solicitud_estado_fecha` (`estado`,`fecha_solicitud`),
  ADD KEY `idx_solicitud_id` (`Dni_usu`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`Dni_usu`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `dni_client` (`dni_client`),
  ADD KEY `Dni_usu` (`Dni_usu`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `compra`
--
ALTER TABLE `compra`
  MODIFY `id_compra` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9047;

--
-- AUTO_INCREMENT de la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  MODIFY `id_detalle` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10051;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11103;

--
-- AUTO_INCREMENT de la tabla `movimiento_inventario`
--
ALTER TABLE `movimiento_inventario`
  MODIFY `id_movimiento` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8053;

--
-- AUTO_INCREMENT de la tabla `solicitud_de_registros`
--
ALTER TABLE `solicitud_de_registros`
  MODIFY `id_solicitud` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id_venta` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7048;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas_opticas`
--
ALTER TABLE `citas_opticas`
  ADD CONSTRAINT `citas_opticas_ibfk_1` FOREIGN KEY (`dni_client`) REFERENCES `cliente` (`dni_client`),
  ADD CONSTRAINT `citas_opticas_ibfk_2` FOREIGN KEY (`Dni_usu`) REFERENCES `usuario` (`Dni_usu`);

--
-- Filtros para la tabla `compra`
--
ALTER TABLE `compra`
  ADD CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`id_provedor`) REFERENCES `proveedor` (`id_provedor`),
  ADD CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`Dni_usu`) REFERENCES `usuario` (`Dni_usu`);

--
-- Filtros para la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  ADD CONSTRAINT `detalle_compra_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`),
  ADD CONSTRAINT `detalle_compra_ibfk_2` FOREIGN KEY (`id_compra`) REFERENCES `compra` (`id_compra`);

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id_venta`),
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

--
-- Filtros para la tabla `movimiento_inventario`
--
ALTER TABLE `movimiento_inventario`
  ADD CONSTRAINT `fk_movimiento_compra` FOREIGN KEY (`id_compra`) REFERENCES `compra` (`id_compra`),
  ADD CONSTRAINT `fk_movimiento_venta` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id_venta`),
  ADD CONSTRAINT `movimiento_inventario_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`),
  ADD CONSTRAINT `movimiento_inventario_ibfk_2` FOREIGN KEY (`Dni_usu`) REFERENCES `usuario` (`Dni_usu`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categoria` (`id_categoria`),
  ADD CONSTRAINT `producto_ibfk_2` FOREIGN KEY (`id_provedor`) REFERENCES `proveedor` (`id_provedor`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`dni_client`) REFERENCES `cliente` (`dni_client`),
  ADD CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`Dni_usu`) REFERENCES `usuario` (`Dni_usu`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
