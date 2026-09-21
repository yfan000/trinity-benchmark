# Verdicts — alphafold@perlmutter, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `98dca67530dc`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer supplies one required FASTA input, `input.fasta`; `.fasta` is an allowed required-input alternative. |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold FASTA inputs are selected as command-line arguments and the format contract does not specify a fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | The content is recognizably FASTA, beginning with `>sp\|P0CG48\|...` and followed by valid one-letter protein residues. |
| `INP.common.mandatory_sections_present` | major | satisfied | `input.fasta` contains a FASTA `>` header followed by an amino-acid sequence line. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary database, model-weight, checkpoint, or runtime-generated file contents are invented. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The file uses only valid FASTA syntax: a header line and sequence residues; it introduces no AlphaFold input directives. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `input.fasta`, not any listed runtime output such as ranked PDBs, result PKLs, or timings.json. |
| `INP.common.no_truncation` | major | satisfied | The supplied FASTA record contains no ellipses, placeholders, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** ⚠︎ flipped across runs | Although the 76-residue ubiquitin sequence is correct, the header assigns `P0CG48` to `GN=UBA52` and `UBIQ_HUMAN`; UniProt P0CG48 is the UBB_HUMAN (GN=UBB) record, while UBA52 is a different ubiquitin-fusion gene/accession. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer supplies one FASTA input file, `input.fasta`; `.fasta` and `.fa` are alternative accepted AlphaFold input extensions. |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold FASTA inputs are selected by a runtime command-line path and the format contract does not specify a fixed filename. |
| `INP.common.file_identifiable` | major | satisfied | The supplied content is recognisably a FASTA record, beginning `>sp\|P0CG48\|UBQ_HUMAN` and followed by amino-acid-like sequence text. |
| `INP.common.mandatory_sections_present` | major | satisfied | `input.fasta` contains a FASTA header beginning with `>` followed by sequence lines. |
| `INP.common.no_binary_contents` | fatal | satisfied | No database, model-weight, checkpoint, or other binary/runtime-generated file contents are provided. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The answer uses standard FASTA syntax only and does not introduce AlphaFold input-language keywords or directives. |
| `INP.common.no_output_as_input` | major | satisfied | The answer writes only `input.fasta` and does not author any AlphaFold output such as ranked PDBs, result PKLs, or timings files. |
| `INP.common.no_truncation` | major | satisfied | The file content contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | The sequence after the P0CG48 header is not canonical human ubiquitin: it contains the non-ubiquitin segment `KFSNRHQHLQLGKELPGRVGERDKQKCKCKNDCKPLHHK...` and ends in `J`; it is 97 characters rather than the required 76-residue P0CG48 sequence. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides one required FASTA input file, `input.fasta`; `.fasta` and `.fa` are alternative accepted extensions. |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold accepts a user-selected FASTA filename as a command-line input and the format contract does not specify a fixed filename. |
| `INP.common.file_identifiable` | major | satisfied | The file is recognisable as FASTA from its `>` record header and valid one-letter protein sequence. |
| `INP.common.mandatory_sections_present` | major | satisfied | `input.fasta` contains a FASTA header beginning `>sp\|P0CG48\|...` followed by the amino-acid sequence. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, database, checkpoint, model-weight, or runtime-generated file contents are fabricated. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The file uses only FASTA structure (comments, a `>` header, and sequence residues) and contains no AlphaFold input-language directives or invented keywords. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `input.fasta` and does not provide contents for any AlphaFold output such as ranked PDBs, result pickles, or timings files. |
| `INP.common.no_truncation` | major | satisfied | The FASTA sequence is written in full with no ellipses, placeholders, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** ⚠︎ flipped across runs | Although the written sequence is the correct 76-residue ubiquitin monomer, the rationale incorrectly describes the requested five models as “model generation (5 recycles)”; five models and recycle count are different AlphaFold settings, and five recycles would deviate from the stated standard settings. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides `input.fasta`, satisfying the catalog's alternative required FASTA extension requirement (`.fasta` or `.fa`). |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold FASTA input filenames are user-selected command-line arguments; the format contract does not declare a fixed filename. |
| `INP.common.file_identifiable` | major | satisfied | The `input.fasta` content is recognisably FASTA, beginning with `>sp\|P0CG48\|...` and followed by one-letter amino-acid residues. |
| `INP.common.mandatory_sections_present` | major | satisfied | `input.fasta` has the required FASTA structure: a `>` header line followed by residue sequence lines. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary contents are fabricated: the `.mmtf.gz` archive and checkpoint artifacts are listed without invented text contents. |
| `INP.common.no_invented_keywords` | fatal | **violated** | The answer invents an `input.json` AlphaFold configuration language with unsupported fields such as `"model": "resnet"`, `mmtf`, and `num_relaxation_steps`; standard AlphaFold requires only FASTA input and runtime command-line flags, not this JSON schema. |
| `INP.common.no_output_as_input` | major | satisfied | `output.pdb`, checkpoint files, and the database archive are only labeled as runtime-produced and no contents are authored for them. |
| `INP.common.no_truncation` | major | satisfied | The authored code blocks contain no ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | Although labeled human ubiquitin P0CG48, the FASTA sequence starts `MVLSPADKTNVKAAWGKVGAHAGEY...` and is hundreds of residues long, rather than the specified canonical 76-residue ubiquitin sequence. |
