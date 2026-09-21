# Prompt — alphafold@perlmutter

Subtask: **Input preparation**. Base arm, exactly as the model received it.

````
**Task:** Construct the input file(s) required by AlphaFold to predict the structure of human ubiquitin.

**Workload:**
- Scientific problem: human ubiquitin (UniProt P0CG48), 76-residue monomer, full database search, 5 models with relaxation
- Target system: Perlmutter (NERSC)
- Working directory: /pscratch/sd/l/lchen/alphafold_run
- Reproducing a collaborator's earlier result; no deviation from standard run settings

**Required input files:**
Write one file, in a fenced code block:
```
input.fasta
```

**Worked example** (real input for a DIFFERENT system — form only):
```
# source: https://rest.uniprot.org/uniprotkb/P0DTC2.fasta
# a real input for a DIFFERENT system — form only

>sp|P0DTC2|SPIKE_SARS2 Spike glycoprotein OS=Severe acute respiratory syndrome coronavirus 2 OX=2697049 GN=S PE=1 SV=1
MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFS
NVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIV
NNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLE
GKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQT
LLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETK
CTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISN
CVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIAD
YNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPC
NGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVN
FNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITP
GTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSY
ECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTI
SVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQE
VFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDC
LGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAM
QMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALN
TLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRA
SANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPA
ICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDP
LQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDL
QELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDD
SEPVLKGVKLHYT
```

**Instructions:** Determine the parameters and configuration AlphaFold requires for this workload, then write out each input file in full. Do NOT write a job script or scheduler directives — input files only.

(a) Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.
(b) Never fabricate the contents of binary or runtime-generated files (databases, checkpoint files, outputs) — list those as produced at runtime instead of writing text into them.
(c) Treat the worked example above as a demonstration of FORM ONLY: header line syntax, sequence wrapping, FASTA identifier format. Its protein sequence, species, accession, and comment header describe a DIFFERENT system and must not be carried over.
(d) Make sure any count you declare matches the entries you actually write out (e.g., if you state a sequence is 76 residues, verify the written sequence is exactly 76 amino acid characters).

**Output:** For each required file, give its filename and its complete contents in a fenced code block, then one line on why each is needed. You are writing file contents as text; you have no filesystem access and are not expected to create anything on disk.
````
