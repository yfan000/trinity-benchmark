# nemotron-3-ultra — vllm@frontier, rich arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
```python
# /lustre/orion/AlloyDesign/scratch/efaraday/vllm_run/offline_inference.py
from vllm import LLM, SamplingParams
import json
import time

# 50 prompts for offline inference
prompts = [
    "The crystal structure of aluminum is",
    "In materials science, dislocation motion affects",
    "The phase diagram of iron-carbon shows",
    "Grain boundary strengthening mechanisms include",
    "The Hall-Petch relationship describes",
    "Precipitation hardening in aluminum alloys works by",
    "The difference between FCC and BCC metals is",
    "Solid solution strengthening occurs when",
    "The recrystallization temperature of copper is approximately",
    "Work hardening increases the yield strength by",
    "The elastic modulus of steel is typically around",
    "Fatigue failure in metals initiates at",
    "Creep deformation becomes significant at temperatures above",
    "The Schmid factor calculates the resolved shear stress on",
    "Twinning in magnesium alloys is activated along",
    "The stacking fault energy of austenitic stainless steel influences",
    "Intermetallic compounds such as Ni3Al exhibit",
    "The coefficient of thermal expansion for tungsten is",
    "Superalloys derive their high-temperature strength from",
    "The Burgers vector characterizes the magnitude and direction of",
    "In titanium alloys, the alpha-beta transition occurs at",
    "The toughening mechanism in transformation-toughened zirconia involves",
    "Carbon fiber reinforced polymers exhibit high specific strength because",
    "The glass transition temperature of epoxy resins is typically",
    "Dislocation pile-ups at grain boundaries create",
    "The Orowan mechanism describes strengthening by",
    "In nickel-based superalloys, the gamma prime phase provides",
    "The critical resolved shear stress for slip in copper is",
    "Grain size refinement improves both strength and toughness through",
    "The Peierls stress represents the lattice friction stress for",
    "Solidification cracking in welds is promoted by",
    "The Taylor equation relates flow stress to dislocation density by",
    "In shape memory alloys, the martensitic transformation is",
    "The fracture toughness of ceramics is typically lower than metals because",
    "Dispersion strengthening uses particles that are",
    "The Lomer-Cottrell lock forms when two dislocations react to create",
    "In hexagonal close-packed metals, basal slip is",
    "The Coffin-Manson relation describes low-cycle fatigue life as a function of",
    "Hydrogen embrittlement in high-strength steels is caused by",
    "The Zener pinning effect limits grain growth by",
    "In dual-phase steels, the martensite islands provide",
    "The Nabarro-Herring creep mechanism involves diffusion through",
    "Twin boundaries in copper have lower energy than random grain boundaries because",
    "The stacking sequence for FCC crystals is",
    "In aluminum-lithium alloys, the delta prime precipitate strengthens by",
    "The Bauschinger effect describes the reduction in yield strength after",
    "Coble creep differs from Nabarro-Herring creep by diffusion along",
    "The Krieger-Reid relationship predicts the effect of texture on",
    "In materials informatics, descriptor-based models predict properties from",
]

# Sampling parameters: max_tokens=50, greedy decoding for speed
sampling_params = SamplingParams(
    temperature=0.0,
    top_p=1.0,
    max_tokens=50,
)

# Initialize LLM with tensor parallel size 4 (uses 4 GPUs)
# model path from system specification
llm = LLM(
    model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
    tensor_parallel_size=4,
    dtype="float16",  # Use FP16 for faster inference on MI250X
    trust_remote_code=True,
    gpu_memory_utilization=0.9,
)

# Run inference
start_time = time.time()
outputs = llm.generate(prompts, sampling_params)
end_time = time.time()

# Print results and timing
print(f"Inference completed in {end_time - start_time:.2f} seconds")
print(f"Throughput: {len(prompts) / (end_time - start_time):.2f} prompts/sec")

for i, output in enumerate(outputs):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"\n--- Prompt {i+1} ---")
    print(f"Prompt: {prompt!r}")
    print(f"Generated: {generated_text!r}")

# Save results to JSON for record
results = []
for output in outputs:
    results.append({
        "prompt": output.prompt,
        "generated_text": output.outputs[0].text,
    })

with open("inference_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to inference_results.json")
```

Needed because: This is the main Python script that executes the vLLM offline inference workload. It loads the Llama-3.1-8B model from the specified system path, configures tensor parallel size 4 to utilize 4 MI250X GPUs, defines exactly 50 prompts as required, sets max_tokens=50 with greedy decoding for minimal latency, runs batched inference, and saves results to JSON.

```json
// /lustre/orion/AlloyDesign/scratch/efaraday/vllm_run/prompts.json
[
  "The crystal structure of aluminum is",
  "In materials science, dislocation motion affects",
  "The phase diagram of iron-carbon shows",
  "Grain boundary strengthening mechanisms include",
  "The Hall-Petch relationship describes",
  "Precipitation hardening in aluminum alloys works by",
  "The difference between FCC and BCC metals is",
  "Solid solution strengthening occurs when",
  "The recrystallization temperature of copper is approximately",
  "Work hardening increases the yield strength by",
  "The elastic modulus of steel is typically around",
  "Fatigue failure in metals initiates at",
  "Creep deformation becomes significant at temperatures above",
  "The Schmid factor calculates the resolved shear stress on",
  "Twinning in magnesium alloys is activated along",
  "The stacking fault energy of austenitic stainless steel influences",
  "Intermetallic compounds such as Ni3Al exhibit",
  "The coefficient of thermal expansion for tungsten is",
  "Superalloys derive their high-temperature strength from",
  "The Burgers vector characterizes the magnitude and direction of",
  "In titanium alloys, the alpha-beta transition occurs at",
  "The toughening mechanism in transformation-toughened zirconia involves",
  "Carbon fiber reinforced polymers exhibit high specific strength because",
  "The glass transition temperature of epoxy resins is typically",
  "Dislocation pile-ups at grain boundaries create",
  "The Orowan mechanism describes strengthening by",
  "In nickel-based superalloys, the gamma prime phase provides",
  "The critical resolved shear stress for slip in copper is",
  "Grain size refinement improves both strength and toughness through",
  "The Peierls stress represents the lattice friction stress for",
  "Solidification cracking in welds is promoted by",
  "The Taylor equation relates flow stress to dislocation density by",
  "In shape memory alloys, the martensitic transformation is",
  "The fracture toughness of ceramics is typically lower than metals because",
  "Dispersion strengthening uses particles that are",
  "The Lomer-Cottrell lock forms when two dislocations react to create",
  "In hexagonal close-packed metals, basal slip is",
  "The Coffin-Manson relation describes low-cycle fatigue life as a function of",
  "Hydrogen embrittlement in high-strength steels is caused by",
  "The Zener pinning effect limits grain growth by",
  "In dual-phase steels, the martensite islands provide",
  "The Nabarro-Herring creep mechanism involves diffusion through",
  "Twin boundaries in copper have lower energy than random grain boundaries because",
  "The stacking sequence for FCC crystals is",
  "In aluminum-lithium alloys, the delta prime precipitate strengthens by",
  "The Bauschinger effect describes the reduction in yield strength after",
  "Coble creep differs from Nabarro-Herring creep by diffusion along",
  "The Krieger-Reid relationship predicts the effect of texture on",
  "In materials informatics, descriptor-based models predict properties from"
]
```

Needed because: Provides the 50 prompts in a separate reusable JSON file, allowing the inference script to load prompts externally rather than hardcoding them. This separates data from code and enables easy prompt modification or reuse across runs. The script can be modified to `json.load(open("prompts.json"))` instead of the inline list.
````
