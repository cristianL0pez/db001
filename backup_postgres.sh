#!/bin/bash

# Configuración
PG_USER="midb_ff6g_user"
PG_HOST="oregon-postgres.render.com"
PG_PORT="5432"
DB_NAME="midb_ff6g"
BACKUP_DIR="/workspaces/db001/backup"
PGPASSWORD="5FebCuwKycGrfFm7NK4l7r8Um7PTfNXY"

# Crear el directorio de backup si no existe
mkdir -p $BACKUP_DIR

# Bucle infinito con intervalo de 5 minutos
while true; do
    DATE=$(date +%Y-%m-%d_%H-%M-%S)
    BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.dump"

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

    # Comprimir el backup
    echo "Comprimiendo el backup..."
    gzip $BACKUP_FILE

    # Eliminar backups antiguos (más de 7 días)
    echo "Eliminando backups antiguos..."
    find $BACKUP_DIR -type f -name "*.dump.gz" -mtime +7 -exec rm {} \;

    echo "Proceso de backup finalizado."

    # Esperar 5 minutos antes de la siguiente ejecución
    sleep 300
done