# Proyecto DB001

Este es un proyecto para un curso de bases de datos que incluye la configuración de PostgreSQL, creación de tablas, conexión a un backend y el uso de Docker para el despliegue.

---

## Pasos del Proyecto

### 1. Conectar PostgreSQL de Render a PgAdmin 4

1. **Configura la conexión en PgAdmin 4**:
   - **Hostname**: `oregon-postgres.render.com`
   - Los demás datos de conexión están disponibles en la página de configuración de Render.

2. **Crear las tablas necesarias en PostgreSQL**:

```sql
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
```

---

### 2. Conectar PostgreSQL al Backend

1. **Configura la conexión en el archivo `main.py`**:
   - Modifica la línea 8 para agregar la URL de la base de datos externa proporcionada por Render.

```python
DATABASE_URL = "aqui va el External Database URL"
```

---

### 3. Levantar el Proyecto con Docker

1. Usa el siguiente comando para construir y levantar los servicios:

```bash
docker-compose up -d --build
```

---

## Información Adicional

### Requisitos Previos

- Tener instalado `Docker` y `Docker Compose`.
- Disponer de acceso a la base de datos en Render.
- Contar con PgAdmin 4 para gestionar PostgreSQL.

### Funcionalidades del Proyecto

- **Tablas:**
  - `usuarios`: para gestionar los usuarios.
  - `items`: para almacenar elementos y sus descripciones.
- **Backend:**
  - Conexión a PostgreSQL.
  - API funcional con endpoints para CRUD.
- **Despliegue:**
  - Contenedor de Docker para simplificar el entorno de desarrollo y producción.

---

¿Faltaría incluir información sobre cómo probar los endpoints del backend o algún detalle adicional? Avísame si necesitas agregar más secciones.

