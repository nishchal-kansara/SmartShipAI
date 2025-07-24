from flask import Flask, request, render_template
import joblib
import numpy as np

from models.gemini_wrapper import ai_explaination

app = Flask(__name__)
ml_model = joblib.load('models/rf_tuned.pkl')  # Load the saved MultiOutput Random Forest model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Read form inputs (make sure these names match HTML form fields!)
        distance = int(request.form['distance'])
        ship_type = int(request.form['ship_type_encoded'])
        month = int(request.form['month_encoded'])
        fuel_type = int(request.form['fuel_type_encoded'])
        weather = int(request.form['weather_conditions_encoded'])

        # Arrange features in same order used during training
        features = np.array([[distance, fuel_type, month, weather, ship_type]])

        # Predict using the multi-output model
        prediction = ml_model.predict(features)[0]  # Returns [fuel, co2]

        fuel_consumption = round(prediction[0], 2)
        co2_emission = round(prediction[1], 2)

        # AI explanation using Generative AI model
        analysis = ai_explaination(
            fuel_consumption, co2_emission, distance,
            ship_type, fuel_type, weather, month
        )
        
        return render_template(
            'index.html',
            fuel=f"{fuel_consumption} Lit.",
            co2=f"{co2_emission} Kg.",
            analysis=analysis
        )

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
