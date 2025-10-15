CREATE DATABASE IF NOT EXISTS crud_flask_python;
USE crud_flask_python;

CREATE TABLE `carros` (
  `id` int NOT NULL AUTO_INCREMENT,
  `marca` varchar(45) NOT NULL,
  `modelo` varchar(45) NOT NULL,
  `year` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  `puertas` varchar(45) NOT NULL,
  `favorito` varchar(45) NOT NULL,
  `foto` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `carros` (`id`, `marca`, `modelo`, `year`, `color`, `puertas`, `favorito`, `foto`) VALUES
(1, 'BMW', 'BMW X7', '2022', 'Gris', '4', 'Si', 'R5Q2IZSTU6BVDWL3CA9H.png'),
(2, 'Ford', 'CAMIONETA', '2022', 'Blanco', '4', 'Si', 'ZHKTJE319UCDIB6F7A_5.png'),
(3, 'Chevrolet', 'Onix Turbo', '2013', 'Blanco', '2', 'No', 'IMWSBJD4O1UCA97N_R0P.jpg'),
(7, 'Toyota', 'Avalon', '2018', 'Gris', '2', 'No', '4IQKOW_31NFYL7BU9TPM.png'),
(8, 'Chevrolet', 'Joy HB', '2015', 'Rojo', '4', 'Si', 'Z1UR8IQMVSE3JWDLFNOT.jpg'),
(10, 'Mercedes-Benz', 'CLA Coupé', '2022', 'Blanco', '4', 'Si', 'SM_A2NQ13GZKOW0JIDP9.jpg');
