import os
from flask import Flask, render_template, request, url_for, session
from tika import parser
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
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
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TODO: change this to answers
@app.route('/upload', methods=['POST'])
def upload():
    
    file = request.files['uploaded_file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # use tika package to extract text from PDF
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_data = parser.from_file(filepath)
    text = file_data['content']

    

    render_values = {
        'question': questions_dict[request.form.get("question")], 
        "context" : text,
        "answer" : text
    }

    
    return render_template('output.html', render_values=render_values)


    

