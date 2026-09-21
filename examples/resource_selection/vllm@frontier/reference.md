# Reference answer — vllm@frontier

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
**Step 1 — Node count and ranks**

The workload requests tensor parallel size 4 (TP=4). The build defaults assign one MPI rank per GCD (8 ranks per node). TP=4 requires exactly 4 GCDs. One Frontier node exposes 8 GCDs (4 physical MI250X cards, each presenting 2 GCDs). TP=4 therefore fits within a single node using 4 of the 8 available GCDs. The node count is 1. The agent must not choose a different node count because TP is a property of the model launch configuration, not a node-scaling dimension for this run. Ranks per node = 8 (from build defaults), but only 4 ranks will be active for TP=4; the remaining 4 GCDs are unused. (Acceptable alternative framing: 4 ranks per node, 4 GPUs per node, constraining GPU visibility to the 4 active GCDs.)

**Step 2 — Walltime estimate**

No throughput measurement at TP=4 is supplied. From the validated data point: at TP=8 the server starts in ~165 s and processes 16 concurrent prompts at 271.5 tok/s. This run has 50 prompts × 50 max_tokens = 2500 tokens of output at lower parallelism. Assuming conservatively ~100 tok/s at TP=4 (roughly half the TP=8 rate, since fewer GCDs), generation takes ~25 s. Adding 165 s startup and a safety margin: ~10 minutes total is a reasonable upper bound. The agent should state these are assumptions, not measurements. A walltime of 1800 s (30 min) is appropriate and conservative.

**Step 3 — Queue elimination**

- batch: 1–9280 nodes, max 24h. Node count 1 is in range; walltime 30 min < 24h. Survives, but g1 is preferred per application guidance for small/fast jobs.
- debug: max 2h, node count not explicitly bounded but intended for high-priority short tests; production inference is not prohibited if under 2h — however, the application notes recommend g1.
- extended: 1–64 nodes, max 24h. Survives on limits, but intended for long-running small jobs.
- g1: 1–2 nodes, max 2h. Node count 1 ≤ 2 ✓; walltime 30 min < 2h ✓. Application defaults and sizing notes explicitly recommend g1 for faster scheduling.
- service: 1–1 nodes, max 24h. Technically valid but intended for service jobs, not inference benchmarks.

Chosen queue: **g1**

**Step 4 — Verdict table for g1**

| Limit | Requested | Queue limit | Result |
|---|---|---|---|
| Node minimum | 1 | 1 | PASS |
| Node maximum | 1 | 2 | PASS |
| Maximum walltime | 1800 s (30 min) | 7200 s (2h) | PASS |

**Step 5 — Scaling note**

The validated run used TP=8 (all 8 GCDs on one node). This run requests TP=4; the application's tensor-parallel design means it runs correctly on 4 GCDs within one node. No multi-node scaling is needed. The PBS Pro conventions from the source facility (qsub, select=, mpiexec) do not apply; Frontier uses Slurm (sbatch, srun).

**Final specification**

- Nodes: 1
- Ranks per node: 8 (build default; 4 active for TP=4)
- Total ranks: 1 × 8 = 8 (4 active)
- GPUs per node: 8 GCDs available; 4 used for TP=4
- Walltime: 1800 s (30 minutes) — assumed, not measured; includes ~165 s startup plus generation time with margin
- Queue: g1
````
