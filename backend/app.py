from flask import Flask
from flask_cors import CORS

# Importamos los Blueprints desde la carpeta interna de rutas
from rutas.auth_routes import auth_bp
from rutas.admin_routes import admin_bp
from rutas.diag_routes import diag_bp
from rutas.reportes_routes import reportes_bp

app = Flask(__name__)

# Permitimos CORS explícitamente para peticiones de Angular
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ==========================================
# REGISTRO DE MÓDULOS (BLUEPRINTS)
# ==========================================
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(diag_bp, url_prefix='/api/diagnosticos')
app.register_blueprint(reportes_bp, url_prefix='/api/reportes')

# Endpoint de verificación de salud del sistema
@app.route('/', methods=['GET'])
def health_check():
    return "API DeepL-Arabica funcionando al 100% con arquitectura modular", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)