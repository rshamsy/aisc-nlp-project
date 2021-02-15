import os
from flask import Flask, render_template, request, url_for
from tika import parser
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    
    file = request.files['uploaded_file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # use tika package to extract text from PDF
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_data = parser.from_file(filepath)
    text = file_data['content']
    return text
    

