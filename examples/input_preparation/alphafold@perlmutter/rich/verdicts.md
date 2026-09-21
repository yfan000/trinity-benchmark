# Verdicts — alphafold@perlmutter, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `98dca67530dc`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the single requested alternative required input type as `input.fasta`. |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold FASTA files are supplied as command-line inputs and the format contract does not define `fixed_filenames: true`. |
| `INP.common.file_identifiable` | major | satisfied | The emitted content is recognisable as a protein FASTA record, with a `>` header and standard one-letter amino-acid sequence. |
| `INP.common.mandatory_sections_present` | major | satisfied | `input.fasta` contains a FASTA header beginning with `>sp\|P0CG48\|...` followed by sequence residues. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, database, checkpoint, model-weight, or runtime-generated file contents are authored. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The answer uses FASTA header and sequence content only and introduces no AlphaFold input-language directives or keywords. |
| `INP.common.no_output_as_input` | major | satisfied | The answer writes only `input.fasta`, not any runtime output such as `ranked_*.pdb`, `result_model_*.pkl`, or `timings.json`. |
| `INP.common.no_truncation` | major | satisfied | The FASTA record is fully written without ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The sequence `MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG` is the 76-residue human ubiquitin sequence for UniProt P0CG48. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides one required AlphaFold FASTA input file named `input.fasta`; `.fasta` and `.fa` are alternative accepted extensions. |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold FASTA inputs are selected by command-line argument and the format contract does not establish a fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | The supplied content is recognisable as a FASTA record through the `>sp\|P0CG48\|...` header and amino-acid-like sequence lines. |
| `INP.common.mandatory_sections_present` | major | satisfied | `input.fasta` contains a FASTA header beginning with `>` followed by sequence text. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, database, model-weight, checkpoint, or runtime-generated file contents are fabricated. |
| `INP.common.no_invented_keywords` | fatal | satisfied ⚠︎ flipped across runs | No AlphaFold input directives or unsupported configuration keywords are used; the supplied file is a FASTA record. |
| `INP.common.no_output_as_input` | major | satisfied | The answer writes only `input.fasta` and does not author any AlphaFold output such as ranked PDBs, result pickles, or timings files. |
| `INP.common.no_truncation` | major | satisfied | The response contains no ellipses, placeholder paths, TODOs, or explicit truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | Although the header identifies P0CG48, the written sequence is not the canonical 76-residue human ubiquitin sequence and additionally ends with the non-residue text `</h1>`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides one required AlphaFold FASTA input, `input.fasta`; `.fasta` and `.fa` are alternative accepted extensions. |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold accepts the FASTA filename as a runtime command-line argument; the format contract does not specify a fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | The supplied content is recognizably FASTA format, with a `>` record header and valid one-letter protein residues. |
| `INP.common.mandatory_sections_present` | major | satisfied | `input.fasta` contains a FASTA header beginning with `>sp\|P0CG48\|...` followed by amino-acid sequence lines. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, database, checkpoint, model-weight, or runtime-generated file contents are written. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The file uses standard FASTA syntax only and contains no AlphaFold input-language directives or invented keywords. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `input.fasta`, not any AlphaFold output such as ranked PDBs, result PKLs, or timings files. |
| `INP.common.no_truncation` | major | satisfied | The FASTA record is fully written with no ellipses, placeholders, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The sequence `MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG` is the 76-residue human ubiquitin sequence for UniProt P0CG48. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The required FASTA input is provided as `input.fasta`, which has an accepted `.fasta` extension. |
| `INP.common.exact_filenames_used` | major | not_applicable | AlphaFold FASTA inputs are selected as command-line arguments and the format contract does not specify any fixed input filename. |
| `INP.common.file_identifiable` | major | satisfied | `input.fasta` is recognisable as FASTA because it contains a `>` header followed by amino-acid sequence characters. |
| `INP.common.mandatory_sections_present` | major | **violated** | Although `input.fasta` has a FASTA `>` header, the additionally authored `uniprot.fasta` contains only `# This file will be generated at runtime` and no required FASTA header. |
| `INP.common.no_binary_contents` | fatal | **violated** | The answer authors a `uniprot.fasta` placeholder while describing it as a runtime-generated database file, rather than merely listing the database as externally provided at runtime. |
| `INP.common.no_invented_keywords` | fatal | **violated** | The extra `input.json` uses unsupported AlphaFold input-language configuration keys such as `num_recycle`, `relax`, `db`, and `target`; AlphaFold's required user-prepared input format here is FASTA. |
| `INP.common.no_output_as_input` | major | satisfied | The answer does not author any file matching AlphaFold's declared output patterns such as `output/*/ranked_*.pdb`, `result_model_*.pkl`, or `timings.json`. |
| `INP.common.no_truncation` | major | **violated** | The authored `uniprot.fasta`, `run.sh`, and `submission.sh` contents are placeholders stating they "will be generated at runtime," not complete file contents. |
| `INP.common.values_match_physical_system` | major | **violated** | The sequence under `>sp\|P0CG48\|UBIQ_HUMAN` is not the canonical 76-residue human ubiquitin sequence for UniProt P0CG48 and is substantially longer than 76 residues. |
