-- Script con definición de la tabla `usuario` y ALTER para la columna de contraseña
-- Úsalo en phpMyAdmin o en el cliente MySQL para crear/ajustar la tabla.

-- Crear la tabla si no existe (opcional)
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Si la tabla ya existe y solo quieres ampliar la columna de contraseña:
ALTER TABLE `usuario` MODIFY COLUMN `contraseña` VARCHAR(255) NOT NULL;
