import os
from flask import Flask, render_template, request, url_for, session, request
from werkzeug.utils import secure_filename
import pandas as pd
from config import PATH_TO_MODEL
# import mlflow.pyfunc
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.reader.farm import FARMReader
from haystack.file_converter.txt import TextConverter
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.docx import DocxToTextConverter
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.pipeline import ExtractiveQAPipeline

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', "txt", "docx"}
questions_dict = {
    "1": "How does your board oversee climate issues?",
    "2": "Who is responsible for climate-related issues?",
    "3": "How are climate issues monitored?",
    "4": "Do you identify and respond to climate risks and opportunities?",
    "5": "How do you define long-term time horizons?",
    "6": "How do you identify and respond to climate risks and opportunities?",
    "7": "Which climate risk types do you consider?",
    "8": "Do you assess your portfolio's exposure to climate risks and opportunities?",
    "9": "How do you assess your portfolio's exposure to climate risks and opportunities?",
    "10": "Do you request climate-related information from your clients or investees?",
    "11": "Do climate risks have a financial impact on your business?",
    "12": "What climate risks may have a financial impact on your business?",
    "13": "Are there any climate opportunities that have financial impact on your business?",
    "14": "What climate opportunities will have a financial impact on your business?",
    "15": "Have climate risks and opportunities influenced your strategy or finances?",
    "16": "Do you analyze climate scenarios to inform your strategy?",
    "17": "What climate scenarios do you analyze?",
    "18": "How have climate risks and opportunities influenced your strategy?",
    "19": "How have climate risks and opportunities influenced your financial planning?",
    "20": "Do climate issues effect your external asset manager or independent asset manager selection?",
    "21": "How do climate issues effect your external asset manager or independent asset manager selection?",
    "22": "Did you have an emissions target?",
    "23": "What is your absolute emissions target progress?",
    "24": "What is your emissions intensity target progress?",
    "25": "Did you have climate targets?",
    "26": "What are your targets to increase low-carbon energy consumption or production?",
    "27": "What are your methane-reduction targets?",
    "28": "What were your buildings' operational Scope 1 emissions in metric tons of carbon dioxide?",
    "29": "What were market-based power usage Scope 2 emissions in metric tons of carbon dioxide?",
    "30": "What were your employees' Scope 3 emissions in metric tons of carbon dioxide?",
    "31": "What climate metrics do you use?",
    "32": "Do you analyze how your portfolio impacts the climate?",
    "33": "What are your Scope 3 portfolio emissions?",
    "34": "What is your Scope 3 portfolio impact from Category 15 Investments with alternative carbon footprinting or exposure metrics?",
    "35": "Why do you not conduct analysis to understand how your portfolio impacts the climate with Scope 3 portfolio impact from Category 15 Investments with alternative carbon footprinting or exposure metrics?"
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    # use haystack package to extract text from uploads

    all_docs = convert_files_to_dicts(dir_path=f"{UPLOAD_FOLDER}")

    # pull question text from user input
    
    question = request.form.get("question")

    # load uploads into document store and create document retriever

    document_store = InMemoryDocumentStore()
    document_store.write_documents(all_docs)
    retriever = TfidfRetriever(document_store=document_store)

    # create reader

    reader = FARMReader(model_name_or_path="deepset/xlm-roberta-large-squad2")

    # create pipeline

    pipe = ExtractiveQAPipeline(reader, retriever)

    # run inference

    prediction = pipe.run(query=questions_dict[question], top_k_retriever=5, top_k_reader=5)

    # send results to output.html
    
    render_values_1 = {
        'question': questions_dict[question],
        "context" : prediction["answers"][0]["context"],
        "answer" : prediction["answers"][0]["answer"]
    }

    render_values_2 = {
        'question': questions_dict[question],
        "context" : prediction["answers"][1]["context"],
        "answer" : prediction["answers"][1]["answer"]
    }

    render_values_3 = {
        'question': questions_dict[question],
        "context" : prediction["answers"][2]["context"],
        "answer" : prediction["answers"][2]["answer"]
    }
    
    return render_template('output.html', render_values_1=render_values_1, render_values_2=render_values_2, render_values_3=render_values_3)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)