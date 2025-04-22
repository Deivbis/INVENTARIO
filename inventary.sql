-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-04-2025 a las 03:52:42
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
-- Base de datos: `inventary`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id_categoria`, `nombre`, `descripcion`, `estado`, `fecha_registro`) VALUES
(6, 'saludable', 'ayudar', 'activo', '2025-04-14 23:16:52'),
(7, 'grasoso', 'perjudicial', 'activo', '2025-04-16 02:09:11'),
(8, 'viajes', 'motos,carros', 'activo', '2025-04-17 23:15:22'),
(9, 'salud', 'cuidado de salud', 'inactivo', '2025-04-21 03:53:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(11) UNSIGNED NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'activo',
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre`, `telefono`, `correo`, `estado`, `fecha_registro`) VALUES
(1, 'sofia', '23456789809', 'sofia@gmail.com', 'activo', '2025-04-16 14:38:42'),
(2, 'maria', '3045906678', 'marianita@gmail.com', 'activo', '2025-04-18 13:12:56'),
(3, 'duba', '3045905678', 'dubancito@gmail.com', 'activo', '2025-04-18 21:02:04'),
(4, 'daycar', '3097896545', 'campo130@gmail.com', 'activo', '2025-04-18 21:02:34'),
(5, 'mateo', '3456789876', 'mateo@gmail,com', 'activo', '2025-04-18 21:02:55'),
(6, 'deivis', '3045906758', 'deivis@gmail,com', 'activo', '2025-04-18 21:03:38'),
(7, 'lucia', '4680647456', 'lucita@gmail.com', 'activo', '2025-04-19 14:12:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id_detalle` int(11) NOT NULL,
  `id_venta` int(11) UNSIGNED NOT NULL,
  `id_producto` int(11) UNSIGNED NOT NULL,
  `cantidad` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT 'activo',
  `fecha_registro` datetime DEFAULT current_timestamp(),
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `total` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id_detalle`, `id_venta`, `id_producto`, `cantidad`, `estado`, `fecha_registro`, `precio_unitario`, `total`) VALUES
(14, 42, 12, 12, 'activo', '2025-04-17 13:44:14', 30000.00, 360000),
(15, 43, 12, 3, 'activo', '2025-04-17 14:14:11', 30000.00, 90000),
(16, 44, 12, 5, 'activo', '2025-04-17 14:42:56', 30000.00, 150000),
(17, 45, 12, 5, 'activo', '2025-04-17 15:03:48', 30000.00, 150000),
(18, 46, 13, 4, 'activo', '2025-04-17 15:05:42', 30000.00, 120000),
(19, 47, 14, 10, 'activo', '2025-04-17 15:09:29', 3000.00, 30000),
(20, 48, 13, 5, 'activo', '2025-04-17 15:11:30', 30000.00, 150000),
(21, 49, 12, 5, 'activo', '2025-04-17 15:20:22', 30000.00, 150000),
(22, 50, 14, 5, 'activo', '2025-04-17 15:44:45', 3000.00, 15000),
(23, 51, 15, 3, 'activo', '2025-04-17 15:47:13', 30000.00, 90000),
(24, 52, 12, 5, 'activo', '2025-04-17 18:12:46', 30000.00, 150000),
(25, 53, 13, 5, 'activo', '2025-04-17 18:16:11', 30000.00, 150000),
(27, 55, 14, 3, 'activo', '2025-04-17 20:02:28', 3000.00, 9000),
(28, 56, 14, 2, 'activo', '2025-04-17 22:52:16', 3000.00, 6000),
(29, 57, 11, 4, 'activo', '2025-04-17 23:18:05', 3000.00, 12000),
(30, 58, 12, 5, 'activo', '2025-04-18 13:09:31', 30000.00, 150000),
(31, 58, 13, 2, 'activo', '2025-04-18 13:09:31', 30000.00, 60000),
(32, 58, 14, 4, 'activo', '2025-04-18 13:09:31', 3000.00, 12000),
(33, 59, 14, 11, 'activo', '2025-04-18 13:14:09', 3000.00, 33000),
(34, 59, 16, 10, 'activo', '2025-04-18 13:14:09', 2000000.00, 20000000),
(35, 60, 11, 4, 'activo', '2025-04-18 15:41:50', 3000.00, 12000),
(36, 61, 11, 3, 'activo', '2025-04-19 14:15:50', 3000.00, 9000),
(37, 61, 12, 6, 'activo', '2025-04-19 14:15:50', 30000.00, 180000),
(38, 61, 15, 7, 'activo', '2025-04-19 14:15:51', 30000.00, 210000),
(39, 62, 13, 4, 'activo', '2025-04-20 22:22:41', 30000.00, 120000),
(40, 63, 17, 200, 'activo', '2025-04-20 22:58:12', 2000.00, 400000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos`
--

CREATE TABLE `movimientos` (
  `id` int(11) NOT NULL,
  `producto_id` int(11) UNSIGNED NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `motivo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimientos`
--

INSERT INTO `movimientos` (`id`, `producto_id`, `tipo`, `cantidad`, `fecha`, `motivo`) VALUES
(17, 16, '', 6, '2025-04-17 23:47:14', 'entrada'),
(18, 13, '', -5, '2025-04-17 23:47:22', 'salida'),
(19, 16, '', 4, '2025-04-18 00:08:14', 'entrada'),
(20, 16, '', -4, '2025-04-18 00:08:21', 'salida'),
(21, 14, '', 3, '2025-04-17 20:02:28', 'Venta'),
(22, 14, '', 2, '2025-04-17 22:52:16', 'Venta'),
(23, 11, '', 4, '2025-04-17 23:18:05', 'Venta'),
(24, 12, '', 5, '2025-04-18 13:09:31', 'Venta'),
(25, 13, '', 2, '2025-04-18 13:09:31', 'Venta'),
(26, 14, '', 4, '2025-04-18 13:09:31', 'Venta'),
(27, 14, '', 11, '2025-04-18 13:14:09', 'Venta'),
(28, 16, '', 10, '2025-04-18 13:14:09', 'Venta'),
(29, 11, '', 4, '2025-04-18 15:41:50', 'Venta'),
(30, 11, '', 3, '2025-04-19 14:15:50', 'Venta'),
(31, 12, '', 6, '2025-04-19 14:15:51', 'Venta'),
(32, 15, '', 7, '2025-04-19 14:15:51', 'Venta'),
(33, 21, '', -20, '2025-04-21 03:09:13', 'salida'),
(34, 21, '', 20, '2025-04-21 03:10:19', 'entrada'),
(35, 21, '', -20, '2025-04-21 03:13:10', 'salida'),
(36, 21, '', 0, '2025-04-21 03:13:12', 'salida'),
(37, 21, '', 20, '2025-04-21 03:13:24', 'entrada'),
(38, 21, '', -20, '2025-04-21 03:17:21', 'salida'),
(39, 21, '', -20, '2025-04-21 03:19:17', 'salida'),
(40, 21, '', 29, '2025-04-21 03:21:08', 'entrada'),
(41, 21, '', 0, '2025-04-21 03:21:17', 'salida'),
(42, 21, '', -49, '2025-04-21 03:21:29', 'salida'),
(43, 21, '', 50, '2025-04-21 03:21:37', 'entrada'),
(44, 13, '', 4, '2025-04-20 22:22:41', 'Venta'),
(45, 21, '', -30, '2025-04-21 03:22:56', 'salida'),
(46, 21, '', -230, '2025-04-21 03:32:47', 'salida'),
(47, 21, '', -30, '2025-04-21 03:32:47', 'Salida'),
(48, 21, '', -260, '2025-04-21 03:32:55', 'entrada'),
(49, 21, '', 30, '2025-04-21 03:32:55', 'Entrada'),
(50, 20, '', -60, '2025-04-21 03:38:07', 'entrada'),
(51, 20, '', 20, '2025-04-21 03:38:07', 'Entrada'),
(52, 20, '', -50, '2025-04-21 03:38:15', 'salida'),
(53, 20, '', -10, '2025-04-21 03:38:15', 'Salida'),
(54, 21, '', -290, '2025-04-21 03:41:37', 'entrada'),
(55, 21, '', 30, '2025-04-21 03:41:37', 'Entrada'),
(56, 17, '', 200, '2025-04-20 22:58:12', 'Venta'),
(57, 21, '', -250, '2025-04-21 03:59:21', 'salida'),
(58, 21, '', -40, '2025-04-21 03:59:21', 'Salida'),
(59, 11, '', -11, '2025-04-21 03:59:38', 'entrada'),
(60, 11, '', 7, '2025-04-21 03:59:38', 'Entrada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id_permiso` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` int(10) UNSIGNED NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` double NOT NULL,
  `categoria` int(11) NOT NULL,
  `cantidad_stock` int(11) NOT NULL,
  `stock_minimo` int(11) NOT NULL,
  `id_proveedor` int(10) UNSIGNED NOT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `nombre`, `precio`, `categoria`, `cantidad_stock`, `stock_minimo`, `id_proveedor`, `estado`, `fecha_registro`) VALUES
(11, 'sall', 3000, 6, 11, 10, 6, 'activo', '2025-04-14 19:05:46'),
(12, 'carro', 30000, 6, 19, 5, 6, 'activo', '2025-04-15 20:16:05'),
(13, 'silla', 30000, 6, 24, 15, 6, 'activo', '2025-04-15 20:16:41'),
(14, 'carro', 3000, 7, 100, 100, 7, 'activo', '2025-04-15 21:31:04'),
(15, 'carro', 30000, 6, 203, 200, 7, 'inactivo', '2025-04-15 21:31:29'),
(16, 'moto', 2000000, 7, 260, 100, 6, 'inactivo', '2025-04-17 18:14:34'),
(17, 'arroz', 2000, 8, 100, 50, 8, 'activo', '2025-04-18 21:04:36'),
(18, 'motor', 3000000, 7, 150, 20, 6, 'activo', '2025-04-18 21:05:05'),
(19, 'dado', 3000, 6, 200, 50, 6, 'activo', '2025-04-18 21:05:29'),
(20, 'carne', 3000, 7, 50, 10, 6, 'activo', '2025-04-18 21:06:11'),
(21, 'carpa', 2000, 8, 250, 100, 6, 'activo', '2025-04-18 21:06:35');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proovedores`
--

CREATE TABLE `proovedores` (
  `id` int(10) UNSIGNED NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proovedores`
--

INSERT INTO `proovedores` (`id`, `nombre`, `estado`, `fecha_registro`) VALUES
(6, 'cash', 'activo', '2025-04-14 18:16:16'),
(7, 'rol', 'activo', '2025-04-15 21:06:50'),
(8, 'mecanicas', 'inactivo', '2025-04-17 18:16:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_usuarios`
--

CREATE TABLE `registro_usuarios` (
  `id_usuario` int(11) UNSIGNED NOT NULL,
  `USUARIO` varchar(100) NOT NULL,
  `CONTRASEÑA` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `id_rol` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro_usuarios`
--

INSERT INTO `registro_usuarios` (`id_usuario`, `USUARIO`, `CONTRASEÑA`, `Email`, `estado`, `fecha_registro`, `id_rol`) VALUES
(1, 'deivis', '$2b$12$xJC9RHx2b6UnFvx9AO/4kO2tZMv5k/RDjGm8AC42EFvBDYcagU3W2', 'deivisbariios@gmail.com', 'activo', '2025-04-16 00:00:00', 1),
(2, 'mateo', '$2b$12$IsjyKyMPw781QjwtAlWweewOtW4j82z9enMaxzHKfqhWRsPmcZdH2', 'mateo@gmail.com', 'activo', '2025-04-16 00:00:00', 2),
(3, 'daycar', '$2b$12$PyOCD8t4wJIAdmkQ7Otoh.B8Y1ADRBMFCSPK91emVUa0g/itzwwuG', 'daycar@gmail.com', 'activo', '2025-04-18 00:00:00', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre`, `descripcion`, `estado`, `fecha_registro`) VALUES
(1, 'admin', NULL, 'activo', '2025-04-09 20:08:53'),
(2, 'usuario', 'solo para usuarios', 'activo', '2025-04-13 16:58:37');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_permiso`
--

CREATE TABLE `rol_permiso` (
  `id_rol` int(11) NOT NULL,
  `id_permiso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` int(11) NOT NULL,
  `id_cliente` int(11) UNSIGNED NOT NULL,
  `cantidad_inicial` int(11) DEFAULT NULL,
  `movimiento` enum('venta') NOT NULL,
  `cantidad_actual` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `total` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `id_cliente`, `cantidad_inicial`, `movimiento`, `cantidad_actual`, `precio_unitario`, `estado`, `fecha_registro`, `total`) VALUES
(43, 1, 3, 'venta', 3, 30000.00, 'activo', '2025-04-17 14:14:11', 90000),
(44, 1, 5, 'venta', 5, 30000.00, 'activo', '2025-04-17 14:42:55', 150000),
(45, 1, 5, 'venta', 5, 30000.00, 'activo', '2025-04-17 15:03:48', 150000),
(46, 1, 4, 'venta', 4, 30000.00, 'activo', '2025-04-17 15:05:42', 120000),
(47, 1, 10, 'venta', 10, 3000.00, 'activo', '2025-04-17 15:09:29', 30000),
(48, 1, 5, 'venta', 5, 30000.00, 'activo', '2025-04-17 15:11:30', 150000),
(49, 1, 5, 'venta', 5, 30000.00, 'activo', '2025-04-17 15:20:22', 150000),
(50, 1, 5, 'venta', 5, 3000.00, 'activo', '2025-04-17 15:44:45', 15000),
(51, 1, 3, 'venta', 3, 30000.00, 'activo', '2025-04-17 15:47:13', 90000),
(52, 1, 5, 'venta', 5, 30000.00, 'activo', '2025-04-17 18:12:46', 150000),
(53, 1, 5, 'venta', 5, 30000.00, 'activo', '2025-04-17 18:16:11', 150000),
(54, 1, 5, 'venta', 5, 30000.00, 'activo', '2025-04-17 20:01:06', 150000),
(55, 1, 3, 'venta', 3, 3000.00, 'activo', '2025-04-17 20:02:28', 9000),
(56, 1, 2, 'venta', 2, 3000.00, 'activo', '2025-04-17 22:52:15', 6000),
(57, 1, 4, 'venta', 4, 3000.00, 'activo', '2025-04-17 23:18:05', 12000),
(58, 0, 11, 'venta', 11, 30000.00, 'activo', '2025-04-18 13:09:31', 222000),
(59, 2, 21, 'venta', 21, 3000.00, 'activo', '2025-04-18 13:14:09', 20033000),
(60, 2, 4, 'venta', 4, 3000.00, 'activo', '2025-04-18 15:41:50', 12000),
(61, 5, 16, 'venta', 16, 3000.00, 'activo', '2025-04-19 14:15:50', 399000),
(62, 3, 4, 'venta', 4, 30000.00, 'activo', '2025-04-20 22:22:41', 120000),
(63, 5, 200, 'venta', 200, 2000.00, 'activo', '2025-04-20 22:58:12', 400000);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `codigo` (`id_venta`,`id_producto`);

--
-- Indices de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id_permiso`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_proveedor` (`id_proveedor`),
  ADD KEY `categoria` (`categoria`);

--
-- Indices de la tabla `proovedores`
--
ALTER TABLE `proovedores`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `registro_usuarios`
--
ALTER TABLE `registro_usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `fk_roles` (`id_rol`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `rol_permiso`
--
ALTER TABLE `rol_permiso`
  ADD PRIMARY KEY (`id_rol`,`id_permiso`),
  ADD KEY `id_permiso` (`id_permiso`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id_permiso` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `proovedores`
--
ALTER TABLE `proovedores`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `registro_usuarios`
--
ALTER TABLE `registro_usuarios`
  MODIFY `id_usuario` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD CONSTRAINT `movimientos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proovedores` (`id`),
  ADD CONSTRAINT `producto_ibfk_2` FOREIGN KEY (`categoria`) REFERENCES `categoria` (`id_categoria`);

--
-- Filtros para la tabla `registro_usuarios`
--
ALTER TABLE `registro_usuarios`
  ADD CONSTRAINT `fk_roles` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`),
  ADD CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);

--
-- Filtros para la tabla `rol_permiso`
--
ALTER TABLE `rol_permiso`
  ADD CONSTRAINT `rol_permiso_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE CASCADE,
  ADD CONSTRAINT `rol_permiso_ibfk_2` FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id_permiso`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
