from src.generate_features import *
from src.train_model import *
from src.score_model import *
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


dataset_train, dataset_test, dataset_validate, dataset_full = generate_dataset(type='non-nlp')

# dataset_full = generate_dataset(type='nlp', test=1)

x_train, x_test, y_train, y_test = get_train_test(dataset_train, dataset_test, dataset_validate)
# x_train, x_test, y_train, y_test = get_train_test(dataset_full=dataset_full)


RF, y_pred = train_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, model_name='RF')

print(RF.n_features_)
# score = hyperparameter_search(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, model_name='RF')

accuracy, precision, recall, f1 = evaluate_model(x_train, x_test, y_train, y_test, y_pred, RF)

# we save the model.
filename = 'model/model-spotify-full-dataset-no-nlp.sav'
# filename = 'model/model-spotify-full-dataset-nlp.sav'

joblib.dump(RF, filename)
