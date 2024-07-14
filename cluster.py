import gensim
import nltk
import numpy as np
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin
nltk.download('punkt')
nltk.download('stopwords')
import re




class preprocess_document(BaseEstimator, TransformerMixin):

    def fit(self, X, y= None):
        return self
    
    def transform(self, X):
 
        processed_documents = []
        for document in X["topics"]:
            document = re.sub(r'\[.*?\]', '', document)
            document = re.sub(r'[^a-zA-Z\s]', '', document)
            tokens = word_tokenize(document)
            tokens = [word.lower() for word in tokens]
            tokens = [word for word in tokens if word.isalpha()]
            stop_words = set(stopwords.words('english'))
            tokens = [word for word in tokens if word not in stop_words]
            processed_documents.append(tokens)
    
        X["tokens"] = processed_documents
        return X


class document_to_vector(BaseEstimator, TransformerMixin):

    def __init__(self, model):
        super().__init__
        self.model = model

    def fit(self, X, y =None):
        return self
    
    def transform(self, X): 
        document_vectors = []
        for tokens in X["tokens"]:
            word_vectors = []
            for token in tokens:
                if token in self.model:
                    word_vectors.append(self.model[token])
            if word_vectors: 
                document_vector = np.mean(word_vectors, axis = 0)
            else:
                document_vector = np.zeros(self.model.vector_size)
            document_vectors.append(document_vector)

        return np.array(document_vectors)

