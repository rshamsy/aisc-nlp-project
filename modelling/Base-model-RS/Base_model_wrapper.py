import torch
import pickle
from transformers import pipeline
import pandas as pd

class ModelWrapper():
    def __init__(self, model, tokenizer):
        self._model = model
        self._tokenizer = tokenizer
        
        # create pipeline object passing model and tokenizer
        self._pipeline = pipeline('question-answering', model=self._model, tokenizer=self._tokenizer)
    
    def predict(self, data: pd.DataFrame):
        """
        predict function expects data in as a pd.DataFrame object with
        columns named 'context' and 'question', to access the two
        """
       
        # call pipeline on question and text
        return self._pipeline(question=data.iloc[0].question, context=data.iloc[0].context)


def _load_pyfunc(path):
    # load model 
    model = torch.load(f'{path}/model.pt')

    # load tokenizer
    tokenizer = torch.load(f'{path}/tokenizer.pt')
    
    return ModelWrapper(model=model, tokenizer=tokenizer) 
