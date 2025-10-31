"""
"""
import numpy as np
import pyaudio
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SAMPLE_RATE = 44100
DURATION = 2.0  # segundos


def generar_ondas(f1, f2, p1_deg, p2_deg):
    """Genera dos ondas senoidales y su mezcla."""
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    p1 = np.deg2rad(p1_deg)
    p2 = np.deg2rad(p2_deg)

    wave1 = np.sin(2 * np.pi * f1 * t + p1)
    wave2 = np.sin(2 * np.pi * f2 * t + p2)
    mixed = (wave1 + wave2) / 2

    return wave1, wave2, mixed, t


def reproducir_audio(wave):
    """Reproduce el audio generado."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True)
    stream.write(wave.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play', methods=['POST'])
def play():
    """Reproduce según el modo: onda1, onda2 o mezcla."""
    f1 = float(request.form['f1'])
    f2 = float(request.form['f2'])
    p1 = float(request.form['p1'])
    p2 = float(request.form['p2'])
    modo = request.form['modo']  # 'onda1', 'onda2', 'mezcla'

    wave1, wave2, mixed, t = generar_ondas(f1, f2, p1, p2)

    if modo == "onda1":
        reproducir_audio(wave1)
        data = wave1
    elif modo == "onda2":
        reproducir_audio(wave2)
        data = wave2
    else:
        reproducir_audio(mixed)
        data = mixed

    # Retornamos datos para graficar (solo primeros 1000 puntos)
    return jsonify({
        'time': t[:1000].tolist(),
        'wave1': wave1[:1000].tolist(),
        'wave2': wave2[:1000].tolist(),
        'mixed': mixed[:1000].tolist()
    })


if __name__ == '__main__':
    app.run(debug=True)
