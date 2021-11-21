from create_datasets import *
from utils import *

from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns

from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_predict, train_test_split, ParameterGrid
from sklearn.preprocessing import StandardScaler, Normalizer, RobustScaler

import joblib

# Visualitzarem només 3 decimals per mostra
pd.set_option('display.float_format', lambda x: '%.3f' % x)

indep_columns = ['danceability', 'energy', 'key', 'loudness',
       'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'duration_ms', 'time_signature', 'chorus_hit',
       'sections']
#create two var lists, one with Spotify's features (spfeatures_var_list) and one with the song traits (song_traits_var_list)
spfeatures_var_list = ['danceability', 'energy', 'key', 'loudness','mode', 'speechiness', 'acousticness', 
                       'instrumentalness', 'liveness','valence']
song_traits_var_list = ['key', 'loudness','tempo', 'time_signature', 'chorus_hit','sections'] 
#duration_ms has been removed since it has such larger numbers than the other variables 

# columns_to_drop  = ['track','artist','uri','key','mode','speechiness','acousticness','instrumentalness','liveness','tempo','duration_ms','chorus_hit','sections']
# columns_to_drop  = ['track','artist','uri']
columns_to_drop  = ['track','artist','uri', 'chorus_hit','sections' ]
# columns_to_drop  = ['track','artist','uri','key','mode','speechiness','liveness','tempo','duration_ms','chorus_hit','sections']
# dataset_full = get_full_dataset()
dataset_train, dataset_test, dataset_validate = get_dataset_flushed(train_size=0.8, validate_size=0.0, columns_to_drop=columns_to_drop)

# all_songs_hits = dataset_train[spfeatures_var_list].loc[dataset_train['target'] == 1]

# all_songs_flops = dataset_train[spfeatures_var_list].loc[dataset_train['target'] == 0]

# #create a dataframe that includes the means for hits and flops
# hits_means = pd.DataFrame(all_songs_hits.describe().loc['mean'])
# flops_means = pd.DataFrame(all_songs_flops.describe().loc['mean'])
# means_joined = pd.concat([hits_means,flops_means], axis = 1)
# means_joined.columns = ['hit_mean', 'flop_mean']

# ss = StandardScaler()
# means_joined_scaled = pd.DataFrame(ss.fit_transform(means_joined),index= means_joined.index, columns = means_joined.columns)
# means_joined_scaled


# means_joined_scaled.plot(kind = 'bar', figsize=(10, 5), color = ('purple', 'grey'), title = 'Means of Hit Songs and Flop Songs for Song Features')
# plt.legend(labels=['Hits', 'Flops'], loc='upper right')
# plt.show()
# plt.show()

#create histograpms of all the variables to see distributions
# fig, ax = plt.subplots(5,3, figsize=(5,5))

# def hist_plot(row, column, variable, binsnum, color):
#     ax[row, column].hist(dataset_train[variable], bins = binsnum, color = color)
#     ax[row, column].set_title(variable + ' histogram')
    
# hist_plot(0, 0, 'danceability', 10, 'purple')
# hist_plot(0, 1, 'energy', 10, 'orchid')
# hist_plot(0, 2, 'key', 10, 'plum')
# hist_plot(1,0, 'loudness', 10, 'purple')
# hist_plot(1,1, 'mode', 10, 'orchid')
# hist_plot(1,2, 'speechiness', 10, 'plum')
# hist_plot(2,0, 'acousticness', 10, 'purple')
# hist_plot(2,1, 'instrumentalness', 10, 'orchid')
# hist_plot(2,2, 'liveness', 10, 'plum')
# hist_plot(3,0, 'valence', 10, 'purple')
# hist_plot(3,1, 'tempo', 10, 'orchid')
# hist_plot(3,2, 'duration_ms', 50, 'plum')
# hist_plot(4,0, 'time_signature', 10, 'purple')
# hist_plot(4,1, 'chorus_hit', 10, 'orchid')
# hist_plot(4,2, 'sections', 50, 'plum')

# plt.show()

x_train = dataset_train.drop(['target'], 1).values  # values converts it into a numpy array
y_train = dataset_train['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

x_test = dataset_test.drop(['target'], 1).values  # values converts it into a numpy array
y_test = dataset_test['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

x_val = dataset_validate.drop(['target'], 1).values  # values converts it into a numpy array
y_val = dataset_validate['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

# x = dataset_full.drop(['target'], 1).values  # values converts it into a numpy array
# y = dataset_full['target'].values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

################

# # Step 1: Data Preprocessing
# # Feature Scaling
sc =  StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
# x_val = sc.transform(x_val)

# transformer = Normalizer()
# x_train = transformer.fit_transform(x_train)
# x_test = transformer.fit_transform(x_test)
# x_val = transformer.fit_transform(x_val)


# models = {
#     "Logistic Regression": LogisticRegression(),
#     "K-Nearest Neighbors": KNeighborsClassifier(),
#     "Decision Tree": DecisionTreeClassifier(),
#     "Support Vector Machine (Linear Kernel)": LinearSVC(),
#     "Random Forest": RandomForestClassifier(),
#     "Naive Bayes": GaussianNB(),
#     "Neural Net": MLPClassifier(),
#     "AdaBoost": AdaBoostClassifier(),
#     "Gradient Boosting": GradientBoostingClassifier()
# }

# for name, model in models.items():
#     print(name + " training...")
#     model.fit(x_train, y_train)
#     print(name + " trained.")

# for name, model in models.items():
#     print("###")
#     print(name + ": {:.2f}% accuracy".format(model.score(x_test, y_test) * 100))
#     print("###")
    # print("Model evaluation {0}".format(name))
    # print("###")
    # evaluate_model(y_test, model.predict(x_test))
    # print("###")
    # print("Cross validation {0}".format(name))
    # print("###")
    # cross_val_preds = cross_val_predict(model, x_val, y_val)

RF = RandomForestClassifier()
RF.fit(x_train, y_train)
y_pred = RF.predict(x_test)

# #create a confusion matrix to see the efficacy of the model
# from sklearn import metrics
# cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
# cnf_matrix

# #create a figure/heatmap of the confusion matrix for a better visual
# mpl.rcParams['figure.figsize']=(10,5)
# class_names=[0,1] # name  of classes
# fig, ax = plt.subplots()
# tick_marks = np.arange(len(class_names))
# plt.xticks(tick_marks, class_names)
# plt.yticks(tick_marks, class_names)
# # create heatmap
# sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="RdPu" ,fmt='g')
# ax.xaxis.set_label_position("top")
# plt.tight_layout()
# plt.title('Confusion matrix', y=1.1)
# plt.ylabel('Actual label')
# plt.xlabel('Predicted label')
# plt.show()

#create a dataframe of the feature importances to determine which variables are the most important in determining a hit
# all_songs_feat = RF.feature_importances_
# df_indep_columns = pd.DataFrame(indep_columns)
# df_all_songs_feat = pd.DataFrame(all_songs_feat)
# all_songs_feat_vars = pd.concat([df_indep_columns, df_all_songs_feat], axis = 1)
# all_songs_feat_vars.columns = ['Variable', 'Feature importance all decades']
# all_songs_feat_vars = all_songs_feat_vars.set_index('Variable')
# all_songs_feat_vars = all_songs_feat_vars.sort_values(by=['Feature importance all decades'], ascending = False)
# all_songs_feat_vars
# all_songs_feat_vars.to_csv('all_songs_feat.csv', index = False) #create a CSV file of the new dataframe

# all_songs_feat_vars.plot(kind='bar', color = "purple", title = "Most important features for predicting hit and flop songs for all decades", legend = None)
# plt.ylabel('Feature importance')
# plt.show()

print("Accuracy:",accuracy_score(y_test, y_pred)*100)
print("Precision:", precision_score(y_test, y_pred)*100)
print("Recall:", recall_score(y_test, y_pred)*100)
print("F1 score:", f1_score(y_test, y_pred))
print ('Training MSE: ', np.mean((RF.predict(x_train) - y_train)**2))
print ('Test model MSE', np.mean((RF.predict(x_test) - y_test)**2)) 

filename = 'deploy/model-spotify.sav'
joblib.dump(RF, filename)