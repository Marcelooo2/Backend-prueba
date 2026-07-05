import pymysql

# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS TiDB (AWS)
# ==========================================
DB_HOST = 'gateway01.us-east-1.prod.aws.tidbcloud.com'
DB_PORT = 4000
DB_USER = '48vN34SyuVsmZoq.root'
DB_PASSWORD = 'kWXlqgNGbN2MqHKB' 
DB_NAME = 'deepl_arabica'

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