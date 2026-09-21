# llama-3.1-8b — vllm@frontier, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 4 of 9 requirements violated).

````
### File 1: `prompts.txt`
```markdown
# List of 50 prompts for Llama-3.1-8B offline inference
1. What is the meaning of life?
2. The capital of France is
3. The future of AI is
4. The president of the United States is
5. Hello, my name is
6. The world is a
7. A new technology is
8. The benefits of meditation are
9. A new medical breakthrough is
10. The importance of education is
11. The role of AI in healthcare is
12. A new discovery in space is
13. The impact of climate change is
14. The benefits of a plant-based diet are
15. A new development in renewable energy is
16. The importance of mental health is
17. A new breakthrough in materials science is
18. The role of AI in finance is
19. A new discovery in physics is
20. The benefits of a healthy lifestyle are
21. A new development in biotechnology is
22. The impact of social media on society is
23. The importance of critical thinking is
24. A new breakthrough in computer science is
25. The role of AI in transportation is
26. A new discovery in chemistry is
27. The benefits of a balanced diet are
28. A new development in nanotechnology is
29. The importance of emotional intelligence is
30. A new breakthrough in robotics is
31. The role of AI in education is
32. A new discovery in biology is
33. The benefits of a happy marriage are
34. A new development in cybersecurity is
35. The importance of adaptability is
36. A new breakthrough in environmental science is
37. The role of AI in healthcare is
38. A new discovery in mathematics is
39. The benefits of a fulfilling career are
40. A new development in artificial intelligence is
41. The importance of resilience is
42. A new breakthrough in materials engineering is
43. The role of AI in finance is
44. A new discovery in astronomy is
45. The benefits of a healthy sleep schedule are
46. A new development in biophysics is
47. The importance of empathy is
48. A new breakthrough in computer vision is
49. The role of AI in transportation is
50. A new discovery in materials science is
```
Why: This file contains the list of 50 prompts for Llama-3.1-8B offline inference.

### File 2: `sampling_params.json`
```json
{
  "temperature": 0.8,
  "top_p": 0.95,
  "max_tokens": 50,
  "num_return_sequences": 1,
  "num_sequences": 50,
  "num_parallel": 4
}
```
Why: This file contains the sampling parameters for the Llama-3.1-8B offline inference, including temperature, top-p, max tokens, and parallelization settings.

### File 3: `llm_config.json`
```json
{
  "model_path": "/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
  "model_name": "llama-3.1-8b",
  "tensor_parallel_size": 4
}
```
Why: This file contains the configuration for the Llama-3.1-8B model, including the model path, model name, and tensor parallel size.

### File 4: `run_config.json`
```json
{
  "num_nodes": 1,
  "num_gpus": 8,
  "num_cores": 64,
  "memory": 512,
  "filesystem": "/lustre/orion"
}
```
Why: This file contains the run configuration for the Llama-3.1-8B offline inference, including the number of nodes, GPUs, cores, memory, and filesystem.

### File 5: `input.json`
```json
{
  "prompts": "prompts.txt",
  "sampling_params": "sampling_params.json",
  "llm_config": "llm_config.json",
  "run_config": "run_config.json"
}
```
Why: This file contains the input configuration for the Llama-3.1-8B offline inference, including the prompts, sampling parameters, LLM configuration, and run configuration.

### File 6: `model.bin` (produced at runtime)
This file will contain the Llama-3.1-8B model binary.

### File 7: `output.txt` (produced at runtime)
This file will contain the output of the Llama-3.1-8B offline inference, including the generated text for each prompt.
````
