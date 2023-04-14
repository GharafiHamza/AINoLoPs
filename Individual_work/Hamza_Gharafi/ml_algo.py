from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV


def rf_classifier_hpt(X_train, y_train, X_test, y_test):
    rf_classifier = RandomForestClassifier()


    param_grid = {
        'n_estimators': [10, 50, 100],  
        'max_depth': [None, 10, 20],     
        'min_samples_split': [2, 5, 10], 
        'min_samples_leaf': [1, 2, 4]    
    }

    grid_search = GridSearchCV(rf_classifier, param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    best_rf_classifier = RandomForestClassifier(**best_params)
    best_rf_classifier.fit(X_train, y_train)

    test_accuracy = best_rf_classifier.score(X_test, y_test)

    print("Best Hyperparameters: ", best_params)
    print("Best Mean Cross-validation Score: ", best_score)
    print("Test Accuracy: ", test_accuracy)
    
    return best_params, best_score, test_accuracy


def rf_classifier(X_train, y_train, X_test, y_test):
    
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    
    rf_classifier.fit(X_train, y_train)

    predicted_labels = rf_classifier.predict(X_test)

    accuracy = accuracy_score(y_test, predicted_labels)
    classification_report_s = classification_report(y_test, predicted_labels)
    print("Accuracy: {:.2f}%".format(accuracy * 100))
    print("Classification Report:\n", classification_report_s)
    
    return accuracy, classification_report_s



def lr_classifier(X_train, y_train, X_test, y_test, C=1.0):
    
    clf = LogisticRegression(C=C)
    
    clf.fit(X_train, y_train)
    
    y_train_pred = clf.predict(X_train)
    y_test_pred = clf.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    print("Train Accuracy: ", train_accuracy)
    print("Test Accuracy: ", test_accuracy)

    return train_accuracy, test_accuracy

def lr_classifier_hpt(X_train, y_train, X_test, y_test):
    
    param_grid = {
        'C': [0.001, 0.01, 0.1, 1, 10] 
    }

    logreg = LogisticRegression()

    grid_search = GridSearchCV(logreg, param_grid, cv=5)
    grid_search.fit(X_train, y_train) 
    
    best_C = grid_search.best_params_['C']
    best_score = grid_search.best_score_

    best_logreg = LogisticRegression(C=best_C)
    best_logreg.fit(X_train, y_train)

    test_accuracy = best_logreg.score(X_test, y_test)

    return best_C, best_score, test_accuracy

def nb_classifier(X_train, y_train, X_test, y_test):

    nb = MultinomialNB()
    nb.fit(X_train, y_train)

    y_pred = nb.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1_score = f1_score(y_test, y_pred, average='weighted')

    return accuracy, precision, recall, f1_score

def svm_classifier(X_train, y_train, X_test, y_test, kernel='linear', C=1.0):

    svm = SVC(kernel=kernel, C=C)
    svm.fit(X_train, y_train)

    y_pred = svm.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    return accuracy

def svm_classifier_hpt(X_train, y_train, X_test, y_test):
    
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    param_grid = {'C': [0.1, 1, 10, 100],
                  'kernel': ['linear', 'poly', 'rbf', 'sigmoid']}
    svm = SVC()
    grid_search = GridSearchCV(svm, param_grid, cv=5)
    grid_search.fit(X_train_vectorized, y_train)

    best_C = grid_search.best_params_['C']
    best_kernel = grid_search.best_params_['kernel']

    svm = SVC(kernel=best_kernel, C=best_C)
    svm.fit(X_train_vectorized, y_train)

    y_pred = svm.predict(X_test_vectorized)

    accuracy = accuracy_score(y_test, y_pred)

    return accuracy
