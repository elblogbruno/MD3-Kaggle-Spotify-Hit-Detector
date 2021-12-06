from src.dataset_utils import *

def generate_non_nlp_dataset():
    columns_to_drop  = ['track','artist','uri', 'chorus_hit','sections' ]
    # columns_to_drop  = ['track','artist','uri','key','mode','speechiness','liveness','tempo','duration_ms','chorus_hit','sections']

    dataset_full = get_full_dataset()
    dataset_train, dataset_test, dataset_validate = get_dataset_flushed(train_size=0.8, validate_size=0.0, columns_to_drop=columns_to_drop)

    return dataset_train, dataset_test, dataset_validate, dataset_full