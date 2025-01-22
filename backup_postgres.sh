#!/bin/bash

# Configuración
PG_USER="midb_ff6g_user"          # Usuario de PostgreSQL
PG_HOST="oregon-postgres.render.com" # Host de PostgreSQL
PG_PORT="5432"                # Puerto de PostgreSQL
DB_NAME="midb_ff6g"    # Nombre de la base de datos
BACKUP_DIR="/workspaces/db001/backup"  # Directorio donde se guardarán los backups
DATE=$(date +%Y-%m-%d_%H-%M-%S)  # Fecha y hora para el nombre del archivo
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.dump"  # Nombre del archivo de backup
PGPASSWORD="5FebCuwKycGrfFm7NK4l7r8Um7PTfNXY"  

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