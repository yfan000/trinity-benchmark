# gemma-4-31b — vllm@frontier, rich arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
`inference.py`
```python
from vllm import LLM, SamplingParams

# 50 prompts for offline inference
prompts = [
    "Explain the concept of quantum entanglement in simple terms.",
    "What are the primary benefits of using a transformer architecture?",
    "Write a short poem about the beauty of the Rocky Mountains.",
    "How does a Large Language Model handle tokenization?",
    "Describe the process of photosynthesis.",
    "What is the difference between supervised and unsupervised learning?",
    "Write a Python function to calculate the Fibonacci sequence.",
    "What are the main causes of inflation in an economy?",
    "Explain the significance of the Magna Carta.",
    "How do neural networks use backpropagation?",
    "Describe the laws of thermodynamics.",
    "What is the capital city of Kazakhstan?",
    "Explain the role of a catalyst in a chemical reaction.",
    "Write a summary of the plot of Hamlet.",
    "How does the CRISPR-Cas9 system work?",
    "What are the key features of the ROCm software stack?",
    "Describe the impact of the Industrial Revolution on society.",
    "What is the purpose of a GPU in deep learning?",
    "Explain the theory of relativity in a few sentences.",
    "How do search engines index the web?",
    "What is the difference between a list and a tuple in Python?",
    "Describe the function of mitochondria in a cell.",
    "What are the main ingredients in a classic beef bourguignon?",
    "Explain the concept of 'Attention' in the context of Transformers.",
    "What is the significance of the Turing Test?",
    "Describe the water cycle.",
    "How do electric vehicle batteries work?",
    "What is the purpose of a Load Balancer in system architecture?",
    "Write a short story about a robot learning to paint.",
    "What is the chemical formula for glucose?",
    "Explain the concept of a 'smart contract' on a blockchain.",
    "How does the human heart pump blood?",
    "What is the difference between REST and GraphQL APIs?",
    "Describe the plot of the Odyssey.",
    "What is the role of the ozone layer in protecting Earth?",
    "Explain the difference between a process and a thread.",
    "What are the primary goals of the Sustainable Development Goals?",
    "Write a recipe for a simple chocolate cake.",
    "How does a hash map achieve constant time complexity for lookups?",
    "What is the significance of the French Revolution?",
    "Describe the process of nuclear fusion in stars.",
    "What is the purpose of an activation function in a neural network?",
    "Explain the concept of 'overfitting' in machine learning.",
    "How do airplanes generate lift?",
    "What is the difference between TCP and UDP?",
    "Describe the architecture of the MI250X GPU.",
    "What is the main goal of the Large Hadron Collider?",
    "Explain how public key encryption works.",
    "What are the properties of a noble gas?",
    "Write a brief biography of Ada Lovelace."
]

# sampling_params with max_tokens=50 as requested
sampling_params = SamplingParams(max_tokens=50)

# LLM configuration: local model path and tensor parallel size 4
llm = LLM(
    model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
    tensor_parallel_size=4
)

# Generate outputs
outputs = llm.generate(prompts, sampling_params)

# Print results
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}\nGenerated text: {generated_text!r}\n{'-'*40}")
```
This Python script is the primary driver for vLLM offline inference, defining the model location, the hardware parallelism (tensor parallel 4), the 50 specific prompts, and the output length constraint.
````
