# llama-3.1-8b — alphafold@perlmutter, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 9 requirements violated).

````
### input.fasta
```fasta
>sp|P0CG48|UBIQ_HUMAN Ubiquitin OS=Homo sapiens OX=9606 GN=UBB PE=1 SV=1
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG
KLVATVAHKSDAEFVEVSAQTDKEGIPADNYLQDNFYINPSDKTHPERAARVLVDPVNFK
RTLLKAEELEGCEVQHADPVQVVKVDEADPVVFKLLDGIHAEQIQHDLSFPEVSVNVDL
KVLVNFPETTVPQVTVSAVDDMQKIKEVLNADIKLELDHGIDTKDLLEHYYMREAELRLR
DDMVLLEFAFPQVTKVLHPSAEIKVLNTPSGEQVLQSKHVDDAEKLLISDVNSLLGIYD
TTRDNLRILIRDFKTFLKSGAAIFASVLHLKPVQLDDHVNGQVAVVYTLPPSQQRKIV
```

This is the input FASTA file containing the sequence of human ubiquitin.

### input.json
```json
{
  "model": "resnet",
  "data": {
    "mmtf": {
      "database": {
        "url": "https://alphafold.ebi.ac.uk/files/AF-Db-2022-04-01.mmtf.gz",
        "path": "/pscratch/sd/l/lchen/alphafold_run/AF-Db-2022-04-01.mmtf.gz"
      },
      "max_msa_sequences": 1000,
      "max_msa_sequence_length": 1000,
      "max_msa_sequence_identity": 1000,
      "max_msa_sequence_similarity": 1000,
      "max_msa_sequence_length_diversity": 1000,
      "max_msa_sequence_identity_diversity": 1000
    },
    "msa": {
      "max_msa_sequences": 1000,
      "max_msa_sequence_length": 1000,
      "max_msa_sequence_identity": 1000,
      "max_msa_sequence_similarity": 1000,
      "max_msa_sequence_length_diversity": 1000,
      "max_msa_sequence_identity_diversity": 1000
    }
  },
  "templates": {
    "max_templates": 1000,
    "max_template_msa_sequences": 1000,
    "max_template_msa_sequence_length": 1000,
    "max_template_msa_sequence_identity": 1000,
    "max_template_msa_sequence_similarity": 1000,
    "max_template_msa_sequence_length_diversity": 1000,
    "max_template_msa_sequence_identity_diversity": 1000
  },
  "relax": {
    "num_relaxation_steps": 5,
    "relaxation_temperature": 300,
    "relaxation_time": 1000,
    "relaxation_step_size": 0.1
  }
}
```

This is the input JSON file containing the configuration parameters for the AlphaFold run.

### input.sh
```bash
#!/bin/bash

# Set the working directory
WORKDIR=/pscratch/sd/l/lchen/alphafold_run

# Set the database URL
DATABASE_URL="https://alphafold.ebi.ac.uk/files/AF-Db-2022-04-01.mmtf.gz"

# Set the number of models to generate
NUM_MODELS=5

# Set the number of relaxation steps
NUM_RELAXATION_STEPS=5

# Run the AlphaFold command
alphafold --input input.fasta --output output.pdb --database $DATABASE_URL --num_models $NUM_MODELS --relaxation_steps $NUM_RELAXATION_STEPS
```

This is the input shell script that runs the AlphaFold command. Note that this script is not intended to be run directly, but rather serves as a template for the actual job script.

### output.pdb
*Produced at runtime*

This is the output PDB file containing the predicted structure of human ubiquitin.

### AF-Db-2022-04-01.mmtf.gz
*Produced at runtime*

This is the AlphaFold database file used for the run.

### checkpoint.pdb
*Produced at runtime*

This is the checkpoint PDB file used for the run.

### checkpoint.mmtf
*Produced at runtime*

This is the checkpoint MMTF file used for the run.
````
