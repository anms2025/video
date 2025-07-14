from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = []
    for i in range(1, 4):
        file = request.files.get(f'foto{i}')
        if file:
            filename = f'foto{i}.jpg'
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded_files.append(filepath)

    output_video = os.path.join(OUTPUT_FOLDER, 'video.mp4')
    subprocess.call([
        'ffmpeg', '-y',
        '-framerate', '1',
        '-i', f'{UPLOAD_FOLDER}/foto%d.jpg',
        '-c:v', 'libx264',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        output_video
    ])

    return redirect(url_for('index', video='/' + output_video))

if __name__ == '__main__':
    app.run(debug=True)
