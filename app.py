from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import markdown2
from database import init_db, insert_data, fetch_all_data, fetch_map_data
import json
import google.generativeai as genai

genai.configure(api_key="AIzaSyBP4ThpGB9BNfEZGp_4IcOYafRXcxuP6Q4")
model = genai.GenerativeModel('gemini-1.5-pro')

def analyze_latest_data_with_gemini(latest_data):
    prompt = f"""
    Analyze the provided river water sensor dataset and identify any abnormalities or potential risks based on key parameters such as pH, turbidity, TDS, water temperature, air temperature, and humidity. Confirm the absence of abnormalities if all parameters are within safe ranges. Only proceed with further instructions if abnormalities are detected.
Important Conditions:
If all parameters are within safe environmental ranges, confirm their normalcy.
Suggest maintenance measures only if all parameters are safe.
If even one parameter exceeds safe limits, identify it explicitly.
Instructions:
Problem Analysis:
Summarize the major issues detected in the dataset.
Focus on deviations from established safe environmental ranges critical for river water health.
Clearly state which parameters are abnormal and specify where the risks are highest.
Ensure a precise and professional tone.
Possible Causes:
Provide 4 possible causes with concise explanations.
Recommended Remedies:
Propose 4 practical remedies to mitigate the identified risks.
Output Format:
Structure the response into three clearly separated sections:
Problem Analysis (4 bullet points)
Possible Causes (4 bullet points)
Recommended Remedies (4 bullet points)
Use formal and professional language.
Maintain clarity and conciseness.
Strictly do not mix causes with remedies.
Sensor Data Provided:
pH: {latest_data['ph']}
Turbidity: {latest_data['turbidity']}
Water Temperature: {latest_data['temperature_water']}
TDS: {latest_data['tds']}
Air Temperature: {latest_data['temperature_air']}
Air Humidity: {latest_data['humidity_air']}"""

    response = model.generate_content(prompt)
    return response.text

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/get_latest_data', methods=['GET'])
def get_latest_data():
    try:
        rows = fetch_all_data()
        if not rows:
            return jsonify({'status': 'error', 'message': 'No data found'}), 404

        latest_row = rows[-1]
        latest_data = {
            'ph': latest_row[4],
            'turbidity': latest_row[5],
            'temperature_water': latest_row[6],
            'tds': latest_row[7],
            'temperature_air': latest_row[9],
            'humidity_air': latest_row[10],
        }
        return jsonify(latest_data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        insert_data(data)
        socketio.emit('new_data', {'status': 'new_data_received'})
        return jsonify({'status': 'success', 'message': 'Data inserted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/data', methods=['GET'])
def get_data():
    try:
        rows = fetch_all_data()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/map', methods=['GET'])
def map_view():
    try:
        coords = fetch_map_data()
        data = [
            {
                "latitude": row[0],
                "longitude": row[1],
                "timestamp": row[2],
                "temperature_water": row[3],
                "ph": row[4],
                "turbidity": row[5],
                "gas": row[6]
            }
            for row in coords
        ]
        return render_template('map.html', sensor_data=json.dumps(data))
    except Exception as e:
        return f"Error loading map: {str(e)}"

# ---- CHANGES START HERE ----

# Serve genai.html with spinner and JavaScript
@app.route('/genai', methods=['GET'])
def genai_page():
    return render_template('genai.html')

# Separate API route for slow GenAI work
@app.route('/get_genai_analysis', methods=['GET'])
def get_genai_analysis():
    try:
        rows = fetch_all_data()
        if not rows:
            return "No data available for analysis."

        latest_row = rows[-1]
        latest_data = {
            'ph': latest_row[4],
            'turbidity': latest_row[5],
            'temperature_water': latest_row[6],
            'tds': latest_row[7],
            'temperature_air': latest_row[9],
            'humidity_air': latest_row[10],
        }

        analysis_result = analyze_latest_data_with_gemini(latest_data)
        analysis_html = markdown2.markdown(analysis_result)
        return analysis_html
    except Exception as e:
        return f"Error in GenAI analysis: {str(e)}"

# ---- CHANGES END HERE ----

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True, host='0.0.0.0')

