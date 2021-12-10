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

        sc =  StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)
        
        return x_train, x_test, y_train, y_test
    
    x_train = dataset_train.drop(['target'], 1).values  # values converts it into a numpy array
    y_train = dataset_train['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

    x_test = dataset_test.drop(['target'], 1).values  # values converts it into a numpy array
    y_test = dataset_test['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column
    
    sc =  StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

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

def hyperparameter_search(x_train, y_train, x_test, y_test, model_name, params=None):
    """ retrain model with new song """
    sc =  StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)
    
    # use grid search to find best parameters for random forest

    from skopt import BayesSearchCV

    from skopt.space import Real, Categorical, Integer

    # log-uniform: understand as search over p = exp(x) by varying x
    opt = BayesSearchCV(
        RandomForestClassifier(),
        {
            'n_estimators': Integer(1, 500),
            'max_depth': Integer(1, 20),
            'max_features': Categorical(['auto', 'sqrt', 'log2']),
            'min_samples_split': Integer(2, 20),
            'min_samples_leaf': Integer(1, 20),
            'bootstrap': Categorical([True, False]),
            'criterion': Categorical(['gini', 'entropy']),
        },
        n_iter=32,
        random_state=0,
        verbose=2
    )

    # executes bayesian optimization
    _ = opt.fit(x_train, y_train)

    # model can be saved, used for predictions or scoring
    print(opt.score(x_test, y_test))
    print(opt.best_params_)
    print(opt.best_score_)
    print(opt.best_estimator_)

    return opt.score(x_test, y_test), opt.best_params_