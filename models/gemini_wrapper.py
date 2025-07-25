import os
import google.generativeai as genai # type: ignore
import markdown2 # type: ignore

from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate AI explanation
def ai_explaination(fuel_consumption, co2_emission, distance, ship_type, fuel_type, weather, month):
    
    # Initialize the Generative AI model
    ai_model = genai.GenerativeModel("gemini-2.5-pro")

    # Map numerical values to human-readable labels
    ship_map = {0: 'Fishing Trawler', 1: 'Oil Service Boat', 2: 'Surfer Boat', 3: 'Tanker Ship'}
    fuel_map = {0: 'Diesel', 1: 'HFO'}
    month_map = {0: 'April', 1: 'August', 2: 'December', 3: 'February', 4: 'January', 5: 'July', 6: 'June', 7: 'March', 8: 'May', 9: 'November', 10: 'October', 11: 'September'}
    weather_map = {0: 'Calm', 1: 'Moderate', 2: 'Stormy'}

    month_label = month_map.get(month, "Unknown Month")
    fuel_label = fuel_map.get(fuel_type, "Unknown Fuel")
    ship_label = ship_map.get(ship_type, "Unknown Ship")
    weather_label = weather_map.get(weather, "Unknown Weather")

    # Prepare the prompt for the AI model
    base_prompt = f"""
    You are a helpful assistant for a ship efficiency tool.

    Given:
    - Predicted fuel consumption: {fuel_consumption} liters
    - Predicted CO₂ emission: {co2_emission} kilograms
    - Distance: {distance} km
    - Ship Type: {ship_label}
    - Fuel Type: {fuel_label}
    - Weather: {weather_label}
    - Month: {month_label}

    Your tasks:

    1. **Explain the Prediction (2-3 sentences, ≤50 words):**
    Explain in Simple English what the predicted fuel and CO₂ values mean that helps a normal user understand. Focus on cost, environmental impact, and whether it’s normal or high/low based on values. Do not use technical words. Keep it casual like a helpful assistant.

    2. **Give Suggestions to Reduce Emissions (2-3 suggestions):**
    Based on ship type, fuel type, weather, and distance, suggest simple ways to reduce emissions or fuel use. Keep it short and actionable, like "Try switching to diesel in calm weather."

    3. **Generate a Mini Report (2-3 sentences):**
    Write a small English summary report using the values. 
    Follow this example format: "For a 500km trip in stormy weather using a tanker ship, expected fuel is 600L and CO₂ emission is 1600Kg."

    Keep all responses clear, simple, straight-forward, and user-friendly. Make it sound natural and useful for ship operators.
    """

    response = ai_model.generate_content(base_prompt)
    return markdown2.markdown(response.text.strip())