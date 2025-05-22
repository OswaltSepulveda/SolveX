import cv2
from deepface import DeepFace

def detect_faces_and_attributes(img_path):
    
    img = cv2.imread(img_path)
    result = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'emotion'], enforce_detection=False)
    
    if isinstance(result, dict):
        result = [result]
    
    faces_inf = []
    for face in result:
        faces_inf.append({
            'edad': face['age'],
            'genero': face['gender'],
            'emocion': face['dominant_emotion']
        })
    
    return faces_inf
       