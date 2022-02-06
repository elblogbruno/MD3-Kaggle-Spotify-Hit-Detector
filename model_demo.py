from src.generate_features import *
from src.train_model import *
from src.score_model import *
from deploy.spotipy_api import *
import joblib

filename = 'model/model-spotify-full-dataset-no-nlp.sav'
model = joblib.load(filename)

# You can generate features for an specific spotify song
# song_x_data = get_data_for_new_song('https://open.spotify.com/track/0BzhS74ByIVlyz8BedHaYi?si=13b7304e6c264662', datetime.now())

dataset_train, dataset_test, dataset_validate, dataset_full = generate_dataset(type='non-nlp')
x_train, x_test, y_train, y_test = get_train_test(dataset_train, dataset_test, dataset_validate)

y_pred = model.predict(x_test)
accuracy, precision, recall, f1 = evaluate_model(x_train, x_test, y_train, y_test, y_pred, model)