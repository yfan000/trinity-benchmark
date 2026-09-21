# nemotron-3-ultra — pytorch@sophia, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 4 requirements violated).

````
**Selected Application: PyTorch (MPI)**

**Why it fits:**
- **Native NCCL Support:** The installed PyTorch 2.5.0a0 is built from source on Sophia with explicit **MPI+NCCL distributed backends**, directly satisfying the requirement for multi-GPU collective communication via NCCL for gradient synchronization.
- **Data Parallelism Ready:** PyTorch’s `DistributedDataParallel` (DDP) module is the standard, production-grade approach for single-node, multi-GPU data-parallel training of models like ResNet-50, leveraging NCCL for efficient all-reduce operations.
- **Architecture Alignment:** Built specifically for Sophia’s A100 nodes, ensuring optimal CUDA compatibility and performance.
- **Production Suitability:** As a core framework (rather than a higher-level wrapper like DeepSpeed), it minimizes overhead and complexity for a straightforward data-parallel CNN training workload, while respecting queue limits via standard MPI launch mechanisms (e.g., `torchrun` or MPI wrappers).
````
