from flask import Flask, render_template, request, jsonify
import face_recognition
import numpy as np
import base64
import cv2
import os

app = Flask(__name__)

# Load known faces
known_face_encodings = []
known_face_names = []

KNOWN_DIR = 'known_faces'
for file in os.listdir(KNOWN_DIR):
    path = os.path.join(KNOWN_DIR, file)
    if file.endswith(('.jpg', '.png')):
        image = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(file)[0])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json['image']
    img_data = base64.b64decode(data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_encodings(rgb_frame)

    name = "Unknown"
    if faces:
        matches = face_recognition.compare_faces(known_face_encodings, faces[0])
        if True in matches:
            index = matches.index(True)
            name = known_face_names[index]

    return jsonify({'name': name})
