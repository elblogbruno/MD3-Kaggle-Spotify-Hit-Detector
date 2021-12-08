from scipy.sparse import data
from src.dataset_utils import *
from src.score_model import *

from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import cross_val_predict, train_test_split, ParameterGrid, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, Normalizer, RobustScaler

import joblib

# Visualitzarem només 3 decimals per mostra
pd.set_option('display.float_format', lambda x: '%.3f' % x)

indep_columns = ['danceability', 'energy', 'key', 'loudness',
       'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'duration_ms', 'time_signature', 'chorus_hit',
       'sections']

dataset_full  = pd.read_csv('dataset_full_token.csv', header=0, delimiter=',')
dataset_full = dataset_full.drop(['Unnamed: 0'], axis=1)
print(dataset_full.isnull().sum())
# count nomber of flops of that artist.

# dataset_train, dataset_test, dataset_validate = get_dataset_flushed(train_size=0.8, validate_size=0.0, columns_to_drop=columns_to_drop)



# #add new column with the number of hits per song
# # dataset_full['hits'] = dataset_full.apply(lambda row: len(dataset_full[(dataset_full['target'] == 1) & (dataset_full['track'] == row['track'])]), axis=1)
# # dataset_full['flops'] = dataset_full.apply(lambda row: len(dataset_full[(dataset_full['target'] == 0) & (dataset_full['track'] == row['track'])]), axis=1)

# # dataset_full.head()
# # freq.plot(20, cumulative=False)

# # print(dataset_full['target'].value_counts())
# # print(dataset_train['target'].value_counts())


# # x_train = dataset_train.drop(['target'], 1).values  # values converts it into a numpy array
# # y_train = dataset_train['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

# # x_test = dataset_test.drop(['target'], 1).values  # values converts it into a numpy array
# # y_test = dataset_test['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

# # x_val = dataset_validate.drop(['target'], 1).values  # values converts it into a numpy array
# # y_val = dataset_validate['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column
dataset_full = dataset_full.drop(['track', 'artist'], axis=1)

x = dataset_full.drop(['target'], 1).values  # values converts it into a numpy array
y = dataset_full['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

################

# # Step 1: Data Preprocessing
# # Feature Scaling
sc =  StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
# x_val = sc.transform(x_val)
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# transformer = Normalizer()
# x_train = transformer.fit_transform(x_train)
# x_test = transformer.fit_transform(x_test)
# x_val = transformer.fit_transform(x_val)

#heatmap
# sns.heatmap(dataset_full.corr(), annot=True)
# plt.show()


RF = RandomForestClassifier()
# # create random forest classifier model
# rf_model = RandomForestClassifier(ccp_alpha=0.0, class_weight=None, criterion='entropy', max_depth=28, max_features='log2', max_leaf_nodes=None, max_samples=None, min_impurity_decrease=0.0,  min_samples_leaf=1, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=None, oob_score=False, random_state=None, verbose=0, warm_start=False)

# # set up random search meta-estimator
# model_params = { 'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 'max_features': ['auto', 'sqrt', 'log2'], 'max_depth': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100], 'bootstrap': [True, False], 'criterion': ['gini', 'entropy']}
# # this will train 100 models over 5 folds of cross validation (500 models total)
# clf = RandomizedSearchCV(rf_model, model_params, n_iter=100, cv=5, random_state=1, verbose=2)

# train the random search meta-estimator to find the best model out of 100 candidates
# model = clf.fit(x_train, y_train)

# # print winning set of hyperparameters
# from pprint import pprint
# pprint(model.best_estimator_.get_params())
RF.fit(x_train, y_train)
y_pred = RF.predict(x_test)

evaluate_model(x_train, x_test, y_train, y_test, y_pred, RF)


filename = 'deploy/model-spotify.sav'
joblib.dump(RF, filename)