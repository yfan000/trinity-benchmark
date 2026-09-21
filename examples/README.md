# Examples

The whole of corpus v8 as readable markdown: for each anchor, the prompt as each arm
posed it, Claude's reference answer, what all four models wrote, and every requirement
verdict with the judge's evidence. Same 320 graded answers the HTML browsers show.

Judged by `gpt56terra` at k=3 under rubric **r27**; severities shown are the current library, **r28**.

**198 of 320 attempts passed.** An attempt is one model on one anchor in one arm; a pass is 2/2 on correctness, completeness and usability with no fatal violation, taken as the majority of three judge replicates.


## software_selection — 60/80

Name the application to run for a stated workload on a stated machine, and justify it from what the facility actually provides.

- [`alphafold@perlmutter`](software_selection/alphafold@perlmutter/) — 8/8 passed
- [`gromacs@sirius`](software_selection/gromacs@sirius/) — 4/8 passed
- [`hpl@crux`](software_selection/hpl@crux/) — 8/8 passed
- [`lammps@polaris`](software_selection/lammps@polaris/) — 0/8 passed
- [`nekrs@polaris`](software_selection/nekrs@polaris/) — 8/8 passed
- [`nwchem@polaris`](software_selection/nwchem@polaris/) — 7/8 passed
- [`pytorch@sophia`](software_selection/pytorch@sophia/) — 7/8 passed
- [`qe@aurora`](software_selection/qe@aurora/) — 4/8 passed
- [`qmcpack@aurora`](software_selection/qmcpack@aurora/) — 8/8 passed
- [`vllm@frontier`](software_selection/vllm@frontier/) — 6/8 passed

## input_preparation — 16/80

Write the input files the application needs, complete and runnable, for the physical system the prompt describes.

- [`alphafold@perlmutter`](input_preparation/alphafold@perlmutter/) — 2/8 passed
- [`gromacs@sirius`](input_preparation/gromacs@sirius/) — 0/8 passed
- [`hpl@crux`](input_preparation/hpl@crux/) — 6/8 passed
- [`lammps@polaris`](input_preparation/lammps@polaris/) — 4/8 passed
- [`nekrs@polaris`](input_preparation/nekrs@polaris/) — 0/8 passed
- [`nwchem@polaris`](input_preparation/nwchem@polaris/) — 0/8 passed
- [`pytorch@sophia`](input_preparation/pytorch@sophia/) — 1/8 passed
- [`qe@aurora`](input_preparation/qe@aurora/) — 0/8 passed
- [`qmcpack@aurora`](input_preparation/qmcpack@aurora/) — 0/8 passed
- [`vllm@frontier`](input_preparation/vllm@frontier/) — 3/8 passed

## resource_selection — 64/80

Choose nodes, ranks, walltime and queue for a stated job, within the limits the prompt states.

- [`alphafold@perlmutter`](resource_selection/alphafold@perlmutter/) — 6/8 passed
- [`gromacs@sirius`](resource_selection/gromacs@sirius/) — 4/8 passed
- [`hpl@crux`](resource_selection/hpl@crux/) — 7/8 passed
- [`lammps@polaris`](resource_selection/lammps@polaris/) — 6/8 passed
- [`nekrs@polaris`](resource_selection/nekrs@polaris/) — 8/8 passed
- [`nwchem@polaris`](resource_selection/nwchem@polaris/) — 7/8 passed
- [`pytorch@sophia`](resource_selection/pytorch@sophia/) — 7/8 passed
- [`qe@aurora`](resource_selection/qe@aurora/) — 6/8 passed
- [`qmcpack@aurora`](resource_selection/qmcpack@aurora/) — 6/8 passed
- [`vllm@frontier`](resource_selection/vllm@frontier/) — 7/8 passed

## batch_job_creation — 58/80

Write the submission script: directives, environment, launch command.

- [`alphafold@perlmutter`](batch_job_creation/alphafold@perlmutter/) — 6/8 passed
- [`gromacs@sirius`](batch_job_creation/gromacs@sirius/) — 3/8 passed
- [`hpl@crux`](batch_job_creation/hpl@crux/) — 5/8 passed
- [`lammps@polaris`](batch_job_creation/lammps@polaris/) — 7/8 passed
- [`nekrs@polaris`](batch_job_creation/nekrs@polaris/) — 4/8 passed
- [`nwchem@polaris`](batch_job_creation/nwchem@polaris/) — 7/8 passed
- [`pytorch@sophia`](batch_job_creation/pytorch@sophia/) — 7/8 passed
- [`qe@aurora`](batch_job_creation/qe@aurora/) — 7/8 passed
- [`qmcpack@aurora`](batch_job_creation/qmcpack@aurora/) — 6/8 passed
- [`vllm@frontier`](batch_job_creation/vllm@frontier/) — 6/8 passed
