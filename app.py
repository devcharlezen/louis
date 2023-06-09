# app.py
from flask import Flask, render_template, request, redirect
import os
import cv2
import numpy as np
import time
from urllib.parse import quote_plus

app = Flask(__name__)

interviewQuestions = [
    {
        'id': 1,
        'questions': [
            {'number_id': 1, 'questionText': 'What is event delegation in JavaScript?'},
            {'number_id': 2, 'questionText': 'Explain the concept of closures in JavaScript and provide an example.'},
        ]
    },
    {
        'id': 2,
        'questions': [
            {'number_id': 1, 'questionText': 'How does prototypal inheritance work in JavaScript?'},
            {'number_id': 2, 'questionText': 'Describe the differences between `null` and `undefined` in JavaScript.'},
        ]
    },
    {
        'id': 3,
        'questions': [
            {'number_id': 1, 'questionText': 'What is the purpose of the `this` keyword in JavaScript? How is it determined?'},
            {'number_id': 2, 'questionText': 'What is the difference between a list and a tuple in Python?'},
        ]
    },
    {
        'id': 4,
        'questions': [
            {'number_id': 1, 'questionText': 'Explain the concept of generators in Python and how they differ from regular functions.'},
            {'number_id': 2, 'questionText': 'What are the main differences between Python 2 and Python 3?'},
        ]
    },
    {
        'id': 5,
        'questions': [
            {'number_id': 1, 'questionText': 'Describe the purpose of decorators in Python and provide an example.'},
            {'number_id': 2, 'questionText': 'How does exception handling work in Python? Explain the `try-except` block.'},
        ]
    },
]

recorder_answers = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interview')
def interview():
    return render_template('interview.html', questions=interviewQuestions)

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if 1 <= question_id <= len(interviewQuestions):
        question_data = interviewQuestions[question_id - 1]
        question_count = len(interviewQuestions)
        if request.method == 'POST':
            video_data = request.form.get('videoData')
            cartoon_video_data = convert_to_cartoon(video_data)
            recorder_answers.append({'question_id': question_id, 'video_data': cartoon_video_data})
            next_question_id = question_id + 1
            return redirect(f'/question/{next_question_id}')
        return render_template('question.html', question_data=question_data, question_count=question_count)
    else:
        return "Question not found"

@app.route('/recording_urls')
def recording_urls():
    return render_template('recording_urls.html', recorder_answers=recorder_answers)

def create_video_url(question_id):
    timestamp = int(time.time())
    encoded_question_id = quote_plus(str(question_id))
    video_url = f"/video/{encoded_question_id}/{timestamp}"
    return video_url

def convert_to_cartoon(video_data):
    nparr = np.frombuffer(video_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Apply cartoon effect to the image
    cartoon_img = cartoonify_image(img)

    # Encode the cartoon image to video format
    _, cartoon_data = cv2.imencode('.webm', cartoon_img)
    cartoon_video_data = cartoon_data.tobytes()
    return cartoon_video_data

def cartoonify_image(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply median blur to smoothen the image
    blur = cv2.medianBlur(gray, 5)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter to reduce noise and keep the edges sharp
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # Combine the edges and color image to create a cartoon effect
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    return cartoon

if __name__ == '__main__':
    app.run(debug=True)
