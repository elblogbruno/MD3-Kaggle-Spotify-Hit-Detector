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


def train_model(dataset_train, dataset_test, dataset_validate):
    """ retrain model with new song """
    x_train = dataset_train.drop(['target'], 1).values  # values converts it into a numpy array
    y_train = dataset_train['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

    x_test = dataset_test.drop(['target'], 1).values  # values converts it into a numpy array
    y_test = dataset_test['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

    sc =  StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    RF = RandomForestClassifier()
    RF.fit(x_train, y_train)
    y_pred = RF.predict(x_test)

    return x_train, x_test, y_train, y_test, y_pred, RF