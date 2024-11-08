CREATE DATABASE SistemaSoporte;
USE SistemaSoporte;

CREATE TABLE REQUERIMIENTO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(20),
    requerimiento TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#Consulta de los datos enviados por postman
select * from requerimiento