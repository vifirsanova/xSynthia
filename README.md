![image](https://github.com/user-attachments/assets/9792a323-041c-4525-a894-d952ee7d6c77)

Generate your own semantic web with LLMs

- Use it for **Retrieval-Augmented Generation** (RAG)
- Generate **custom visualizations**
- **Xplainbale AI**: explore semantic relations behind LLMs

## Table of Contents
- [About](#about)
- [Features](#features)
- [Public demo](#public-web-demo)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)

## About
The tool takes unstructured data (i.e., plain text) as input and generates a graph knowledge base using Large Language Models (LLMs). The resulting graph can be visualized or applied for Retrieval-Augmented Generation (RAG). The tool allows for generating graphs from unstructured data for the following use cases: 
- **Enhancing RAG systems** by accessing graph databases instead of generating answers directly from unstructured data. Adding intermediate graph generation step improves overall RAG quality (see evidence [here](https://arxiv.org/pdf/2404.16130)).
- **Exploring the semantic web** generated with LLMs. Knowledge graphs are easily visualized in 2-dimensional space, providing a tool for comprehensive overview of the resulting structures. They can be used to explore the strength of connections between inputs and outputs in LLMs contributing to the field of Explainable AI (XAI) (see [overview of applying graphs to XAI](https://arxiv.org/pdf/2407.15248)).
- **Generating graphs** for data exploratory analysis. The tool allows for generating semantic web from unstructured data for research purposes, such as data science, linguistics analysis or open domain data visualization. For example, such a tool can visualize topics and connections between them in a graph, providing a more agile alternative to bibliometric exploratory tools such as VOSViewer, or linguistic research ontologies, like WordNet.

## Features

![image_2025-03-29_14-32-45](https://github.com/user-attachments/assets/e786244c-f2b2-469a-b4cc-1197cca5de82)

![image_2025-03-29_14-33-18](https://github.com/user-attachments/assets/8ab4ecb4-f1d5-4c2d-b768-b064caad2ed4)

![image_2025-03-29_14-34-10](https://github.com/user-attachments/assets/566a3787-85b9-4bd0-8aa9-b119a2e69391)

- **Convert Unstructured Text to Knowledge Graph**
  - Transform plain text (e.g., articles, reports, notes) into structured graph representations.
  - Extract entities, relationships, and semantic hierarchies.
- **LLM-Powered Graph Construction**
  - Test and apply various Large Language Models (e.g., DeepSeek, LLaMA) for semantic parsing and relationship extraction.
  - Generates knowledge graphs to enhance and explain RAG pipelines by providing and visualizing structured context.
- **Interactive Visualization**
  - Intuitive interface for exploring and manipulating generated graphs.
  - Node-link diagrams with zoom, filter, and search capabilities.

## Public Web Demo

Accessible at https://xsynthia.onrender.com/ for testing and validation.

## Usage
Start the application from a terminal:
```bash
git clone git@github.com:vifirsanova/xSynthia.git
cd xSynthia
./run.sh # Run script and start the application on your browser
```

**Prerequisites**:  
Python 3.8+

## Configuration
To run the application locally, provide your configuration for Groq or HuggingFace API:

```toml
# config.toml
api_key = "your_api_key_here"  # Replace with your Groq or HuggingFace API key
```

## Examples
Show more complex examples or use cases:

```javascript
// Advanced usage example
const result = advancedFunction({
  param1: 'value',
  param2: 42
});
```

## Testing
How to run tests:

```bash
npm test
# or
pytest
```

## Contributing
Guidelines for contributors:
- How to submit pull requests
- Coding standards
- Issue reporting
