from flask import jsonify
from app import app, image_processing

recognition = image_processing.Recognition()


@app.route("/")
def hello_world():
    return jsonify(
        recognition.do_recognition('app/2.jpg',
            actions=['emotion'])), 200
