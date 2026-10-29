from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/analizar", methods=["POST"])
def analizar():
    archivo = request.files["imagen"].read()
    img = cv2.imdecode(np.frombuffer(archivo, np.uint8), cv2.IMREAD_COLOR)
    alto, ancho = img.shape[:2]
    color_prom = img.mean(axis=(0, 1)).tolist()  # BGR
    bordes = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 100, 200)
    return jsonify({
        "ancho": ancho,
        "alto": alto,
        "color_promedio_bgr": color_prom,
        "porcentaje_bordes": round(float((bordes > 0).mean() * 100), 2),
    })

@app.route("/")
def salud():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)