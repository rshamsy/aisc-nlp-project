from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.file_converter.txt import TextConverter
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.docx import DocxToTextConverter
from haystack.preprocessor.preprocessor import PreProcessor
from haystack import Finder
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.retriever.dense import DensePassageRetriever, EmbeddingRetriever
from haystack.pipeline import ExtractiveQAPipeline

reader = FARMReader(model_name_or_path="deepset/xlm-roberta-large-squad2")

import wrapper_model
import mlflow
import torch

train_data = "./answers"
reader.train(data_dir=train_data, train_filename="answers.json", use_gpu=False, n_epochs=1, save_dir="tuned_1_iter_xlm-roberta-large-squad2")

mlflow_path = './pyfunc_model'

mlflow.pyfunc.save_model(
    path=mlflow_path,
    loader_module=wrapper_model.__name__,
    data_path="./tuned_1_iter_xlm-roberta-large-squad2/",
    code_path=['./wrapper_model.py'],
    conda_env='./conda.yml'
)
