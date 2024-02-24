from flask import Flask, request, render_template
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load('models/model.pkl')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        pclass = request.form['pclass']
        sex = request.form['sex']
        age = int(request.form['age'])
        sibsp = int(request.form['sibsp'])
        parch = int(request.form['parch'])
        fare = float(request.form['fare'])
        embarked = request.form['embarked']
        class_ = 'First' # will be dropped
        who = request.form['who']
        adult_male = True if who == 'men' else False
        deck = 'C' # will be dropped
        embark_town = 'Southampton' # will be dropped
        alive = 'yes' # will be dropped
        alone = True if (sibsp > 0 or parch > 0) else False

    try:
        data = {'pclass': [pclass],
            'sex': [sex],
            'age': [age],
            'sibsp': [sibsp],
            'parch': [parch],
            'fare': [fare],
            'embarked': [embarked],
            'class': [class_],
            'who': [who],
            'adult_male': [adult_male],
            'deck': [deck],
            'embark_town': [embark_town],
            'alive': [alive],
            'alone': [alone]}

        df = pd.DataFrame(data)

        df.drop('deck', axis=1, inplace=True)                
        df.drop(['class', 'embark_town', 'alive'], axis=1, inplace=True)
        df['sex'] = df['sex'].map({'male':0,'female':1})
        df['embarked'] = df['embarked'].map({'S':0,'C':1,'Q':2})
        df['who'] = df['who'].map({'man':0,'woman':1,'child':2})      

        scaler = joblib.load('models/scaler.pkl')
        df_scaled = scaler.transform(df)
        prediction = model.predict(df_scaled)
        return f'{"Le passager aurait survécu" if prediction == 1 else "Le passager n aurait pas survécu"}'
    except Exception as e:
        return f'Error, fill the form again (Exception: {e})'
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
