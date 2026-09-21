# gpt-oss-120b — hpl@crux, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1. Estimate a realistic wall‑time**

HPL performance on a Crux node (128 × Intel Xeon cores, ~2 TFLOP s⁻¹ per core in double precision) is on the order of a few minutes for a 50 000‑order problem when the whole node is used.  
Taking a conservative efficiency of 70 % and adding a 20 % safety margin:

\[
\begin{aligned}
\text{Flops needed} &= 2 N^{3}=2\,(5\times10^{4})^{3}=2.5\times10^{14}\,\text{FLOP}\\
\text{Effective node performance} &=128\;\text{cores}\times 2\;\text{TFLOP/s}\times0.70\approx179\;\text{TFLOP/s}\\
\text{Ideal run time} &=\frac{2.5\times10^{14}}{1.79\times10^{14}}\approx1.4\;\text{s}\\
\text{Add 20 % margin} &\rightarrow\approx1.7\;\text{s}
\end{aligned}
\]

Even allowing for MPI start‑up, I/O, and a very generous safety factor, a **10‑minute** wall‑time is far more than enough.  
We therefore request  

```
walltime = 00:10:00   (hh:mm:ss)
```

**2. Apply the queue table**

| Queue            | Node range (min‑max) | Max wall‑time | Does our request fit? |
|------------------|----------------------|---------------|-----------------------|
| **debug**        | 1 – 8                | 1 h           | **PASS** (1 node, 00:10:00 ≤ 1 h) |
| workq‑route      | 1 – 184              | 24 h          | PASS (1 ≤ 184, 00:10:00 ≤ 24 h) |
| preemptable      | 1 – 10               | 72 h          | PASS (1 ≤ 10, 00:10:00 ≤ 72 h) |
| demand           | 1 – 64               | 1 h           | PASS (1 ≤ 64, 00:10:00 ≤ 1 h) |

All four queues accept a 1‑node, 10‑minute request.  
The *debug* queue is the highest‑priority (shortest turn‑around) queue, so it is the logical choice for a deadline‑sensitive run.

**3. Resource numbers dictated by the build defaults**

- **Ranks per node** – taken from the application build default: **128** MPI ranks per node.  
- **GPUs per node** – Crux nodes have **0 GPUs** (CPU‑only HPL).  
- **Total ranks** – `nodes × ranks_per_node = 1 × 128 = 128` MPI ranks.  

The HPL input file (P = 2, Q = 2) will be interpreted in the usual hybrid MPI/OpenMP fashion: each of the 4 MPI ranks will launch 32 OpenMP threads, giving full utilisation of the 128 cores on the single node.

**4. Final specification**

| Item                | Value                     |
|---------------------|---------------------------|
| **Queue**           | debug                     |
| **Nodes**           | 1                         |
| **Ranks per node**  | 128                       |
| **Total ranks**     | 128 (= 1 × 128)            |
| **GPUs per node**   | 0                         |
| **Wall‑time**       | 00:10:00 (hh:mm:ss)       |
| **Working directory** | /eagle/CosmoSurvey/dokafor/hpl_run |

**Why this works**

- The wall‑time (10 min) is well below the debug‑queue limit (1 h).  
- The node count (1) lies inside the debug‑queue’s allowed range (1‑8).  
- All three checks (node‑minimum, node‑maximum, maximum wall‑time) read **PASS**.  
- Using the build‑default of 128 MPI ranks per node lets the job occupy the full 128 CPU cores, honouring the scaling guidance “maximize performance by using all 128 cores per node.”  
- No GPUs are requested because Crux nodes provide none.  

Thus the request is legal, respects the scheduler policies, and targets the queue that will give the fastest possible turnaround for this HPL LINPACK run.
````
