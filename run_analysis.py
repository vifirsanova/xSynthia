#!/usr/bin/env python3
from huggingface_hub import InferenceClient
import ast
import plotly.graph_objects as go
import pandas as pd
import json
import os
import glob
from pathlib import Path

# Path to the settings file
settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')

# Load settings
with open(settings_file, 'r') as f:
    settings = json.load(f)

""" DEMO """

# Assuming settings is defined somewhere
if settings[''] == "meta-llama/Llama-3.1-8B-Instruct":  # Replace <...> with your actual condition
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Get all html files in example directory
    html_files = glob.glob('examples/jailbreaking_ios.html.html')
    
    for html_file in html_files:
        # Rename each file to static/chord_diagram.html
        os.rename(html_file, 'static/chord_diagram.html')

#""" GLOBAL VARIABLES """

#MODEL = settings['model']
#N_SAMPLES = settings['samples']
#K_ASSOCIATIONS = settings['associations']
#STARTING_PONT = settings['starting_point']
#DETAILS = settings['starting_details']
#LEVEL = settings['visualization_levels'] # associations, visualized in a basic network
#TYPE = settings['graph_type'] # a general directed graph visualization, with node and edge attributes encoding additional information

#""" AUTH CLIENT """
#
#TOKEN = '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'
#client = InferenceClient(MODEL, token=TOKEN)
#
#""" GENERATE N SAMPLES (GRAPH EDGES) """
#
#def sampling(n_samples):
#  outputs = client.chat.completions.create(
#                             messages=[
#                                 {"role": "system", "content": "generate one json object, no explanation or additional text, use the following structure:\n"
#                                 "words: []\n"
#                                 f"{n_samples} samples in a list"
#                                 },
#                                 {"role": "user",
#                                  "content": f"synthesize {n_samples} random but widespread nouns for semantic modeling"},
#                                 ],
#                                 response_format={
#                                     "type": "json",
#                                     "value": {
#                                         "properties": {
#                                             "words": {"type": "array", "items": {"type": "string"}},
#                                             }
#                                         }
#                                     },
#                             stream=False,
#                             max_tokens=1024,
#                             temperature=0.7,
#                             top_p=0.1
#                             ).choices[0].get('message')['content']
#  outputs = ast.literal_eval(outputs)
#  return outputs['words']
#
#samples = sampling(N_SAMPLES)
#
#""" GENERATE K ASSOCIATIONS FOR EACH SAMPLE (GRAPH EDGES) """
#
#def populate(n_associations, words):
#  outputs = dict()
#  for word in words:
#    output = client.chat.completions.create(
#                             messages=[
#                                 {"role": "system", "content": "generate one json object, no explanation or additional text, use the following structure:\n"
#                                 "associations: []\n"
#                                 f"{n_associations} samples in a list"
#                                 },
#                                 {"role": "user",
#                                  "content": f"synthesize {n_associations} associations (nouns) for the word '{word}'"},
#                                 ],
#                                 response_format={
#                                     "type": "json",
#                                     "value": {
#                                         "properties": {
#                                             "associations": {"type": "array", "items": {"type": "string"}},
#                                             }
#                                         }
#                                     },
#                             stream=False,
#                             max_tokens=1024,
#                             temperature=0.7,
#                             top_p=0.1
#                             ).choices[0].get('message')['content'] # list of associations
#    output = ast.literal_eval(output)
#    outputs[word] = output['associations']
#  return outputs
#
#associations = populate(K_ASSOCIATIONS, samples)
#
#""" GENERATE PREDICATES (GRAPH EDGES) """
#
#def predicate(associations):
#  triplets = []
#  for word in associations:
#    for association in associations[word]:
#      triplet = {"source": word, "label": None, "target": association}
#      output = client.chat.completions.create(
#                                       messages=[
#                                                 {"role": "system", "content": "generate one json object, no explanation or additional text, use the following structure:\n"
#                                                                               "predicate: ''\n"
#                                                                               "the predicate should be one verb or phrasal verb, do not repeat subject or object in output"
#                                                 },
#                                                 {"role": "user",
#                                                  "content": f"generate predicate between the word '{word}' (subject) and the word '{association}' (object)"},
#                                                 ],
#                                       response_format={
#                                           "type": "json",
#                                           "value": {
#                                               "properties": {
#                                                   "predicate": {"type": "string"},
#                                                   }
#                                               }
#                                           },
#                                       stream=False,
#                                       max_tokens=128,
#                                       temperature=0.7,
#                                       top_p=0.1
#                                       ).choices[0].get('message')['content']
#      output = ast.literal_eval(output)
#      triplet['label'] = output['predicate']
#      triplets.append(triplet)
#  return triplets
#
#triplets = predicate(associations)
#
#""" RESAMPLE: GENERATE SECOND ORDER ASSOCIATIONS FROM OTHER SAMPLES AND THEIR ASSOCIATIONS """
#
#def resample(triplets):
#  """ GENERATE SECOND ORDER TARGETS """
#  source = '' # check that this source word is already processed
#  triplets_second = [] # placeholder
#
#  for triplet in triplets:
#    if source != triplet['source']:
#      associations = dict() # placeholder for second order associations
#
#      source = triplet['source'] # current token
#
#      # extract second order targets
#      targets = [t['source'] for t in triplets if t['source'] != source]
#      targets += [t['target'] for t in triplets if t['source'] != source]
#
#      associations[source] = list(set(targets))
#
#      """ GENERATE SECOND ORDER PREDICATES """
#      triplet_second = predicate(associations)
#      for t in triplet_second:
#        triplets_second.append(t)
#  return triplets_second
#
#triplets_second = resample(triplets)
#
## Combine both datasets
#data = triplets + triplets_second
#
## Extract unique nodes
#nodes = list(set([entry['source'] for entry in data] + [entry['target'] for entry in data]))
#
## Create a mapping for the nodes
#node_indices = {node: i for i, node in enumerate(nodes)}
#
## Prepare links data (source, target, and value)
#links = [
#    {
#        'source': node_indices[entry['source']],
#        'target': node_indices[entry['target']],
#        'value': 10 if entry in triplets else 5  # Assign higher weight for the first dataset
#    }
#    for entry in data
#]
#
## Create the chord diagram using Plotly
#fig = go.Figure(data=[go.Sankey(
#    node=dict(
#        pad=15,
#        thickness=20,
#        line=dict(color='black', width=0.5),
#        label=nodes
#    ),
#    link=dict(
#        source=[link['source'] for link in links],
#        target=[link['target'] for link in links],
#        label=[entry['label'] for entry in data],
#        value=[link['value'] for link in links]
#    )
#)])
#
## Update layout to simulate a circular appearance
#fig.update_layout(
#    title="Chord Diagram for Relationships with Importance Weights",
#    font_size=10,
#    width=800,
#    height=800,
#    showlegend=False,
#    hovermode='closest',
#    xaxis=dict(scaleanchor='y', showgrid=False),
#    yaxis=dict(scaleanchor='x', showgrid=False)
#)
#
# Save the figure to an HTML file
#fig.write_html("static/chord_diagram.html")



