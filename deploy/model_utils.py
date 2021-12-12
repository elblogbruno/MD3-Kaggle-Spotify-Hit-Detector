import joblib
import numpy as np
from src.dataset_utils import *
from src.generate_features import generate_dataset
from src.train_model import *
from deploy.database.model import *

def predict_value(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(-1, 1)
    print(to_predict)
    loaded_model = joblib.load('model/model-spotify-full-dataset.sav')
    result = loaded_model.predict(to_predict)

    # predictions = loaded_model.predict_proba(to_predict)
    # # print(predictions)
    # #get the index of the maximum probability
    # max_index = np.argmax(predictions)
    # #get the class with the maximum probability
    # max_probability = predictions[max_index]
    # # #get the class name
    # # max_probability_class = loaded_model.classes_[max_index]
    # # print(max_probability_class)
    # print("Probability of both classes: " + str(max_probability))
    # print("Probability flop: " + str(max_probability[0]))
    # print("Probability hit: " + str(max_probability[1]))

    # get probability of each class
    predictions = loaded_model.predict_proba(to_predict)
    print(predictions)
    print(predictions[0][0])
    print(predictions[0][1])

    return result[0], predictions[0][0], predictions[0][1]

def extract_decade_from_date(release_date):
    release_date = datetime.strptime(release_date, '%Y-%m-%d')
    release_year = release_date.year
    # get last to numbers of year
    # release_date = str(release_date)[-2:]
    
    if release_year < 1970:
        release_date = '60'
    elif release_year < 1980:
        release_date = '70'
    elif release_year < 1990:
        release_date = '80'
    elif release_year < 2000:
        release_date = '90'
    elif release_year < 2010:
        release_date = '00'
    elif release_year < 2020:
        release_date = '10'
    else:
        release_date = '20'

    return release_date


def save_new_entry(date, song_features, prediction):
    """ save new entry to model """
    date = extract_decade_from_date(date)

    dataset = get_dataset_year(date)

    # apprend prediction to song_features
    song_features['target'] = prediction

    # add new entry to dataste
    dataset = dataset.append(song_features, ignore_index=True)
    # save dataset
    dataset.to_csv('data/dataset-of-{0}s.csv'.format(date), index=False)

    # columns_to_drop  = ['track','artist','uri']


    # """ if random number is 0 save as train else save as test """
    # if np.random.randint(0,2) == 0:
    #     dataset_train, dataset_test, dataset_validate = get_dataset_flushed(train_size=0.8, validate_size=0.0, columns_to_drop=columns_to_drop)
    #     dataset_train.loc[len(dataset_train)] = song_features
    #     dataset_train.to_csv('dataset/train.csv', index=False)
    # else:
    #     dataset_train, dataset_test, dataset_validate = get_dataset_flushed(train_size=0.8, validate_size=0.0, columns_to_drop=columns_to_drop)
    #     dataset_test.loc[len(dataset_test)] = song_features
    #     dataset_test.to_csv('dataset/test.csv', index=False)

    """ retrain model """
    dataset_train, dataset_test, dataset_validate, dataset_full = generate_dataset(type='non-nlp')

    x_train, x_test, y_train, y_test = get_train_test(dataset_train, dataset_test, dataset_validate)

    RF, y_pred = train_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, model_name='RF')

    accuracy, precision, recall, f1 = evaluate_model(x_train, x_test, y_train, y_test, y_pred, RF)

    # accuracy, precision, recall, f1 = train_model()

    entry = DataEntry()
    entry.model_updated_accuracy = accuracy
    entry.model_updated_precision = precision
    entry.model_updated_recall = recall
    entry.model_updated_f1 = f1
    entry.model_updated_new_songs_number  = 1
    entry.save()


