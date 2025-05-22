from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from face_detection import detect_faces_and_attributes
from audio2txt import transcribe_audio_to_text
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = '1234'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('chat.html')

@socketio.on('connect')
def on_connect():
    welcome_message = "Bienvenido al asistente de transcripción y detección de rostros. ¿Cómo puedo ayudarte hoy?"
    emit('chat_response', welcome_message)

@app.route('/detect-face', methods=['POST'])
def detect_face():
    file = request.files['image']
    path = os.path.join('static', file.filename)
    file.save(path)
    results = detect_faces_and_attributes(path)
    return jsonify(results)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['audio']
    path = os.path.join('static', file.filename)
    file.save(path)
    result = transcribe_audio_to_text(path)
    return jsonify({"transcription": result})

@socketio.on('chat_message')
def handle_chat_message(message):
    message_lower = message.lower()  
    
    if "transcribir" in message_lower or "transcribe" in message_lower or "audio" in message_lower:
        response = "Por favor, sube tu archivo de audio para proceder a la transcripción."
    elif "detectar rostro" in message_lower or "rostro" in message_lower or "cara" in message_lower:
        response = "Por favor, sube tu archivo de imagen para proceder a la detección de rostros."
    else:
        response = f"Has dicho: {message}"
        
    emit('chat_response', response, broadcast=False)

if __name__ == "__main__":
    socketio.run(app, debug=True)


