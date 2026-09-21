# gpt-oss-120b — vllm@frontier, rich arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
**File 1 – `prompts.txt`**  
Contains the 50 text prompts that will be fed to the model (one prompt per line).

```text
1. Explain the significance of the Higgs boson in particle physics.
2. Summarize the plot of Shakespeare's *Macbeth* in a few sentences.
3. What are the primary differences between supervised and unsupervised learning?
4. Describe the process of photosynthesis in plants.
5. Give a brief overview of the history of the Internet.
6. What are the main challenges when scaling deep learning models to billions of parameters?
7. List three common causes of climate change.
8. Explain how a blockchain works at a high level.
9. What is the significance of the P vs NP problem in computer science?
10. Provide a short recipe for a classic Margherita pizza.
11. How does quantum entanglement differ from classical correlation?
12. Discuss the impact of renewable energy on global economies.
13. What are the steps to set up a virtual environment in Python?
14. Summarize the plot of the movie *Inception*.
15. Explain the role of mitochondria in eukaryotic cells.
16. What is the principle behind reinforcement learning?
17. Describe the key features of the Rust programming language.
18. Outline the main causes of the French Revolution.
19. How do generative adversarial networks (GANs) generate realistic images?
20. What is the difference between TCP and UDP protocols?
21. Provide a concise definition of the term “machine learning.”
22. Explain why the sky appears blue during the day.
23. List the major components of a modern computer processor.
24. What are the ethical considerations of AI in healthcare?
25. Summarize the plot of the novel *1984* by George Orwell.
26. How does a photovoltaic cell convert sunlight into electricity?
27. Define the concept of “overfitting” in model training.
28. Explain the function of a compiler in software development.
29. What are the main advantages of containerization technologies like Docker?
30. Describe how the COVID‑19 pandemic impacted global supply chains.
31. What is the purpose of the attention mechanism in transformer models?
32. Outline the steps required to perform a Monte Carlo simulation.
33. Explain the difference between static and dynamic typing in programming languages.
34. Provide a short overview of the theory of relativity.
35. What are the typical use‑cases for edge computing?
36. Summarize the plot of the TV series *Breaking Bad* in three sentences.
37. How does a GPU accelerate deep learning workloads?
38. List three common data structures and their primary use cases.
39. Explain the concept of “zero‑knowledge proofs” in cryptography.
40. What are the environmental impacts of large‑scale data centers?
41. Describe the basic workflow of a continuous integration (CI) pipeline.
42. How do satellite constellations improve global internet coverage?
43. Define “bias” in the context of machine learning datasets.
44. Explain the process of DNA transcription and translation.
45. What is the role of a scheduler in high‑performance computing clusters?
46. Summarize the key ideas behind the Agile software development methodology.
47. How does a convolutional neural network (CNN) process images?
48. List the main steps to fine‑tune a pre‑trained language model.
49. Explain why numerical precision matters in scientific computing.
50. Provide a brief description of the concept of “digital twins.”
```

*Why needed:* Supplies the 50 offline inference prompts that vLLM will generate completions for.

---

**File 2 – `vllm_config.json`**  
JSON file that vLLM reads for runtime configuration. It includes the model location, tensor‑parallel size, device type, and the maximum number of new tokens to generate per prompt.

```json
{
  "model_path": "/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
  "tensor_parallel_size": 4,
  "device": "rocm",
  "max_new_tokens": 50,
  "sampling_params": {
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

*Why needed:* Provides all essential inference parameters (model location, parallelism, device, token budget, sampling) in a single, portable file that the Python driver script can load.

---

**File 3 – `run_vllm_offline.py`**  
Python driver script that loads the configuration, reads the prompt list, launches vLLM, and writes the generated completions to `outputs.json`.

```python
#!/usr/bin/env python3
"""
Offline inference script for Llama‑3.1‑8B using vLLM on Frontier (ROCm).

- Model path and parallelism are taken from vllm_config.json.
- 50 prompts are read from prompts.txt.
- Each prompt generates up to 50 new tokens.
- Results are written to outputs.json (one JSON object per prompt).
"""

import json
from pathlib import Path

from vllm import LLM, SamplingParams

# ----------------------------------------------------------------------
# Load configuration
# ----------------------------------------------------------------------
CONFIG_PATH = Path("vllm_config.json")
with CONFIG_PATH.open() as cfg_f:
    cfg = json.load(cfg_f)

model_path = cfg["model_path"]
tensor_parallel_size = cfg.get("tensor_parallel_size", 1)
device = cfg.get("device", "rocm")
max_new_tokens = cfg.get("max_new_tokens", 50)

# Sampling parameters – taken from the same JSON file.
sampling_cfg = cfg.get("sampling_params", {})
sampling_params = SamplingParams(
    max_tokens=max_new_tokens,
    temperature=sampling_cfg.get("temperature", 0.7),
    top_p=sampling_cfg.get("top_p", 0.9),
)

# ----------------------------------------------------------------------
# Read prompts
# ----------------------------------------------------------------------
PROMPT_FILE = Path("prompts.txt")
prompts = [line.strip() for line in PROMPT_FILE.read_text().splitlines() if line.strip()]

assert len(prompts) == 50, f"Expected 50 prompts, found {len(prompts)}"

# ----------------------------------------------------------------------
# Initialise the LLM
# ----------------------------------------------------------------------
llm = LLM(
    model=model_path,
    tensor_parallel_size=tensor_parallel_size,
    device=device,
)

# ----------------------------------------------------------------------
# Run inference (offline – all prompts at once)
# ----------------------------------------------------------------------
outputs = llm.generate(prompts, sampling_params)

# ----------------------------------------------------------------------
# Write results
# ----------------------------------------------------------------------
RESULT_FILE = Path("outputs.json")
with RESULT_FILE.open("w") as out_f:
    json_list = []
    for out in outputs:
        entry = {
            "prompt": out.prompt,
            "generated_text": out.outputs[0].text,
            "prompt_token_len": out.prompt_token_ids,
            "output_token_len": out.outputs[0].token_ids,
        }
        json_list.append(entry)
    json.dump(json_list, out_f, indent=2)

print(f"Generated {len(outputs)} completions → {RESULT_FILE}")
```

*Why needed:* This is the executable entry point for the workload. It parses the configuration, loads the 50 prompts, launches vLLM with the required ROCm‑enabled parallelism, and stores the generated text, satisfying the offline‑inference requirement.
````
