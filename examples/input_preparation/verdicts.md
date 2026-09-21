# Verdicts — llama-3.1-8b on alphafold@perlmutter

Majority across three judge replicates, judged by gpt56terra under rubric **r27**. Severities shown are the current library, **r28** (sha `98dca67530dc`).

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | **satisfied** | The answer provides `input.fasta`, satisfying the catalog's alternative required FASTA extension requirement (`.fasta` or `.fa`). |
| `INP.common.exact_filenames_used` | major | **not_applicable** | AlphaFold FASTA input filenames are user-selected command-line arguments; the format contract does not declare a fixed filename. |
| `INP.common.file_identifiable` | major | **satisfied** | The `input.fasta` content is recognisably FASTA, beginning with `>sp\|P0CG48\|...` and followed by one-letter amino-acid residues. |
| `INP.common.mandatory_sections_present` | major | **satisfied** | `input.fasta` has the required FASTA structure: a `>` header line followed by residue sequence lines. |
| `INP.common.no_binary_contents` | fatal | **satisfied** | No binary contents are fabricated: the `.mmtf.gz` archive and checkpoint artifacts are listed without invented text contents. |
| `INP.common.no_invented_keywords` | fatal | **violated** | The answer invents an `input.json` AlphaFold configuration language with unsupported fields such as `"model": "resnet"`, `mmtf`, and `num_relaxation_steps`; standard AlphaFold requires only FASTA input and runtime command-line flags, not this JSON schema. |
| `INP.common.no_output_as_input` | major | **satisfied** | `output.pdb`, checkpoint files, and the database archive are only labeled as runtime-produced and no contents are authored for them. |
| `INP.common.no_truncation` | major | **satisfied** | The authored code blocks contain no ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.not_copied_from_example` | removed in r28 | **satisfied** | The answer does not reuse the worked example's SARS-CoV-2 Spike accession, header, species, or sequence. |
| `INP.common.values_match_physical_system` | major | **violated** | Although labeled human ubiquitin P0CG48, the FASTA sequence starts `MVLSPADKTNVKAAWGKVGAHAGEY...` and is hundreds of residues long, rather than the specified canonical 76-residue ubiquitin sequence. |
