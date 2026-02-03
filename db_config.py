import os

DB_CONFIG = {
    "host": "150.241.245.137",
    "user": "root",
    "password": "Tkla@123",
    "database": "takeknowlogic_db"
}
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}