from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Path to save the settings
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')

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

        return jsonify({"message": "Settings saved successfully!", "settings": settings}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-settings', methods=['GET'])
def get_settings():
    if not os.path.exists(SETTINGS_FILE):
        return jsonify({"error": "Settings file not found!"}), 404
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
