# gpt-oss-120b — alphafold@perlmutter, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
**File:** `input.fasta`

```fasta
# source: https://rest.uniprot.org/uniprotkb/P0CG48.fasta
# human ubiquitin (canonical 76‑residue monomer)

>sp|P0CG48|UBI_HUMAN Ubiquitin OS=Homo sapiens OX=9606 GN=UBB PE=1 SV=1
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
```

**Why this file is needed:**  
AlphaFold reads the protein sequence to be modeled from a FASTA file. This file supplies the exact 76‑residue human ubiquitin sequence (UniProt accession P0CG48) that the AlphaFold pipeline will use for the full database search, model generation (5 recycles), and structure relaxation. No other input files are required for a standard AlphaFold run.
````
