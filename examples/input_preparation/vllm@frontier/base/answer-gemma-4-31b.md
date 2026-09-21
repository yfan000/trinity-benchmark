# gemma-4-31b — vllm@frontier, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
**inference.py**
```python
from vllm import LLM, SamplingParams

# 50 prompts for offline inference
prompts = [
    "What is the capital of France?",
    "Explain quantum entanglement in one sentence.",
    "Who wrote the play Romeo and Juliet?",
    "What is the chemical symbol for gold?",
    "How does a transformer model work?",
    "What is the speed of light in a vacuum?",
    "Who painted the Mona Lisa?",
    "What is the largest planet in our solar system?",
    "Define the term 'machine learning'.",
    "What is the square root of 144?",
    "Who discovered penicillin?",
    "What is the primary gas in Earth's atmosphere?",
    "What is the currency of Japan?",
    "Who developed the theory of general relativity?",
    "What is the boiling point of water at sea level?",
    "What is the smallest prime number?",
    "Who is the author of '1984'?",
    "What is the capital of Germany?",
    "How many continents are there on Earth?",
    "What is the most abundant element in the universe?",
    "What is the capital of Canada?",
    "Who founded Microsoft?",
    "What is the function of a mitochondria in a cell?",
    "What is the hard disk drive's main purpose?",
    "What is the capital of Australia?",
    "Who wrote the Odyssey?",
    "What is the pH of pure water?",
    "What is the capital of Italy?",
    "What is the main ingredient in hummus?",
    "Who is known as the father of computer science?",
    "What is the capital of Spain?",
    "What is the distance from Earth to the Sun?",
    "Who painted the Sistine Chapel ceiling?",
    "What is the capital of Brazil?",
    "What is the atomic number of carbon?",
    "Who wrote 'The Great Gatsby'?",
    "What is the capital of India?",
    "What is the purpose of a GPU in AI?",
    "Who is the current CEO of OpenAI?",
    "What is the capital of Egypt?",
    "What is the largest ocean on Earth?",
    "Who discovered the law of gravity?",
    "What is the capital of South Korea?",
    "What is the process of plants making food called?",
    "Who wrote 'Pride and Prejudice'?",
    "What is the capital of Mexico?",
    "What is the most spoken language in the world?",
    "Who developed the first vaccine?",
    "What is the capital of Argentina?",
    "What is the value of pi to two decimal places?",
    "What is the capital of Thailand?"
]

# Sampling parameters: max_tokens=50
sampling_params = SamplingParams(max_tokens=50)

# Initialize LLM with model path and tensor parallel size 4
llm = LLM(
    model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
    tensor_parallel_size=4
)

# Generate texts
outputs = llm.generate(prompts, sampling_params)

# Print results
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```
This Python script configures the vLLM engine to load the specific Llama-3.1-8B model from the Frontier filesystem, sets the tensor parallelism to 4 to distribute the workload across GPUs, and executes the 50 required prompts with the specified token limit.
````
