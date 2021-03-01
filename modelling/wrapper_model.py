from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.reader.farm import FARMReader
from haystack.file_converter.txt import TextConverter
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.docx import DocxToTextConverter
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.pipeline import ExtractiveQAPipeline
import os

simple_questions = [
    "How does your board oversee climate issues?",
    "Who is responsible for climate-related issues?",
    "How are climate issues monitored?",
    "Do you identify and respond to climate risks and opportunities?",
    "How do you define long-term time horizons?",
    "How do you identify and respond to climate risks and opportunities?",
    "Which climate risk types do you consider?",
    "Do you assess your portfolio's exposure to climate risks and opportunities?",
    "How do you assess your portfolio's exposure to climate risks and opportunities?",
    "Do you request climate-related information from your clients or investees?",
    "Do climate risks have a financial impact on your business?",
    "What climate risks may have a financial impact on your business?",
    "Are there any climate opportunities that have financial impact on your business?",
    "What climate opportunities will have a financial impact on your business?",
    "Have climate risks and opportunities influenced your strategy or finances?",
    "Do you analyze climate scenarios to inform your strategy?",
    "What climate scenarios do you analyze?",
    "How have climate risks and opportunities influenced your strategy?",
    "How have climate risks and opportunities influenced your financial planning?",
    "Do climate issues effect your external asset manager or independent asset manager selection?",
    "How do climate issues effect your external asset manager or independent asset manager selection?",
    "Did you have an emissions target?",
    "What is your absolute emissions target progress?",
    "What is your emissions intensity target progress?",
    "Did you have climate targets?",
    "What are your targets to increase low-carbon energy consumption or production?",
    "What are your methane-reduction targets?",
    "What were your buildings' operational Scope 1 emissions in metric tons of carbon dioxide?",
    "What were market-based power usage Scope 2 emissions in metric tons of carbon dioxide?",
    "What were your employees' Scope 3 emissions in metric tons of carbon dioxide?",
    "What climate metrics do you use?",
    "Do you analyze how your portfolio impacts the climate?",
    "What are your Scope 3 portfolio emissions?",
    "What is your Scope 3 portfolio impact from Category 15 Investments with alternative carbon footprinting or exposure metrics?",
    "Why do you not conduct analysis to understand how your portfolio impacts the climate with Scope 3 portfolio impact from Category 15 Investments with alternative carbon footprinting or exposure metrics?"
]

class ModelWrapper():
  def __init__(self, reader):
    self._reader = reader

  def predict(self, data):
    upload_folder = data["upload_folder"][0]

    all_docs = convert_files_to_dicts(dir_path=f"{upload_folder}")
    document_store = InMemoryDocumentStore()
    document_store.write_documents(all_docs)
    retriever = TfidfRetriever(document_store=document_store)
    
    question_number = int(data["question_number"][0])
    question = simple_questions[question_number]
    pipe = ExtractiveQAPipeline(self._reader, retriever)
    prediction = pipe.run(query=simple_questions[question_number], top_k_retriever=10, top_k_reader=3)

    return question,prediction

def _load_pyfunc(path):

  # Load the model object
  reader = FARMReader(model_name_or_path=path)

  return ModelWrapper(
    reader=reader
  )