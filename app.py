from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
from spleeter.separator import Separator
import os
import uuid
from werkzeug.utils import secure_filename

from fastapi import FastAPI

fastapp = FastAPI()

@fastapp.get("/")
def root():
    return {"message": "Hello from Render!"}


app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

separator = Separator('spleeter:2stems')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'audio' not in request.files:
        return "No file part", 400

    file = request.files['audio']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
    file.save(input_path)

    # Store session info to share between requests
    session['input_path'] = input_path
    session['output_dir'] = os.path.join(app.config['OUTPUT_FOLDER'], unique_id)

    return redirect(url_for('processing'))

@app.route('/processing')
def processing():
    return render_template('processing.html')

@app.route('/result')
def result():
    input_path = session.get('input_path')
    output_dir = session.get('output_dir')

    if not input_path or not output_dir:
        return redirect(url_for('index'))

    # Run spleeter
    separator.separate_to_file(input_path, output_dir)

    # Set filenames
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_folder = os.path.join(output_dir, base_name)

    vocal_path = os.path.join(output_folder, 'vocals.wav')
    instrumental_path = os.path.join(output_folder, 'accompaniment.wav')

    return render_template('result.html',
                           vocal_url=vocal_path.replace('static/', ''),
                           instrumental_url=instrumental_path.replace('static/', ''))

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
