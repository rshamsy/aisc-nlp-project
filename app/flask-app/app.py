import os
from flask import Flask, render_template, request, url_for, session, request
from werkzeug.utils import secure_filename
import pandas as pd
from config import UPLOAD_FOLDER, PATH_TO_MODEL
import mlflow.pyfunc

# UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', "txt", "docx"}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
@app.route('/uploads')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/answers', methods=['POST'])
def answers():
    
    files = request.files.getlist("uploaded_files")
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # pull question text from user input
    
    question = request.form.get("question")

    # load model with pyfunc and make prediction

    mlflow_model = mlflow.pyfunc.load_model(PATH_TO_MODEL)

    df_in = pd.DataFrame([question, UPLOAD_FOLDER], columns=['question_number', "upload_folder"])

    question,prediction = mlflow_model.predict(df_in)

    answer1 = prediction["answers"][0]["answer"]
    context1 = prediction["answers"][0]["context"]
    document_name_1 = prediction["answers"][0]["meta"]["name"]
    
    answer2 = prediction["answers"][1]["answer"]
    context2 = prediction["answers"][1]["context"]
    document_name_2 = prediction["answers"][1]["meta"]["name"]
    
    answer3 = prediction["answers"][2]["answer"]
    context3 = prediction["answers"][2]["context"]
    document_name_3 = prediction["answers"][2]["meta"]["name"]

    # send results to output.html
    
    render_values_1 = {
        'question': question,
        "answer" : answer1
        "context" : context1
    }

    render_values_2 = {
        'question': question,
        "answer" : answer2
        "context" : context2
    }

    render_values_3 = {
        'question': question,
        "answer" : answer3
        "context" : context3
    }
    
    return render_template('output.html', render_values_1=render_values_1, render_values_2=render_values_2, render_values_3=render_values_3)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)