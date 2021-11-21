from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

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