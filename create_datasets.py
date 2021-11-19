import numpy as np
import pandas as pd

# Funcio per a llegir dades en format csv
def load_dataset(path):
    dataset = pd.read_csv(path, header=0, delimiter=',')
    return dataset

# we get 80% of each decade for training and 20% for testing
def get_dataset_flushed(train_size=0.8, test_size=0.1):
    """
    For each dataset of each decade, get random 20% and add it to a dataset
    """
    # Llegim dades
    total_index = ["60", "70", "80" , "90", "00", "10"]

    temp_ds_train = []
    temp_ds_test = []
    temp_ds_validate = []

    # Carreguem dataset d'exemple
    for i in range(len(total_index)):
        dataset = load_dataset('data/dataset-of-{0}s.csv'.format(total_index[i]))

        # Get random 80% of the dataset and add it to a dataset for training the 20% for testing
        dataset_train = dataset.sample(frac=train_size, random_state=1)
        dataset_test = dataset.drop(dataset_train.index)
        
        dataset_validate = dataset_test.sample(frac=test_size, random_state=1)
        dataset_validate = dataset_test.drop(dataset_validate.index)

        dataset_train['decade'] = total_index[i]
        dataset_test['decade'] = total_index[i]
        dataset_validate['decade'] = total_index[i]

        temp_ds_train.append(dataset_train)
        temp_ds_test.append(dataset_test)
        temp_ds_validate.append(dataset_validate)


    dataset_train = pd.concat(temp_ds_train, axis=0, ignore_index=True)
    dataset_test = pd.concat(temp_ds_test, axis=0, ignore_index=True)
    dataset_validate = pd.concat(temp_ds_validate, axis=0, ignore_index=True)

    dataset_train.drop(["track", "artist", "uri"], axis=1, inplace=True)
    dataset_test.drop(["track", "artist", "uri"], axis=1, inplace=True)
    dataset_validate.drop(["track", "artist", "uri"], axis=1, inplace=True)

    dataset_train.to_csv('data/dataset_test_joined.csv')
    dataset_test.to_csv('data/dataset_test_joined.csv')
    dataset_validate.to_csv('data/dataset_validate_joined.csv')

    return dataset_train, dataset_test, dataset_validate




def get_datasets():
    # Llegim dades
    total_index = ["60", "70", "80" , "90", "00", "10"]

    datasets_to_test = ["00", "10"]  # decada 2000 i 2010
    dataset_names_to_join = ["60", "70", "80" , "90"] # decada 1960, 1970, 1980 i 1990

    temp_ds_train = []
    temp_ds_test = []

    # Carreguem dataset d'exemple
    for i in range(len(dataset_names_to_join)):
        dataset = load_dataset('data/dataset-of-{0}s.csv'.format(dataset_names_to_join[i]))
        dataset['decade'] = dataset_names_to_join[i]
        temp_ds_train.append(dataset)

    for i in range(len(datasets_to_test)):
        dataset = load_dataset('data/dataset-of-{0}s.csv'.format(datasets_to_test[i]))
        dataset['decade'] = datasets_to_test[i]
        temp_ds_test.append(dataset)

    dataset_train = pd.concat(temp_ds_train, axis=0, ignore_index=True)
    dataset_test = pd.concat(temp_ds_test, axis=0, ignore_index=True)

    dataset_train.drop(["track", "artist", "uri"], axis=1, inplace=True)
    dataset_test.drop(["track", "artist", "uri"], axis=1, inplace=True)

    dataset_train.to_csv('data/dataset_test_joined.csv')
    dataset_test.to_csv('data/dataset_test_joined.csv')

    return dataset_train, dataset_test
