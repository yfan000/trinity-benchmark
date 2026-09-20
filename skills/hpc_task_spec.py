"""Seed HPC task categories, their variation axes, and which ALCF docs ground each.

The variation axes matter as much as the categories. Without them a category collapses into
one template restated N times, and the resulting skill profile would describe that template
rather than the task. "Failure diagnosis" spanning OOM, walltime, rank mismatch, quota,
module conflict and preemption is a real distribution; six rephrasings of an OOM is not.

This is a SEED list, open to revision — hpc_discovery.py exists to surface categories it
misses before anything is locked.
"""
from __future__ import annotations

# HPC knowledge is deliberately absent as a task. It is a prerequisite that cuts across every
# task below rather than a sibling of them, so it is modelled as a cross-cutting attribute
# (see hpc_build_mapping.py) instead of competing as a seventh row.
SEED_TASKS = {
    "Job submission": {
        "description": "Composing and submitting a batch or interactive job that runs as intended.",
        "docs": ["polaris-running-jobs", "example-job-scripts", "qsub-options", "aurora-running-jobs"],
        "variations": [
            "a first batch submission that is rejected or silently does nothing",
            "a multi-node MPI job with wrong rank/thread placement",
            "requesting GPUs and getting affinity or visibility wrong",
            "an ensemble or job-array style submission of many similar runs",
            "an interactive debug session on compute nodes",
            "using a machine reservation for a deadline run",
        ],
    },
    "Job monitoring": {
        "description": "Observing queued or running jobs and interpreting their state.",
        "docs": ["polaris-running-jobs", "running-jobs-overview", "queue-scheduling"],
        "variations": [
            "job stuck in the queue far longer than expected",
            "checking progress and output of a currently running job",
            "understanding queue position, priority and backfill",
            "a job that appears to run but produces no output",
            "reconciling accounting or node-hour charges after a run",
        ],
    },
    "Performance analysis": {
        "description": "Measuring and explaining how fast a code runs and why.",
        "docs": ["polaris-perf-nsight", "aurora-perf-tools", "aurora-node-perf", "polaris-using-gpus"],
        "variations": [
            "poor GPU utilization on a code that was expected to be GPU-bound",
            "MPI scaling that flattens or regresses beyond some node count",
            "an I/O bottleneck suspected but not yet confirmed",
            "profiling a run and interpreting the tool's output",
            "a code slower on this machine than on the user's local cluster",
        ],
    },
    "Workflow management": {
        "description": "Coordinating multi-step, dependent, or long-running campaigns of jobs.",
        "docs": ["globus-compute", "example-job-scripts", "running-jobs-overview", "data-globus"],
        "variations": [
            "chaining dependent stages so one starts when another finishes",
            "a parameter sweep or ensemble campaign across many jobs",
            "checkpoint and restart across walltime limits",
            "staging input data in and results out around a run",
            "driving jobs programmatically from an external service",
        ],
    },
    "Failure diagnosis": {
        "description": "Determining why a job failed or misbehaved from the evidence available.",
        "docs": ["known-issues", "polaris-running-jobs", "polaris-debug-cudagdb", "aurora-debugging"],
        "variations": [
            "out-of-memory, on host or device",
            "walltime exceeded and the job killed mid-run",
            "MPI rank count inconsistent with the node/ppn request",
            "filesystem quota exceeded, or writes failing partway through",
            "module or library conflict producing a link or runtime error",
            "a preemptable job killed unexpectedly",
            "a job that fails only at large node counts",
        ],
    },
    "Resource selection": {
        "description": "Choosing the right machine, queue, node count, walltime and storage.",
        "docs": ["queue-scheduling", "running-jobs-overview", "data-filesystems", "polaris-running-jobs"],
        "variations": [
            "sizing node count and walltime for an unfamiliar run",
            "choosing among the production queues for turnaround",
            "topology or placement choices for communication-heavy runs",
            "picking the right filesystem for a given I/O pattern",
            "deciding between machines, or between CPU and GPU execution",
        ],
    },
    "Data management": {
        "description": "Moving, storing and retaining data around computation.",
        "docs": ["data-globus", "data-sftp-scp", "data-filesystems", "data-quotas", "data-hpss"],
        "variations": [
            "transferring a large dataset in or out efficiently",
            "hitting a quota and needing to reorganize storage",
            "archiving or retrieving long-term data",
            "sharing data with collaborators or another facility",
        ],
    },
    "Environment and software": {
        "description": "Building, installing and loading the software a run depends on.",
        "docs": ["polaris-compiling", "polaris-spack", "polaris-containers", "polaris-programming"],
        "variations": [
            "a build that fails against the system compilers or MPI",
            "installing or locating a third-party library",
            "getting a container to run correctly on compute nodes",
            "reproducing an environment across machines or over time",
        ],
    },
}

# Beyond the user's seven, two categories were added here from the ALCF documentation's own
# structure — it devotes whole sections to data management and to compiling/software that the
# seed list had nowhere to put. Discovery will test whether they earn their place, and whether
# anything else is still missing.
USER_SEED = ["Job submission", "Job monitoring", "Performance analysis", "Workflow management",
             "Failure diagnosis", "Resource selection"]
ADDED_FROM_DOCS = ["Data management", "Environment and software"]
