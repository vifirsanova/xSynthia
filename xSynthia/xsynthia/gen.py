# gen.py
import toml

class Model:
    """
    A class to initialize model from config.toml and generate answer 
    based on user prompt and system prompt loaded from *.txt
    """
    def __init__(self, config: str = './xsynthia/config.toml'):
        """
        Initialize model setting from xsynthia.config.
        This file contains configurations set manually through xSynthia GUI.
        This file is also used as default settings for LLM-based configuration parsing.
        In the automated config parsing, these settings will be used if the parsing was not successfull. 
        """
        self.config = self._load_config(config)
        # Load LLM: Gemma 1B is set by default, will be updated later 
        self.model, self.tokenizer = self._load_model()
        
    def _load_config(self, config):
        with open(config, 'r') as f:
            config = toml.load(f)
        return config

    def _load_prompt(self, prompt_path):
        with open(prompt_path, 'r') as f:
            system_prompt = f.read()
        return system_prompt

    def _load_model(self, quantization=True):
        from transformers import AutoTokenizer, Gemma3ForCausalLM, BitsAndBytesConfig
        model_id = "google/gemma-3-1b-it" # More model will be added later; the functionality is limited due toour hardware capacity
        quantization_config = BitsAndBytesConfig(load_in_8bit=True) if quantization == True else None
        model = Gemma3ForCausalLM.from_pretrained(model_id, quantization_config=quantization_config).eval()
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        return model, tokenizer

    def generate(self, prompt_path, user_input):
        import torch, re
        system_prompt = self._load_prompt(prompt_path)
        messages = [[{"role": "system",
                      "content": [{"type": "text", "text": system_prompt},]},
                     {"role": "user",
                      "content": [{"type": "text", "text": user_input},]},],]
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            ).to(self.model.device)

        with torch.inference_mode():
            # We'll add the model tuning here also
            outputs = self.model.generate(**inputs, temperature=0.7, top_k=50, max_new_tokens=2048)

        # We'll add response formatting here
        outputs = self.tokenizer.batch_decode(outputs)
        return str(re.findall(r'<start_of_turn>(.*?)<end_of_turn>', outputs[0], re.DOTALL)[1])[6:]

class Graph:
    def __init__(self, triplets):
        self.triplets = triplets

    def build_graph(self):
        import plotly.graph_objects as go
        import networkx as nx
        from collections import Counter
        import random
        # Prepare nodes and edges
        nodes = set()
        edges = []
        # Extract noded and edges from the set of triplets
        for triplet in self.triplets:
            nodes.add(triplet['subject'])
            nodes.add(triplet['object'])
            edges.append((triplet['subject'], triplet['object'], triplet['predicate']))
        
        print(nodes)
        print(edges)
        # Create a networkx graph
        G = nx.Graph()

        # Add nodes and edges to the graph
        for edge in edges:
            G.add_edge(edge[0], edge[1], label=edge[2])

        # Generate positions for nodes using force-directed layout with more space
        pos = nx.spring_layout(G, seed=42)  # Increasing k for more spacing

        # Extract node and edge data for Plotly
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        node_labels = list(G.nodes())

        # Count connections
        node_degrees = Counter([node for edge in edges for node in edge[:2]])

        # Assign distinct colors for each predicate (use a set to avoid duplicates)
        unique_predicates = list(set([edge[2] for edge in edges]))
        predicate_colors = {predicate: f'rgba({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)},1)'
                            for predicate in unique_predicates}

        # Plotly data for edges
        edge_x = []
        edge_y = []

        for edge in edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        # Create the figure
        fig = go.Figure()

        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='text',
            mode='lines'
        ))

        # Add nodes with uniform size and labels
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(
                size=25,  # Uniform node size for all nodes
                color=[node_degrees[node] for node in node_labels],
                #colorscale='Viridis',
                colorbar=dict(title='Connections')
            ),
            text=node_labels,
            hoverinfo='text',
            textposition='top center',
            textfont=dict(size=13, weight="bold")
        ))

        # Add predicate labels near the nodes with black text
        for edge in edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            predicate_label = edge[2]

            # Calculate the midpoint of the edge and add small offsets to create spacing
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2

            # Add the label near the midpoint of the edge with black text
            fig.add_trace(go.Scatter(
                x=[mid_x], y=[mid_y],
                mode='text',
                text=[predicate_label],
                textposition='middle center',
                showlegend=False,
                textfont=dict(size=10)
            ))

        # Update layout
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            title="Force-Directed Graph with Predicate Labels on Nodes"
        )

        # Save the figure as an HTML file
        fig.write_html("uploads/graph_with_predicates.html")
