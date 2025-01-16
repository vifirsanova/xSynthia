#!/usr/bin/env python3
import subprocess
from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import os

app = Flask(__name__, static_folder='static')

# Path to save the settings
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-settings', methods=['POST'])
def save_settings():
    try:
        # Extract form data
        model = request.form.get('model')
        samples = request.form.get('samples')
        associations = request.form.get('associations')
        starting_point = request.form.get('startingPoint')
        random_seed_value = request.form.get('randomSeedValue')
        word_list = request.form.get('wordList')
        visualization_levels = request.form.get('visualizationLevels')
        graph_type = request.form.get('graphType')

        # Determine starting details
        starting_details = None
        if starting_point == 'randomSeed':
            starting_details = random_seed_value
        elif starting_point == 'setWord':
            starting_details = word_list

        # Structure the data
        settings = {
            "model": model,
            "samples": samples,
            "associations": associations,
            "starting_point": starting_point,
            "starting_details": starting_details,
            "visualization_levels": visualization_levels,
            "graph_type": graph_type,
        }

        # Save the settings to a JSON file
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)

        # Run the external Python script
        script_path = os.path.join(os.path.dirname(__file__), 'run_analysis.py')
        process = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True
        )

        # Check for errors in the script execution
        if process.returncode != 0:
            return jsonify({
                "message": "Settings saved, but an error occurred while running the script.",
                "error": process.stderr
            }), 500

        # Return the output of the script
        return jsonify({
            "message": "Settings saved and script executed successfully!",
            "script_output": process.stdout
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
