import os, toml, json, re
from flask import Flask, render_template, request, jsonify, send_from_directory
from xsynthia.gen import Model, Graph
from xsynthia.utils import extract_text_from_file
app = Flask(__name__)

def save_config(data):
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    # Save as toml
    os.makedirs('xsynthia', exist_ok=True)
    config_path = os.path.join('xsynthia', 'config.toml')
        
    with open(config_path, 'w') as config_file:
        toml.dump(data, config_file)

ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/graph_with_predicates.html')
def serve_graph():
    return send_from_directory('uploads', 'graph_with_predicates.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    # Get prompt
    data = request.get_json()
    user_message = data.get('message', '').strip()
    # Prompt from LLM
    model = Model()
    if 'question' in user_message:
        with open('uploads/graph.json', 'r') as file:
            graph_data = json.load(file)
        with open('uploads/text.txt', 'r') as f:
            content = f.read()
        res = model.generate('prompts/qa_prompt.txt', str(graph_data)+'\nTEXT:'+content+'\nUSER:'+user_message)
        return jsonify({'message': res})
    else:
        # Parse config
        res = model.generate('prompts/parse_config.txt', user_message)
        json_matches = re.findall(r'```json\s*([\s\S]*?)\s*```', res)[0] 
        try:
            data = json.loads(json_matches)
        except json.JSONDecodeError:
            pass
        # Save config file
        save_config(data)
        # Form model respose
        response = {'message': f'Successfully saved automatically parsed config: {data}. Now you can attach your file with unstructured data in *.docx/*.doc/*.txt/*.pdf, and I will create a graph database for you!'}

        # debug
        return jsonify(response)

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    # Get parameters from manual settings
    data = request.get_json()
    save_config(data)
    return jsonify({"message": f"Successfully saved manual config: {data}. Now you can attach your file with unstructured datain *.docx/*.doc/*.txt/*.pdf, and I will create a graph database for you!"})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            os.makedirs('uploads', exist_ok=True)
            content = extract_text_from_file(file.stream, file.filename)
            print(content)
            with open('uploads/text.txt', 'w') as f:
                f.write(content)
            # Prompt from LLM
            model = Model()
            # Parse config
            res = model.generate('prompts/form_tripets.txt', content)
            json_matches = re.findall(r'```json\s*([\s\S]*?)\s*```', res)[0]

            try:
                json_matches = re.findall(r'```json\s*([\s\S]*?)\s*```', res)
                if not json_matches:
                    return jsonify({'error': 'No valid JSON found in model response'}), 400
                    
                data = json.loads(json_matches[0])
                # Validate graph structure
                if 'root' not in data:
                    return jsonify({'error': 'Missing root node in graph structure'}), 400
                
                # Save graph data
                with open('uploads/graph.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=True)
                
                # Build graph
                Graph(data['root']).build_graph()

                html_content = f"""
                <div class="file-response">
                    <h4>File processed successfully</h4>
                    <div class="file-details">
                        <p>Graph structure created with:</p>
                        <ul>
                            <li<strong>>Root node:</strong> {data.get('root', 'N/A')}</li>
                        </ul>
                        <div class="graph-preview">
                            <iframe src="/uploads/graph_with_predicates.html" 
                                    style="width: 100%; height: 400px; border: 1px solid #ddd;"></iframe>
                            <p><a href="/uploads/graph_with_predicates.html" target="_blank">Open graph in new tab</a></p>
                        </div>
                    </div>
                </div>   
                """
                return jsonify({'html': html_content})

            except json.JSONDecodeError as e:
                return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400
            except Exception as e:
                return jsonify({'error': f'Graph processing error: {str(e)}'}), 500
                
        except Exception as e:
            return jsonify({'error': f"File processing error: {str(e)}"}), 500
    else:
        return jsonify({'error': 'File type not allowed. Allowed types: doc, docx, pdf, txt'}), 400

if __name__ == '__main__':
    app.run(debug=True)
