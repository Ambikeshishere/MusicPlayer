from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Get all files in the upload folder
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    uploaded_files = [file for file in uploaded_files if allowed_file(file)]  # Filter allowed files
    return render_template('index.html', files=uploaded_files)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('file')  # Get multiple files
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html', files=os.listdir(UPLOAD_FOLDER))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
