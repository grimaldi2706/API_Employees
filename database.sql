-- Archivo de configuración inicial para la base de datos MySQL (database.sql)
-- Puedes importarlo en tu gestor (PhpMyAdmin, DBeaver, MySQL Workbench, etc.)

CREATE DATABASE IF NOT EXISTS `employees_db`
  CHARACTER SET = 'utf8mb4'
  COLLATE = 'utf8mb4_unicode_ci';

USE `employees_db`;

CREATE TABLE IF NOT EXISTS `employees` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `cargo` VARCHAR(255) NOT NULL,
    `departamento` VARCHAR(255) NOT NULL,
    `salario` DECIMAL(10, 2) NOT NULL,
    `is_active` TINYINT(1) DEFAULT 1,
    INDEX `ix_employees_email` (`email`),
    INDEX `ix_employees_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- (Opcional) Insertar un empleado de prueba
INSERT IGNORE INTO `employees` (`nombre`, `email`, `cargo`, `departamento`, `salario`, `is_active`) 
VALUES ('Juan Pérez', 'juan.perez@example.com', 'Desarrollador Backend', 'Ingeniería', 3500.00, 1);
