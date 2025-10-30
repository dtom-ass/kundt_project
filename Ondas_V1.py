# Importar Scip y Pyaudio para generar las ondas de sonido.
import pyaudio
import numpy as np

define_hz = 150
time_duration = 2

def fun_sound():
    try:
        t = np.linspace(0, time_duration,int(44100 * time_duration),endpoint=False)
        onda = 1 * np.sin(2*np.pi * define_hz * t)
        print("Función de onda generada...")
        onda_int16 = np.int16(onda * 32767)
        print("Transformando función de onda...")

        p = pyaudio.PyAudio()
        print("Iniciando PyAudio...")
        stream = p.open(
            format=pyaudio.paInt16,   # formato de 16 bits
            channels=1,
            rate=44100,
            output=True
        )

        print("Tranformando sonido...")
        stream.write(onda_int16.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        print(f"Error: {e}")

fun_sound()