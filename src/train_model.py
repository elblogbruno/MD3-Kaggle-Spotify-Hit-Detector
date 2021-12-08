from src.score_model import *

from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_predict, train_test_split, ParameterGrid
from sklearn.preprocessing import StandardScaler, Normalizer, RobustScaler

def split_dataset(dataset):
    """ split dataset into train, test, validate """
    dataset_train, dataset_test, dataset_validate = train_test_split(dataset, test_size=0.2, random_state=0)
    return dataset_train, dataset_test, dataset_validate

def get_train_test(dataset_train=None, dataset_test=None, dataset_validate=None, dataset_full=None):
    if dataset_full is not None:
        x = dataset_full.drop(['target'], 1).values  # values converts it into a numpy array
        y = dataset_full['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=0)
        return x_train, x_test, y_train, y_test
    
    x_train = dataset_train.drop(['target'], 1).values  # values converts it into a numpy array
    y_train = dataset_train['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

    x_test = dataset_test.drop(['target'], 1).values  # values converts it into a numpy array
    y_test = dataset_test['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column
    
    return x_train, x_test, y_train, y_test

def train_model(x_train, y_train, x_test, y_test, model_name, params=None):
    """ retrain model with new song """
    sc =  StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)
    
    if params:
        RF = RandomForestClassifier(**params)
    else:
        RF = RandomForestClassifier()

    RF.fit(x_train, y_train)
    y_pred = RF.predict(x_test)

    return RF, y_pred