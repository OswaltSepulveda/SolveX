import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio_to_text(audio_path):
    
    if not audio_path.endswith('.wav'):
        sound = AudioSegment.from_file(audio_path)
        audio_path = audio_path.replace('.', '_converted.') + ".wav"
        sound.export(audio_path, format="wav")
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    try:
        return recognizer.recognize_google(audio, language='es-ES')
    except sr.UnknownValueError:
        return "No se pudo entender el audio"
    except sr.RequestError as e:
        return f"Error al solicitar resultados de Google Speech Recognition; {e}"

