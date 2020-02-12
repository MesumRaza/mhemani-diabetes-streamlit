from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import pandas as pd

from sklearn.externals import joblib


# Get headers for payload
headers = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction', 'Age']

# Use pickle to load in the pre-trained model
model = joblib.load("diabeteseModel.pkl")
    
# Test model with data frame
input_variables = pd.DataFrame([[1, 106, 70, 28, 135, 34.2, 0.142, 22]],
                                columns=headers, 
                                dtype=float,
                                index=['input'])

# Get the model's prediction
prediction = model.predict(input_variables)
print("Prediction: ", prediction)
prediction_proba = model.predict_proba(input_variables)
print("Probabilities: ", prediction_proba)

app = Flask(__name__)
CORS(app)

@app.route("/api_diabetes", methods=['POST'])
def predict():
    payload = request.json['data'] 
    #print(payload)
    values = [float(i) for i in payload.split(',')]
    
    input_variables = pd.DataFrame([values],
                                columns=headers, 
                                dtype=float,
                                index=['input'])    
    
    # Get the model's prediction
    prediction = model.predict(input_variables)
    print("Prediction: ", prediction)
    prediction_proba = model.predict_proba(input_variables)[0][1]
    print("Probabilities: ", prediction_proba)

    ret = '{"prediction":' + str(float(prediction)) +","+ '"prediction_proba":' + str(float(prediction_proba))  + '}'

    print (ret)
    
    return ret

if __name__ == "__main__":
    app.run(debug=True)