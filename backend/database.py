import os
import pymysql

# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS TiDB (AWS)
# ==========================================
# os.getenv busca la variable en Render. Si no la encuentra (ej. en tu PC local), usa la contraseña de respaldo.
DB_HOST = os.getenv('DB_HOST', 'gateway01.us-east-1.prod.aws.tidbcloud.com')
DB_PORT = int(os.getenv('DB_PORT', 4000))
DB_USER = os.getenv('DB_USER', '48vN34SyuVsmZoq.root')

# ¡ATENCIÓN!: Cambia el texto 'TU_NUEVA_CONTRASEÑA_AQUI' por la clave que acabas de crear en TiDB.
DB_PASSWORD = os.getenv('DB_PASSWORD', 'TU_NUEVA_CONTRASEÑA_AQUI') 

DB_NAME = os.getenv('DB_NAME', 'deepl_arabica')

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST, 
        port=DB_PORT, 
        user=DB_USER, 
        password=DB_PASSWORD,
        database=DB_NAME, 
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl_verify_cert": False}
    )
