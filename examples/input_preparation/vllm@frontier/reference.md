# Reference answer — vllm@frontier

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
One input file is required: bench.py placed in /lustre/orion/AlloyDesign/scratch/efaraday/vllm_run.

**bench.py**
```python
from vllm import LLM, SamplingParams

prompts = [
    "The history of computing begins with",
    "Climate change is driven by",
    "In the field of materials science,",
    "The human genome contains",
    "Quantum mechanics explains",
    "The largest supercomputers in the world",
    "Renewable energy sources include",
    "Machine learning models are trained by",
    "The speed of light in a vacuum is",
    "Protein folding is important because",
    "The first moon landing occurred when",
    "Nuclear fusion reactors work by",
    "The population of Earth is approximately",
    "High-performance computing enables",
    "The periodic table organizes elements by",
    "Deep learning differs from traditional ML in",
    "The Amazon rainforest produces",
    "Semiconductor fabrication requires",
    "The theory of relativity states",
    "Ocean currents are driven by",
    "Exascale computing is defined as",
    "The immune system protects the body by",
    "Gravitational waves were first detected",
    "Natural language processing allows computers to",
    "The Standard Model of particle physics describes",
    "Solar panels convert sunlight into",
    "The mitochondria is responsible for",
    "Autonomous vehicles rely on",
    "The Big Bang theory proposes that",
    "Cryptography secures communications by",
    "CRISPR gene editing works by",
    "The atmosphere of Mars consists of",
    "Superconductors are materials that",
    "The Turing test measures",
    "Biodiversity is important because",
    "Fluid dynamics describes",
    "The discovery of penicillin changed",
    "Graph neural networks are used for",
    "Dark matter is thought to make up",
    "The structure of DNA was determined by",
    "Transformer models in NLP rely on",
    "The boiling point of water at sea level is",
    "Parallel computing improves performance by",
    "The human brain contains approximately",
    "Fusion energy could provide",
    "The speed of sound in air is",
    "Reinforcement learning trains agents by",
    "The Higgs boson was discovered at",
    "Carbon capture technologies aim to",
    "Exoplanets are discovered by",
]

sampling_params = SamplingParams(max_tokens=50)

llm = LLM(
    model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
    dtype="bfloat16",
    tensor_parallel_size=4,
    enforce_eager=True,
    gpu_memory_utilization=0.85,
)

outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

Why needed: vLLM's offline inference API requires a Python driver script that instantiates `LLM` with model path, dtype, and tensor_parallel_size, and calls `llm.generate()` with a `SamplingParams` object specifying `max_tokens`. The 50 prompt strings match the declared count. `tensor_parallel_size=4` splits the model across 4 GCDs as specified. `enforce_eager=True` and `gpu_memory_utilization=0.85` follow validated working settings for the ROCm build on Frontier. No binary or checkpoint files are authored — the model weights at the specified path are read at runtime.
````
