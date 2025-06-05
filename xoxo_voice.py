import pyttsx3

def xoxo_speak():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Ajusta si quieres voz femenina
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)

    mensaje = "Hola Cristhiam, soy XOXO. Nuestra mente curiosa está lista para imaginar, construir y transformar. ¡Ya estamos conectados!"
    engine.say(mensaje)
    engine.runAndWait()

if __name__ == "__main__":
    xoxo_speak()
