from src.generate_features import *
from src.train_model import *
from src.score_model import *
import joblib

dataset_train, dataset_test, dataset_validate, dataset_full = generate_dataset(type='non-nlp')

x_train, x_test, y_train, y_test = get_train_test(dataset_train, dataset_test, dataset_validate)

RF, y_pred = train_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, model_name='RF')

accuracy, precision, recall, f1 = evaluate_model(x_train, x_test, y_train, y_test, y_pred, RF)

filename = 'deploy/model-spotify.sav'
joblib.dump(RF, filename)
