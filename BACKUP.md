# Backup de una base de datos PostgreSQL en la nube

Este documento explica cómo realizar un backup de una base de datos PostgreSQL alojada en la nube (por ejemplo, en **Render**) utilizando la herramienta `pg_dump`. También se incluyen instrucciones para automatizar el proceso con un script en Bash y programarlo con `cron`.

---

## Requisitos

1. **Acceso a la base de datos**: Necesitas las credenciales de la base de datos (usuario, contraseña, host, puerto y nombre de la base de datos).
2. **PostgreSQL Client**: Debes tener instalado el cliente de PostgreSQL (`pg_dump`) en tu máquina local.
3. **Permisos de escritura**: Asegúrate de tener permisos para escribir en el directorio donde se guardarán los backups.

---

## Paso 1: Instalar el cliente de PostgreSQL

Asegúrate de tener instalada una versión de `pg_dump` compatible con la versión del servidor de PostgreSQL. Por ejemplo, si el servidor está en la versión 16.x, instala el cliente correspondiente.

### En Ubuntu/Debian

1. Agrega el repositorio oficial de PostgreSQL:
   ```bash
   sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
Importa la clave GPG del repositorio:

bash
Copy
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
Actualiza la lista de paquetes:

bash
Copy
sudo apt update
Instala la versión 16.x del cliente de PostgreSQL:

bash
Copy
sudo apt install postgresql-client-16
Verifica la instalación:

bash
Copy
pg_dump --version
En macOS (con Homebrew)
Instala PostgreSQL 16.x:

bash
Copy
brew install postgresql@16
Agrega pg_dump al PATH:

bash
Copy
echo 'export PATH="/usr/local/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
Verifica la instalación:

bash
Copy
pg_dump --version
En Windows
Descarga el instalador de PostgreSQL 16.x desde postgresql.org.

Durante la instalación, asegúrate de seleccionar las herramientas de línea de comandos (Command Line Tools).

Verifica la instalación:

bash
Copy
pg_dump --version
Paso 2: Crear un script de backup
Crea un script en Bash para automatizar el proceso de backup. Guarda el siguiente código en un archivo llamado backup_postgres.sh:

bash
Copy
#!/bin/bash

# Configuración
PG_USER="midb_ff6g_user"               # Usuario de PostgreSQL
PG_HOST="oregon-postgres.render.com"   # Host de PostgreSQL
PG_PORT="5432"                         # Puerto de PostgreSQL
DB_NAME="midb_ff6g"                    # Nombre de la base de datos
BACKUP_DIR="$HOME/backups"             # Directorio donde se guardarán los backups
DATE=$(date +%Y-%m-%d_%H-%M-%S)        # Fecha y hora para el nombre del archivo
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.dump"  # Nombre del archivo de backup
PGPASSWORD="tu_contraseña"             # Contraseña de PostgreSQL

# Crear el directorio de backup si no existe
mkdir -p $BACKUP_DIR

# Mensaje de inicio
echo "Iniciando backup de la base de datos $DB_NAME en $BACKUP_FILE..."

# Ejecutar pg_dump
export PGPASSWORD
pg_dump -U $PG_USER -h $PG_HOST -p $PG_PORT -F c -b -v -f $BACKUP_FILE $DB_NAME

# Verificar si el backup fue exitoso
if [ $? -eq 0 ]; then
    echo "Backup completado con éxito: $BACKUP_FILE"
else
    echo "Error al realizar el backup."
    exit 1
fi

# Opcional: Comprimir el backup
echo "Comprimiendo el backup..."
gzip $BACKUP_FILE

# Opcional: Eliminar backups antiguos (más de 7 días)
echo "Eliminando backups antiguos..."
find $BACKUP_DIR -type f -name "*.dump.gz" -mtime +7 -exec rm {} \;

echo "Proceso de backup finalizado."
Paso 3: Hacer ejecutable el script
Guarda el script en tu máquina local.

Haz que el script sea ejecutable:

bash
Copy
chmod +x backup_postgres.sh
Paso 4: Ejecutar el script manualmente
Ejecuta el script para verificar que funciona correctamente:

bash
Copy
./backup_postgres.sh