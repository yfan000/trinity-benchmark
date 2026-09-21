# gpt-oss-120b — vllm@frontier, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 4 of 9 requirements violated).

````
**File: `prompts.txt`**  
List of the 50 prompts that the offline‑inference run will process – one prompt per line.  

```text
1. Explain the principle of quantum entanglement in simple terms.
2. What are the main challenges in scaling renewable energy worldwide?
3. Describe how blockchain technology can improve supply‑chain transparency.
4. Summarize the plot of Shakespeare's *Macbeth* in two sentences.
5. What are the health benefits of a Mediterranean diet?
6. Provide a brief overview of the history of the internet.
7. How does a neural network learn from data?
8. List three arguments for and three against autonomous vehicles.
9. What causes the aurora borealis?
10. Explain the difference between static and dynamic typing in programming languages.
11. What are the key components of a modern DevOps pipeline?
12. Outline the steps to perform a basic Monte Carlo simulation.
13. Describe the process of photosynthesis in plants.
14. What is the significance of the Higgs boson discovery?
15. Compare and contrast capitalism and socialism.
16. Give a short recipe for a classic Margherita pizza.
17. How do electric cars impact the electric grid?
18. What are the main factors that affect climate change?
19. Explain the concept of zero‑knowledge proofs.
20. Describe the life cycle of a butterfly.
21. What is the role of mitochondria in eukaryotic cells?
22. Summarize the plot of the movie *Inception*.
23. Provide an example of a logical fallacy and why it is flawed.
24. How does the capital market differ from the money market?
25. What are the basic principles of Agile software development?
26. Explain how CRISPR-Cas9 gene editing works.
27. What is the importance of diversity in an organization?
28. Describe the typical workflow for training a large language model.
29. What are the primary causes of ocean acidification?
30. Outline the steps to secure a Linux server.
31. How does a Bitcoin transaction get confirmed?
32. Explain the difference between supervised and unsupervised learning.
33. What are the potential risks of artificial general intelligence?
34. Give a brief description of the Taj Mahal’s architecture.
35. What is the function of the Federal Reserve in the US economy?
36. Summarize the main ideas of Einstein’s theory of relativity.
37. How do vaccines stimulate the immune system?
38. Describe the process of recycling plastic bottles.
39. What are the advantages of using containerization in software deployment?
40. Explain the concept of a “smart city.”
41. What are the main features of the Rust programming language?
42. How does a PID controller work in control systems?
43. Provide a short biography of Ada Lovelace.
44. What is the effect of deforestation on biodiversity?
45. Explain the role of the United Nations in international peacekeeping.
46. How does a solar eclipse occur?
47. Describe the main steps of the scientific method.
48. What are the ethical considerations of facial‑recognition technology?
49. Outline the basic architecture of a transformer model.
50. What is the significance of the French Revolution in modern politics?
```

*Why needed:* `prompts.txt` is the sole input data source that vLLM will read and generate up‑to‑50‑token completions for; the workload specifies exactly 50 prompts.

---

**File: `vllm_config.json`**  
JSON‑formatted configuration that tells vLLM where to find the model, how to parallelize it, the generation limits, and the sampling strategy.

```json
{
  "model_path": "/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
  "tensor_parallel_size": 4,
  "max_tokens": 50,
  "sampling_params": {
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

*Why needed:* vLLM reads this file (or an equivalent set of command‑line arguments) to set up the inference engine exactly as required by the workload: the Llama‑3.1‑8B checkpoint location, a tensor‑parallel degree of 4 for the Frontier GPUs, a maximum of 50 generated tokens per request, and the sampling hyper‑parameters that give a good trade‑off between speed and output quality.
````
