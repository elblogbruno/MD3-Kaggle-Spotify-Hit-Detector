from src.nltk_test.generate_features_nltk import generate_nlp_dataset
from src.non_nltk_test.generate_features_non_nltk import generate_non_nlp_dataset

def generate_dataset(type = 'nlp'):
    """
    Generates a dataset for the model.
    """
    if type == 'nlp':
        return generate_nlp_dataset()
    elif type == 'non-nlp':
        return generate_non_nlp_dataset()
