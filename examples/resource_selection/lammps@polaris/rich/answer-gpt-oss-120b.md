# gpt-oss-120b — lammps@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step 1 – Estimate the wall‑time that the job really needs**

* System size*: 500 000 LJ argon atoms  
* Simulation length*: 100 000 steps × 1 fs = 0.10 ns of physical time  
* Benchmark information (ALCF / Polaris, LAMMPS + Kokkos on an A100):  
  – A single A100 typically delivers ≈ 6 ns of simulated LJ time per **wall‑clock day** (≈ 0.25 ns h⁻¹).  

Therefore the wall‑clock time for 0.10 ns of simulated trajectory on **one GPU** is  

\[
\frac{0.10\;\text{ns}}{6\;\text{ns day}^{-1}} \;=\;0.0167\;\text{day}
  \;=\;0.40\;\text{h}
  \;\approx\;24\;\text{min}.
\]

Because the build default uses **4 MPI ranks per node, each bound to one GPU**, the four GPUs on a node run in parallel. The runtime scales roughly with 1/ # GPUs, so the wall‑clock estimate for a *single node* (4 GPUs) is

\[
24\;\text{min} / 4 \;\approx\;6\;\text{min}.
\]

To be conservative we add a 5× safety margin (to cover I/O, start‑up overhead, and possible slower performance on the first run on Polaris).  

\[
6\;\text{min} \times 5 \;=\;30\;\text{min}.
\]

**Requested wall‑time = 00:30:00** (30 minutes). This is well below any queue limit that permits at least one node.

---

**Step 2 – Eliminate queues that cannot satisfy the request**

| Queue            | Node range      | Max wall‑time | Reason for elimination (if any) |
|------------------|-----------------|---------------|----------------------------------|
| debug            | 1‑2             | 1 h           | **PASS** – node count 1 ∈ [1,2] and 30 min ≤ 1 h |
| debug‑scaling    | 1‑10            | 1 h           | **PASS** – node count 1 ∈ [1,10] and 30 min ≤ 1 h |
| prod             | 10‑496          | 24 h          | **FAIL** – node count 1 < 10 (minimum) |
| demand           | 1‑56            | 1 h           | **PASS** – node count 1 ∈ [1,56] and 30 min ≤ 1 h |
| preemptable      | 1‑10            | 72 h          | **PASS** – node count 1 ∈ [1,10] and 30 min ≤ 72 h |
| capacity         | 1‑4             | 168 h         | **PASS** – node count 1 ∈ [1,4] and 30 min ≤ 168 h |

All queues except **prod** satisfy the three limits (node‑minimum, node‑maximum, wall‑time).  

---

**Step 3 – Choose a legal queue and verify each limit**

We pick the **debug** queue because it is the smallest‑turnaround queue that meets all constraints and is intended for short, test‑scale runs.

| Check                | Requested value | Queue limit | Result |
|----------------------|-----------------|-------------|--------|
| Node minimum         | 1               | ≥ 1         | PASS |
| Node maximum         | 1               | ≤ 2         | PASS |
| Maximum wall‑time    | 00:30:00        | ≤ 01:00:00  | PASS |

All three checks pass, so the request is admissible.

---

**Step 4 – Apply the build defaults for ranks‑per‑node and GPUs‑per‑rank**

* Build default: **4 MPI ranks per node**
* GPU allocation rule (Kokkos backend): **1 GPU per rank**
* Hence **4 GPUs per node** (the whole GPU package on a Polaris node)

The only free decision was the **node count**, which we have set to **1** (the smallest legal value that still passes all queue limits).

---

**Step 5 – Summary (resource specification)**  

| Item                     | Value |
|--------------------------|-------|
| **Queue**                | debug |
| **Wall‑time**            | 00:30:00 |
| **Number of nodes**      | 1 |
| **GPUs per node**        | 4 |
| **MPI ranks per node**   | 4 |
| **Total MPI ranks**      | 4  (= 1 × 4) |
| **Working directory**    | /eagle/QuantumMatX/lchen/lammps_run |

**Explanation of assumptions & margins**  
*Performance assumption*: 6 ns of simulated LJ time per A100 per wall‑clock day (typical for LAMMPS + Kokkos on Polaris).  
*Safety margin*: 5× the raw estimate to cover start‑up, I/O, and the fact that this is the first LAMMPS run on Polaris. The resulting 30 min request stays safely under the 1‑hour limit of the debug queue.

**Scaling guidance compliance**  
The application note says “Scale nodes for large systems (> 1 M atoms)”. Our system (0.5 M atoms) is below that threshold, so a single‑node configuration follows the recommended default of 4 ranks per node with one GPU each.

---

**Final Resource Specification**

- **Queue**: debug  
- **Wall‑time**: 00:30:00  
- **Nodes**: 1  
- **GPUs per node**: 4  
- **MPI ranks per node**: 4  
- **Total MPI ranks**: 4 (1 node × 4 ranks)  

This request satisfies all Polaris queue policies and uses the build‑default parallel layout for LAMMPS on Polaris.
````
