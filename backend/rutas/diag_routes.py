from flask import Blueprint, request, jsonify
from database import get_db_connection
from datetime import datetime # 🚀 Importamos el motor de tiempo real

diag_bp = Blueprint('diagnosticos', __name__)

@diag_bp.route('/guardar', methods=['POST', 'OPTIONS'])
def guardar_diagnostico():
    if request.method == 'OPTIONS': return '', 200
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """INSERT INTO diagnosticos 
                    (usuario_id, parcela_id, resultado, enfermedad, confianza, recomendacion, foto_url, fecha_hora) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"""
            cursor.execute(sql, (
                data.get('usuario_id'), 
                data.get('parcela_id'), 
                data.get('resultado'), 
                data.get('enfermedad'), 
                data.get('confianza'),
                data.get('recomendacion', ''),
                data.get('foto_url', '')
            ))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Diagnóstico guardado en BD exitosamente'}), 201
    except Exception as e:
        print(f"❌ ERROR CRÍTICO DE MYSQL: {str(e)}")
        return jsonify({'error': str(e)}), 500

@diag_bp.route('/historial/usuario/<int:usuario_id>', methods=['GET', 'OPTIONS'])
def obtener_historial(usuario_id):
    if request.method == 'OPTIONS': return '', 200
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # SQL limpio. Extraemos la fecha como texto (CHAR)
            sql = """SELECT id, CAST(fecha_hora AS CHAR) as fecha_str, 
                            resultado as diagnostico, enfermedad, parcela_id as parcela, 
                            confianza, recomendacion, foto_url 
                     FROM diagnosticos 
                     WHERE usuario_id = %s 
                     ORDER BY fecha_hora DESC"""
            cursor.execute(sql, (usuario_id,))
            
            columnas = [columna[0] for columna in cursor.description]
            registros = []
            
            for fila in cursor.fetchall():
                dic = dict(zip(columnas, fila))
                
                # 🚀 Formateo manual usando la fecha REAL del sistema
                fecha_raw = dic.pop('fecha_str', '')
                if fecha_raw and '-' in str(fecha_raw):
                    # Transforma '2026-07-14 14:30:00' -> '14/07/2026'
                    partes = str(fecha_raw).split(' ')[0].split('-')
                    if len(partes) >= 3:
                        dic['fecha'] = f"{partes[2]}/{partes[1]}/{partes[0]}"
                    else:
                        dic['fecha'] = datetime.now().strftime('%d/%m/%Y')
                else:
                    # Si falla, pone la fecha exacta de hoy
                    dic['fecha'] = datetime.now().strftime('%d/%m/%Y') 
                    
                registros.append(dic)
                
        conn.close()
        return jsonify(registros), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@diag_bp.route('/historial/actualizar-parcela', methods=['PUT', 'OPTIONS'])
def actualizar_parcela():
    if request.method == 'OPTIONS': return '', 200
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE diagnosticos SET parcela_id = %s WHERE id = %s"
            cursor.execute(sql, (data['nueva_parcela'], data['id_diagnostico']))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Parcela actualizada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
