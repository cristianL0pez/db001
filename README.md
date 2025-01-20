# db001
proyecto para curso de base de datos

## paso  1 
conectar postgres de render a  pgadmin 4
hostname : oregon-postgres.render.com
los demas datos de conexion estan en render

crear las tablas  usuarios  y  items

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT
);


## paso 2
conectar postgres a backend 
Configura la conexión
linea 8 del main.py
DATABASE_URL = "aqui va el External Database URL"


## paso 3  
comando para levantar el docker 
docker-compose up -d --build
