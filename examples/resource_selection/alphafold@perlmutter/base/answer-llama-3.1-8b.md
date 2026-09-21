# llama-3.1-8b — alphafold@perlmutter, base arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 3 of 10 requirements violated).

````
## Resource Specification

Based on the workload and system information, the following resource specification is chosen:

- **Nodes**: 1
- **Ranks per Node**: 64 (as per Build Defaults)
- **Total Ranks**: 1 node × 64 ranks per node = 64
- **GPUs per Node**: 4 (as per Build Defaults)
- **GPUs**: 1 node × 4 GPUs per node = 4
- **Walltime**: 6 hours (as per queue express_amsc)
- **Queue**: express_amsc

## Reasoning

### (a) Choosing a Legal Queue

#### 1. Derive Walltime

The problem is a full database search with 5 models and relaxation, which is a CPU-intensive task. However, we also have a GPU-intensive task (AlphaFold structure prediction). Assuming the MSA computation takes about 1-2 hours (a rough estimate) and the structure prediction takes about 1-2 hours per model (another rough estimate), the total walltime can be estimated as follows:

- MSA computation: 1-2 hours
- Structure prediction (5 models): 5 × 1-2 hours = 5-10 hours
- Total walltime: 6-12 hours

To be safe, let's assume we need about 12 hours for the entire task.

#### 2. Eliminate Ineligible Queues

Based on the queue table, the following queues can be eliminated:

- debug: maximum walltime is 30 minutes, which is too short
- interactive: maximum walltime is 4 hours, which is too short
- jupyter: maximum walltime is 6 hours, which is too short
- preempt: node range is 1-128, which is too high for a single job
- overrun: maximum walltime is 48 hours, which is too long

The following queues are eligible:

- express_amsc: maximum walltime is 6 hours
- regular: maximum walltime is 48 hours
- premium: maximum walltime is 48 hours
- shared: maximum walltime is 48 hours

#### 3. Choose the Best Queue

Based on the queue table, the express_amsc queue has the shortest maximum walltime, which is 6 hours. This matches our estimated walltime of 12 hours.

| Queue | Node Minimum | Node Maximum | Maximum Walltime |
| --- | --- | --- | --- |
| express_amsc | PASS | PASS | PASS |
| regular | PASS | PASS | FAIL (too long) |
| premium | PASS | PASS | FAIL (too long) |
| shared | PASS | PASS | FAIL (too long) |

### (b) Ranks per Node and GPUs per Node

According to the Build Defaults, the ranks-per-node and GPUs-per-rank are:

- Ranks per Node: 64
- GPUs per Rank: 1 (single GPU per run typical)

### (c) Assumptions and Margin

We assumed that the MSA computation and structure prediction tasks take about 1-2 hours each. We added a margin of 1-2 hours to account for any unexpected delays.

### (d) Scaling Guidance

The scaling guidance supplied with the application recommends parallelizing by submitting multiple jobs with different FASTA inputs. However, this does not apply to this run, as we are doing a parameter sweep with many similar runs predicting the same target independently.

### (e) Restatement of Resource Specification

Based on the above reasoning, the resource specification is:

- **Nodes**: 1
- **Ranks per Node**: 64
- **Total Ranks**: 1 node × 64 ranks per node = 64
- **GPUs per Node**: 4
- **GPUs**: 1 node × 4 GPUs per node = 4
- **Walltime**: 6 hours
- **Queue**: express_amsc
````
