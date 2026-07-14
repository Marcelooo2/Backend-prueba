import requests
from flask import Blueprint, request, jsonify

# Asumiendo que usas un Blueprint. Ajusta el nombre según tu proyecto.
reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/clima', methods=['GET'])
def obtener_clima():
    # 1. Obtener coordenadas del frontend (con un fallback por si fallan)
    lat = request.args.get('lat', default=-12.04318, type=float)
    lon = request.args.get('lon', default=-77.02824, type=float)

    # 2. Configurar la llamada a Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure",
        "daily": "temperature_2m_max,temperature_2m_min,rain_sum,uv_index_max",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        current = data.get('current', {})
        daily = data.get('daily', {})

        # 3. Procesar datos
        temp_max = daily.get('temperature_2m_max', [0])[0]
        temp_min = daily.get('temperature_2m_min', [0])[0]
        temp_prom = round((temp_max + temp_min) / 2, 1)

        lluvia_hoy = daily.get('rain_sum', [0])[0]
        lluvia_semana = sum(daily.get('rain_sum', [0][:7]))
        
        uv_max = daily.get('uv_index_max', [0])[0]
        uv_nivel = "Alto" if uv_max > 7 else ("Medio" if uv_max > 3 else "Bajo")

        # 4. Estructurar el JSON de salida (sin alerta)
        reporte = {
            "temperatura": {
                "actual": f"{current.get('temperature_2m', 0)}°C",
                "max": f"{temp_max}°C",
                "min": f"{temp_min}°C",
                "promedio": f"{temp_prom}°C"
            },
            "humedad": {
                "actual": f"{current.get('relative_humidity_2m', 0)}%",
                "promedio": f"{current.get('relative_humidity_2m', 0)}%", 
                "lluviaHoy": f"{lluvia_hoy}mm",
                "lluviaSemana": f"{round(lluvia_semana, 1)}mm"
            },
            "condicion": {
                "viento": f"{current.get('wind_speed_10m', 0)}km/h",
                "uv": uv_nivel,
                "presion": f"{current.get('surface_pressure', 0)}hPa"
            }
        }
        
        return jsonify(reporte), 200

    except Exception as e:
        return jsonify({"error": "Fallo al conectar con la API de clima", "detalle": str(e)}), 500