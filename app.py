from flask import Flask, request, render_template
import joblib
import pickle
import numpy as np

app = Flask(__name__)
model = joblib.load('rf_tuned.pkl')  # Load the model

@app.route('/')
def home():
    return render_template('index.html')

from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the saved MultiOutput Random Forest model
model = joblib.load('rf_tuned.pkl')

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
        prediction = model.predict(features)[0]  # Returns [fuel, co2]

        fuel_consumption = round(prediction[0], 2)
        co2_emission = round(prediction[1], 2)

        return render_template(
            'index.html',
            fuel=f"{fuel_consumption} Lit.",
            co2=f"{co2_emission} Kg."
        )

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
