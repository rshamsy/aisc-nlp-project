# aisc-nlp-project
NLP for Climate Risk Question-Answering

### Base Model
See Base-model.ipynb file in this repo.
* The question-answering task is done using a pretrained [roberta-base model](https://huggingface.co/deepset/roberta-base-squad2). 
...See code under "Using Pipeline" code section
...The test example is passed through via a context-question pair. 
...The context is in variable *text* and the question is in variable *question*
* The task is done using transformers' 'Pipeline' strategy. Instantiating model and tokenizer separately led to bugs, so the section "Instantiating Tokenizer + Model" is incomplete

### Next Steps 
See [Trello](https://trello.com/b/WGPdUp7m/aisc-nlp-project) for specs
* Packaging the model and serving it through Flask App
* Building front end application (Flask App)
* Serving the model and releasing Alpha

