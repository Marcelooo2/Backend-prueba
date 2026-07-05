from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['POST', 'OPTIONS'])
def registro_usuario():
    if request.method == 'OPTIONS': return '', 200
    datos = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            password_encriptada = generate_password_hash(datos['password'])
            sql = """INSERT INTO usuarios 
                (nombre_completo, usuario, correo_electronico, contrasena) 
                VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (datos['nombre_completo'], datos['usuario'], datos['correo_electronico'], password_encriptada))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Usuario registrado con éxito'}), 201
    except pymysql.err.IntegrityError:
        return jsonify({'error': 'El usuario o correo ya existe'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login_usuario():
    if request.method == 'OPTIONS': return '', 200
    datos = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre_completo, usuario, contrasena FROM usuarios WHERE usuario = %s", (datos['usuario'],))
            usuario_db = cursor.fetchone()
        conn.close()

        if usuario_db and check_password_hash(usuario_db['contrasena'], datos['password']):
            return jsonify({
                'mensaje': 'Login exitoso',
                'usuario': {
                    'id': usuario_db['id'],
                    'nombre_completo': usuario_db['nombre_completo'],
                    'usuario': usuario_db['usuario'],
                    'rol': 'USER'
                }
            }), 200
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/admin-login', methods=['POST', 'OPTIONS'])
def admin_login():
    if request.method == 'OPTIONS': return '', 200
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM administradores WHERE usuario = %s", (data['usuario'],))
            admin = cursor.fetchone()
        conn.close()
        
        if admin and check_password_hash(admin['contrasena'], data['contrasena']):
            return jsonify({'message': 'Login exitoso', 'usuario': admin}), 200
        return jsonify({'error': 'Credenciales incorrectas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500