from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.reader.farm import FARMReader
from haystack.file_converter.txt import TextConverter
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.docx import DocxToTextConverter
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.pipeline import ExtractiveQAPipeline
import os

class ModelWrapper():
  def __init__(self, reader):
    self._reader = reader

  def predict(self, data):
    upload_folder = data["upload_folder"][0]

    all_docs = convert_files_to_dicts(dir_path=f"{upload_folder}")
    document_store = InMemoryDocumentStore()
    document_store.write_documents(all_docs)
    retriever = TfidfRetriever(document_store=document_store)
    
    company = data["company_name"][0]
    simple_questions = [
      f"How does the {company} board oversee climate issues?",
      f"How does the {company} management assess and manage climate risks and opportunities?",
      f"What climate risks and opportunities has {company} identified?",
      f"What time frames are associated with the climate risks and opportunities at {company}?",
      f"What impact would climate risks and opportunities have on {company}?",
      f"How does {company} describe the resilience of its strategy, taking into consideration different climate scenarios, including alignment with the Paris Agreement?",
      f"How does {company} consider emissions reduction goals in evaluating strategy or financial planning, or for other business purposes?",
      f"How does {company} identify and assess climate risks?",
      f"How does {company} manage and mitigate climate risks?",
      f"How are climate risks integrated into risk management at {company}?",
      f"What metrics does {company} use to assess climate risks and opportunities?",
      f"What are the Scope 1, Scope 2, and Scope 3 greenhouse gas (GHG) emissions for {company}?",
      f"What targets does {company} use to manage climate risks and opportunities?",
      f"How has {company} performed in meeting targets to manage climate risks and opportunities?"
      ]
    question_number = int(data["question_number"][0]) - 1
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