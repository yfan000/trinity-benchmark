# Reference answer — alphafold@perlmutter

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
The single required input file is `input.fasta`, placed in /pscratch/sd/l/lchen/alphafold_run.

Filename: `input.fasta`

```fasta
>sp|P0CG48|UBB_HUMAN Ubiquitin OS=Homo sapiens OX=9606 GN=UBB PE=1 SV=1
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYN
IQKESTLHLVLRLRGG
```

This is the only file required. AlphaFold takes a FASTA-format sequence file as its primary input; all other inputs (uniref90, mgnify, pdb_mmcif databases, model weights) are pre-installed on Perlmutter at /global/cfs/cdirs/dasrepo/alphafold_data and are referenced at runtime via command-line flags, not by files the user prepares.

The sequence is the canonical 76-residue human ubiquitin (UniProt P0CG48). The run is configured as a monomer prediction with 5 models and relaxation, matching the collaborator's settings, which are passed as flags to run_alphafold.py (--model_preset=monomer) rather than written into the input file itself.
````
