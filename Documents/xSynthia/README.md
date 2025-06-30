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
