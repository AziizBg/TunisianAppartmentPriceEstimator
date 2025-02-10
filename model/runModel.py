from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
import pandas as pd

app = Flask(__name__)
# Enable CORS for the specific route
CORS(app, resources={r"/predict": {"origins": "http://localhost:4200"}})

# Load the model
model_path = os.path.join(os.path.dirname(
    __file__), 'best_apartment_price_model7.pkl')
model = joblib.load(model_path)


@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)

    # Convert data into DataFrame
    new_data = pd.DataFrame([data['input']])

    boolean_features = ['elevator', 'equipped_kitchen', 'balcony', 'heating', 'air_conditioning', 'parking', 'garage']
    for feature in boolean_features:
        new_data[feature] = new_data[feature].map({'yes': 1, 'no': 0})

    new_data['surface_bedrooms'] = new_data['surface'] * new_data['bedrooms']

    # Example: Create polynomial features
    new_data['surface_squared'] = new_data['surface'] ** 2

    new_data['bedrooms_squared'] = new_data['bedrooms'] ** 2

    # Create hierarchical feature
    new_data['hierarchical_loc'] = new_data['state'] + '_' + new_data['delegation'] + '_' + new_data['municipality']

    # Interaction between delegation and surface (encode delegation first)
    new_data['municipality_encoded'] = new_data['municipality'].astype('category').cat.codes
    new_data['municipality_surface_interaction'] = new_data['surface'] * new_data['municipality_encoded']

    # Feature for luxury count (number of luxury amenities)
    new_data['luxury_count'] = new_data[
        ['elevator', 'equipped_kitchen', 'balcony', 'heating', 'air_conditioning', 'parking', 'garage']].sum(axis=1)

    # Make prediction
    prediction = model.predict(new_data)

    # Extract the single element from the prediction array
    prediction_value = int(prediction[0])

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction_value})


if __name__ == '__main__':
    app.run(debug=True)
