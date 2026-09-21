# Prompt — pytorch@sophia, enriched arm

Subtask: **Input preparation**. The base prompt with catalog material inserted — format contract, setup and run commands, scaling notes. Derived from the base arm by verified-reversible text insertion, never regenerated, so the two arms are paired.

````
**Task:** Determine and write all input files needed to restart a distributed mixed-precision ResNet-50 training job from an existing checkpoint using the software selection already made.

**Workload:**
- Problem: ResNet-50 image classification on a 100,000-image subset, batch size 256 per GPU, mixed precision, 10 epochs
- System: Sophia (ALCF)
- Working directory: `/eagle/MatGenome/bkowalski/pytorch_run`
- Software: PyTorch (MPI)
- Restart context: training was interrupted; a checkpoint file exists in the working directory from a previous run and must be loaded to resume from where training stopped

**Worked example:**
```python
# source: https://raw.githubusercontent.com/pytorch/examples/main/distributed/ddp-tutorial-series/multigpu.py
# a real input for a DIFFERENT system — form only

import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from datautils import MyTrainDataset

import torch.multiprocessing as mp
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
import os


def ddp_setup(rank, world_size):
    """
    Args:
        rank: Unique identifier of each process
        world_size: Total number of processes
    """
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    torch.cuda.set_device(rank)
    init_process_group(backend="nccl", rank=rank, world_size=world_size)

class Trainer:
    def __init__(
        self,
        model: torch.nn.Module,
        train_data: DataLoader,
        optimizer: torch.optim.Optimizer,
        gpu_id: int,
        save_every: int,
    ) -> None:
        self.gpu_id = gpu_id
        self.model = model.to(gpu_id)
        self.train_data = train_data
        self.optimizer = optimizer
        self.save_every = save_every
        self.model = DDP(model, device_ids=[gpu_id])

    def _run_batch(self, source, targets):
        self.optimizer.zero_grad()
[... 63 more lines of this file omitted — the form above is what matters]
```

**Input file format:**
(the facility catalog records no format requirements for this application — determine the file contents yourself)

**System context:**
per node: 128 CPU cores per node, 8 x A100 per node, 503 GB memory per node
filesystems available: /eagle, /home

**Instructions:** Determine the parameters and configuration the application requires for this workload, then write out each input file in full. Do NOT write a job script or scheduler directives — input files only.

(a) Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.
(b) Never fabricate the contents of binary or runtime-generated files (databases, wavefunction or checkpoint files, restart files, outputs) — list those as produced at runtime instead of writing text into them.
(c) Treat the worked example above as a demonstration of FORM ONLY: its numerical values, dataset names, and comment headers describe a different system and must not be carried over.
(d) Make sure any count you declare matches the entries you actually write out.

**Output:** For each required file, give its filename and its complete contents in a fenced code block, then one line on why each is needed.
````
