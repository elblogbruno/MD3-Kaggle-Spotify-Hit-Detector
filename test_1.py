from joblib.logger import PrintTime
from create_datasets import *
from utils import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import GridSearchCV

import warnings
warnings.filterwarnings("ignore")

def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    errors = abs(predictions - test_labels)
    mape = 100 * np.mean(errors / test_labels)
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))
    
    return accuracy

decades = ['60', '70', '80', '90', '00', '10']
# decades = ['00']
# Create the parameter grid based on the results of random search 
param_grid = {
    'bootstrap': [True],
    'criterion': ['gini', 'entropy'],
    'max_depth': [80, 90, 100, 110],
    'max_features': [2, 3],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [100, 200, 300, 1000]
}


for decade in decades:
    print("Year {0} ".format(decade))
    dataset_train = get_dataset_year(year=decade)

    x = dataset_train.drop(['target'], 1).values  # values converts it into a numpy array
    y = dataset_train['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)

    sc =  StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    RF = RandomForestClassifier(bootstrap=True, max_depth=80, max_features=3, min_samples_leaf=3, min_samples_split=10, n_estimators=300)
    # RF.fit(x_train, y_train)
    # y_pred = RF.predict(x_test)

    # print("Accuracy:",accuracy_score(y_test, y_pred))
    # print("Precision:", precision_score(y_test, y_pred))
    # print("Recall:", recall_score(y_test, y_pred))
    # print("F1 score:", f1_score(y_test, y_pred))


    grid_search = GridSearchCV(estimator = RF, param_grid = param_grid, 
                          cv = 3, n_jobs = -1, verbose = 2)

    grid_search.fit(x_train, y_train)
    print(grid_search.best_params_)

    best_grid = grid_search.best_estimator_
    grid_accuracy = evaluate(best_grid, x_train, y_train)

    print('Improvement of {:0.2f}%.'.format( 100 * (grid_accuracy - base_accuracy) / base_accuracy))