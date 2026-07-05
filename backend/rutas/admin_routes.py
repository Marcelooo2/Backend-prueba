from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database import get_db_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios', methods=['GET', 'OPTIONS'])
def listar_usuarios():
    if request.method == 'OPTIONS': return '', 200
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre_completo, usuario, correo_electronico, estado FROM usuarios")
            usuarios = cursor.fetchall()
        conn.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/cambiar-estado', methods=['POST', 'OPTIONS'])
def cambiar_estado():
    if request.method == 'OPTIONS': return '', 200
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE usuarios SET estado = %s WHERE id = %s", (data['estado'], data['id']))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Estado actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/registrar', methods=['POST', 'OPTIONS'])
def registrar_admin():
    if request.method == 'OPTIONS': return '', 200
    datos = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            pass_enc = generate_password_hash(datos['contrasena'])
            sql = "INSERT INTO administradores (nombre_completo, usuario, correo_electronico, contrasena) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (datos['nombre_completo'], datos['usuario'], datos['correo_electronico'], pass_enc))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Administrador registrado con éxito'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500