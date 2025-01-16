from databases import Database

DATABASE_URL = "postgresql://username:password@db:5432/nudges"

# Conexión asíncrona con databases
database = Database(DATABASE_URL)