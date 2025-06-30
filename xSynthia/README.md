#### Available configurations

```toml
[model]
name = "DeepSeek-R1-Distill-Qwen-32B"

# Options:
# - "DeepSeek-R1-Distill-Qwen-32B"
# - "DeepSeek-R1"
# - "QwQ-32B"
# - "Llama-3.1-8b"
# - "Llama-3.2-1B"
# - "Mistral-7B-v0.3"
# - "Mistral-7B-v0.2"
# - "Gemma-3-1B"
# - "Gemma-3-27B"

[graph]
type = "weighted" # Options: "weighted", "multilayer", "unweighted", "directed"
visualization_level = "association network" # Options: "association network", "semantic relations", "both"
color_scheme = "default" # Options: "default", "blue", "red", "green", "pastel", "acid"

[display]
show_edge_labels = true # Options: true, false
show_node_weights = true # Options: true, false
```

#### Web Interface

![image](https://github.com/user-attachments/assets/88c42580-7480-4eb3-b8be-2a4c81d897b1)

**LLM-based configuration recognition** from graph description in natural language

![image](https://github.com/user-attachments/assets/dbd84e56-2555-41f5-9ea8-9a7cb6324d5b)

**LLM-based graph generation** for advanced RAG 

![image](https://github.com/user-attachments/assets/9eebf1a5-7b79-43ce-b99f-49b52e3c2b6c)

Our system answers questions based on a generated graph and retrieved chunks
