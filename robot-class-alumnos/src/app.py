from flask import Flask, request, jsonify
from src.model.alumno import Alumno
from src.service.robot import RobotPandora
import time

app = Flask(__name__)

@app.route('/procesar_alumnos', methods=['POST'])
def procesar_alumnos_clasificacion():
    # Obtener credenciales del header
    username = request.headers.get("Username")
    password = request.headers.get("Password")

    # Validación de datos de entrada
    data = request.get_json()
    alumnos_raw = data.get('alumnos', [])

    if not username or not password or not alumnos_raw:
        return jsonify({"error": "Faltan datos requeridos: username, password o alumnos"}), 400
    

    # Convertir el JSON a objetos Alumno
    lista_alumnos = []
    for item in alumnos_raw:
        lista_alumnos.append(Alumno(
            codigo=item.get('codigo'),
            curso=item.get('curso'),
            observacion=item.get('observacion')
        ))

    # Ejecucion del robot
    robot = RobotPandora()
    try:
        robot.iniciar()
        robot.login(username, password)
        robot.clasificador_alumnos(lista_alumnos)

        return jsonify({
            "status": "success",
            "message": f"Proceso completado para {len(lista_alumnos)} alumnos"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        robot.cerrar()

    if __name__ == "__main__":
        app.run(debug=True, port=8080)