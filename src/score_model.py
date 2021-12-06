from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np

def evaluate_model(x_train, x_test, y_train, y_test, y_pred, model):
    p_score = precision_score(y_test, y_pred)
    r_score = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    # cfmatrix = confusion_matrix(y_test, y_pred)
    accuracy_score_ = accuracy_score(y_test, y_pred)

    print("Accuracy:", accuracy_score_*100)
    print("Precision:", p_score*100)
    print("Recall:", r_score*100)
    print("F1 score:", f1)
    print ('Training MSE: ', np.mean((model.predict(x_train) - y_train)**2))
    print ('Test model MSE', np.mean((model.predict(x_test) - y_test)**2)) 

    return accuracy_score_, p_score, r_score, f1

    
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