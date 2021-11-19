from create_datasets import *
from matplotlib import pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import cross_val_predict

from sklearn.preprocessing import StandardScaler

# Visualitzarem només 3 decimals per mostra
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def evaluate_model(y_true, y_preds):
    p_score = precision_score(y_true, y_preds)
    r_score = recall_score(y_true, y_preds)
    f1 = f1_score(y_true, y_preds)
    cfmatrix = confusion_matrix(y_true, y_preds)
    accuracy_score_ = accuracy_score(y_true, y_preds)

    print("Precission: "  + str(p_score))
    print("Recall: " + str(r_score))
    print("F1: " + str(f1))
    print("Accuracy: " + str(accuracy_score_))
    
def print_dataset(model, x_train, y_train, x_test, y_test):
    # Step 4: Evaluate the model
    # p_pred = model.predict_proba(x_train)
    y_pred = model.predict(x_train)
    score_ = model.score(x_train, y_train)
    accuracy_score_ = accuracy_score(y_train, y_pred)
    # conf_m = confusion_matrix(y_train, y_pred)
    # report = classification_report(y_train, y_pred)

    print("Score: ", score_)
    print("Accuracy: ", accuracy_score_)
    # print("Confusion Matrix: \n", conf_m)
    # print("Classification Report: \n", report)

dataset_train, dataset_test, dataset_validate = get_dataset_flushed(train_size=0.8, test_size=0.1)

# y_train = dataset_train['target'].values.reshape(1,-1)
# x_train = dataset_train.drop('target', axis=1).values.ravel()

x_train = dataset_train.iloc[:, 0:16].values.reshape(-1, 1)  # values converts it into a numpy array
y_train = dataset_train.target.values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

# y_test = dataset_test['target'].values.reshape(1,-1)
# x_test = dataset_test.drop('target', axis=1).values.ravel()

x_test = dataset_test.iloc[:, 0:16].values.reshape(-1, 1)  # values converts it into a numpy array
y_test = dataset_test.target.values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column

# y_val = dataset_validate['target'].values.reshape(1,-1)
# x_val = dataset_validate.drop('target', axis=1).values.ravel()

x_val = dataset_validate.iloc[:, 0:16].values.reshape(-1, 1)  # values converts it into a numpy array
y_val = dataset_validate.target.values.ravel()  # -1 means that calculate the dimension of rows, but have 1 column


# # Step 1: Data Preprocessing
# # Feature Scaling
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
x_val = sc.transform(x_val)

# ##############################
# print("###")
# print("Logistic regression witouth DG and witouth standarzing")
# print("###")
# log_reg = LogisticRegression().fit(x_train, y_train)
# y_pred = log_reg.predict(x_test)
# evaluate_model(y_test, y_pred)
# print("###")
# print("Logistic regression witouth DG with standarzing")
# print("###")
# # x_train_scaled = preprocessing.scale(x_train)
# scaler = StandardScaler()
# scaler.fit(x_train)
# X_train = scaler.transform(x_train)
# X_test = scaler.transform(x_test)

# log_reg = LogisticRegression().fit(X_train, y_train)
# y_pred = log_reg.predict(X_test)
# evaluate_model(y_test, y_pred)
# print("###")
# print("Cross validation")
# print("###")
# cross_val_preds = cross_val_predict(log_reg, x_val, y_val)

# evaluate_model(y_val, cross_val_preds)

models = {
    "Logistic Regression": LogisticRegression(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "Support Vector Machine (Linear Kernel)": LinearSVC(),
    "Random Forest": RandomForestClassifier()
}

for name, model in models.items():
    model.fit(x_train, y_train)
    print(name + " trained.")

for name, model in models.items():
    print(name + ": {:.2f}%".format(model.score(x_test, y_test) * 100))
    # print("###")
    # print("Model evaluation {0}".format(name))
    # print("###")
    # evaluate_model(y_test, model.predict(x_test))
    # print("###")
    # print("Cross validation {0}".format(name))
    # print("###")
    # cross_val_preds = cross_val_predict(model, x_val, y_val)

    # evaluate_model(y_val, cross_val_preds)