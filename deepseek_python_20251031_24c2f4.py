from flask import Flask, render_template, request, jsonify
from ml_model.train_model import PredictiveMaintenanceModel
import sqlite3
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        sensor_data = [
            data['temperature'],
            data['pressure'], 
            data['vibration'],
            data['rotation_speed'],
            data['tool_wear']
        ]
        
        model = PredictiveMaintenanceModel()
        failure_probability = model.predict_failure(sensor_data)
        
        # Store prediction in database
        store_prediction(data, failure_probability)
        
        return jsonify({
            'failure_probability': round(failure_probability, 4),
            'alert': failure_probability > 0.7
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def store_prediction(sensor_data, probability):
    conn = sqlite3.connect('../database/sensor_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO predictions (temperature, pressure, vibration, rotation_speed, tool_wear, failure_probability)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        sensor_data['temperature'],
        sensor_data['pressure'],
        sensor_data['vibration'], 
        sensor_data['rotation_speed'],
        sensor_data['tool_wear'],
        probability
    ))
    
    conn.commit()
    conn.close()

@app.route('/api/history')
def get_history():
    conn = sqlite3.connect('../database/sensor_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT timestamp, failure_probability FROM predictions 
    ORDER BY timestamp DESC LIMIT 50
    ''')
    
    history = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'timestamp': row[0],
        'probability': row[1]
    } for row in history])

if __name__ == '__main__':
    app.run(debug=True)