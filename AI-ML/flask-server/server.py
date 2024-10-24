from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# Load the trained model during app initialization
model = joblib.load("../predictionModel/trained_model.joblib")


@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'

@app.route('/predict', methods=['POST'])
def predict_json():
    try:
        # Get input data from the JSON request
        data = request.get_json(force=True)
        print("request===",data)
        symptoms_data = pd.DataFrame([data])

        # Extract features for prediction
        # X_new = symptoms_data.drop("prognosis", axis=1)

        # Use the trained model to make predictions
        # predictions = model.predict(symptoms_data)

        probabilities = model.predict_proba(symptoms_data)
        predictions = model.predict(symptoms_data)

        # Add predictions to the original DataFrame
        symptoms_data['predicted_prognosis'] = predictions.tolist()
        symptoms_data['certainty'] = probabilities.max(axis=1) 

        # Return the DataFrame with predictions as JSON
        response_data = {
            'predicted_prognosis': symptoms_data['predicted_prognosis'].iloc[0],
            'certainty': symptoms_data['certainty'].iloc[0]
        }
        # return symptoms_data.to_json(orient='records')
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)})
    


if __name__ == '__main__':
    app.run(debug=True)