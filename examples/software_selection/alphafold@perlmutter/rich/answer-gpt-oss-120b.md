# gpt-oss-120b — alphafold@perlmutter, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 4 requirements violated).

````
**Selected application:** **AlphaFold** – DeepMind AlphaFold2 protein‑structure prediction (conda environment)

**Why it fits the workload**

* **Problem match** – AlphaFold2 is expressly designed for *ab initio* prediction of a protein’s 3‑dimensional structure directly from its amino‑acid sequence, exactly the task described.
* **Single‑chain capability** – It handles individual protein chains (or complexes) without requiring a multi‑protein setup, so it works for the “single protein chain” case.
* **Performance on Perlmutter** – The AlphaFold package is provided as a pre‑configured conda environment that includes GPU‑accelerated components (MSA generation, Evoformer, and structure‑relaxation). Perlmutter’s GPU nodes (A100/A10) are fully supported, delivering high throughput for single‑run predictions.
* **Ease of use** – The installed version already includes all required databases, scripts, and dependencies, allowing you to start the first run from the working directory `/pscratch/sd/a/aschmidt/case01` immediately.
* **Reliability & community support** – AlphaFold is the de‑facto standard in protein‑structure prediction, extensively benchmarked and documented, making it the safest choice over newer, less‑tested models such as *chai‑lab*.

Therefore, AlphaFold is the best‑matched, ready‑to‑run application for the given protein‑structure prediction workload on Perlmutter.
````
