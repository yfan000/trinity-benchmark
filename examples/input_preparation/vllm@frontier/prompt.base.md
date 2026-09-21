# Prompt — vllm@frontier

Subtask: **Input preparation**. Base arm, exactly as the model received it.

````
## Task
Determine and write all input files required to run the chosen inference workload on the target system.

## Workload
- Problem: Llama-3.1-8B offline inference, 50 prompts, max_tokens=50, tensor parallel size 4
- Software selected: vLLM (ROCm)
- System: Frontier (OLCF)
- Working directory: /lustre/orion/AlloyDesign/scratch/efaraday/vllm_run
- Model path on system: /lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b
- Turnaround is the priority: minimize time-to-result

## Worked Example
```python
# source: https://raw.githubusercontent.com/vllm-project/vllm/v0.6.0/examples/offline_inference.py
# a real input for a DIFFERENT system — form only

from vllm import LLM, SamplingParams

# Sample prompts.
prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

# Create an LLM.
llm = LLM(model="facebook/opt-125m")
# Generate texts from the prompts. The output is a list of RequestOutput objects
# that contain the prompt, generated text, and other information.
outputs = llm.generate(prompts, sampling_params)
# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

## Instructions
Determine the parameters and configuration the application requires for this workload, then write out each input file in full. Do NOT write a job script or scheduler directives — input files only.

(a) Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.

(b) Never fabricate the contents of binary or runtime-generated files (databases, wavefunction or checkpoint files, restart files, outputs) — list those as produced at runtime instead of writing text into them.

(c) Treat the worked example above as a demonstration of FORM ONLY: the constructor arguments, method calls, and code structure it shows. Its model name, prompt strings, and parameter values describe a DIFFERENT system and must not be carried over.

(d) Make sure any count you declare matches the entries you actually write out — if you say there are 50 prompts, write exactly 50 prompt strings.

## Output
For each required file, give its filename and its complete contents in a fenced code block, then one line on why each is needed.
````
