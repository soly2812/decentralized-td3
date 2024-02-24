import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

titanic= sns.load_dataset("titanic")

def traitement(titanic):        
    titanic.drop('deck', axis=1, inplace=True)
    titanic_row=titanic.isnull().sum(axis=1)/titanic.shape[1]*100
    titanic.drop(titanic_row[titanic_row>5].index, axis=0, inplace=True)

    titanic.drop(['class', 'embark_town', 'alive'], axis=1, inplace=True)
    titanic['sex'] = titanic['sex'].map({'male':0,'female':1})
    titanic['embarked'] = titanic['embarked'].map({'S':0,'C':1,'Q':2})
    titanic['who'] = titanic['who'].map({'man':0,'woman':1,'child':2})      
    return titanic

titanic_traited = traitement(titanic=titanic)

def model(titanic):
    X = titanic.drop('survived', axis=1)
    Y=titanic['survived']

    x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size = 0.3, random_state=10)
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train= scaler.transform(x_train)
    x_test= scaler.transform(x_test)
    joblib.dump(scaler, 'scaler.pkl')


    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=10)
    grid_search.fit(x_train, y_train)

    print("Meilleurs paramètres:", grid_search.best_params_)
    print("Meilleure précision:", grid_search.best_score_)
    y_pred = grid_search.best_estimator_.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary')
    f1 = f1_score(y_test, y_pred, average='binary')

    # Affichage des métriques
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")

    joblib.dump(grid_search.best_estimator_, "model.pkl")

model(titanic=titanic_traited)