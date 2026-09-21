# Verdicts — lammps@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `98dca67530dc`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The response provides exactly the requested sole input file, `in.lj_argon`, with complete LAMMPS deck contents. |
| `INP.common.exact_filenames_used` | major | not_applicable | LAMMPS accepts the input filename supplied with `-in`; its format contract does not define a fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | The deck is recognisably LAMMPS input and includes content markers such as `units`, `atom_style`, `pair_style`, and `fix`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `in.lj_argon` contains all mandatory LAMMPS sections: `units lj`, `atom_style atomic`, and `run 100000`. |
| `INP.common.no_binary_contents` | fatal | satisfied | No restart, trajectory, or other binary/runtime-generated file contents are fabricated; only a text LAMMPS input deck is provided. |
| `INP.common.no_invented_keywords` | fatal | satisfied | All directives used are valid LAMMPS commands, including `lattice`, `region`, `create_box`, `create_atoms`, `velocity`, `pair_style`, `neigh_modify`, and `fix`. |
| `INP.common.no_output_as_input` | major | satisfied | The response writes only `in.lj_argon` and does not author contents for runtime outputs such as `log.lammps` or trajectory/dump files. |
| `INP.common.no_truncation` | major | satisfied | The provided input deck is complete and contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The 50×50×50 fcc-cell region produces 4×50^3 = 500,000 atoms and the deck uses the required density 0.8442, temperature 0.72, LJ parameters/cutoff, NVE integration, and 100,000 steps. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The response provides the single explicitly required LAMMPS input file, `in.lj_argon`. |
| `INP.common.exact_filenames_used` | major | not_applicable | LAMMPS reads an input filename supplied with `-in`; it has no fixed mandatory input filename. |
| `INP.common.file_identifiable` | major | satisfied | The contents use recognizable LAMMPS directives including `units`, `atom_style`, `pair_style`, `fix`, and `run`. |
| `INP.common.mandatory_sections_present` | major | satisfied | The file contains `units lj`, `atom_style atomic`, and `run 100000`. |
| `INP.common.no_binary_contents` | fatal | satisfied | No restart, trajectory, or other binary/runtime-generated file contents are invented. |
| `INP.common.no_invented_keywords` | fatal | satisfied | All directives used, including `lattice`, `region`, `create_box`, `create_atoms`, `velocity`, `neigh_modify`, and `fix`, are valid LAMMPS input commands. |
| `INP.common.no_output_as_input` | major | satisfied | The response authors only `in.lj_argon` and does not provide contents for runtime outputs such as `log.lammps` or dump files. |
| `INP.common.no_truncation` | major | satisfied | The supplied input deck is complete and contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | `lattice fcc 0.8442` with a 50x50x50 lattice-unit box yields 4×50^3 = 500,000 atoms, and the deck specifies T=0.72, lj/cut 2.5, NVE, and `run 100000`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The response provides the single required LAMMPS input file, `in.lj_argon`, with a valid `.in` extension. |
| `INP.common.exact_filenames_used` | major | not_applicable | LAMMPS reads an input filename supplied through `lmp -in <file>` and has no fixed mandatory input filename. |
| `INP.common.file_identifiable` | major | satisfied | The file is recognizably a LAMMPS deck and includes markers such as `units`, `atom_style`, `pair_style`, and `fix`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `in.lj_argon` contains the mandatory LAMMPS commands `units lj`, `atom_style atomic`, and `run 100000`. |
| `INP.common.no_binary_contents` | fatal | satisfied | The response writes only the text LAMMPS input script and does not invent restart, trajectory, log, or other runtime-generated file contents. |
| `INP.common.no_invented_keywords` | fatal | satisfied | All directives used, including `lattice`, `region`, `create_box`, `velocity`, `neigh_modify`, and `fix`, are valid LAMMPS input commands and keyword forms. |
| `INP.common.no_output_as_input` | major | satisfied | No runtime output file is authored; the only dump command is commented out (`#dump 1 all atom 1000 dump.lj_argon`). |
| `INP.common.no_truncation` | major | satisfied | The supplied input script is complete and contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | In LJ units, `lattice fcc 1.6788` interprets 1.6788 as the fcc reduced number density, not as a lattice constant; therefore the generated 50×50×50 fcc system has density 1.6788 rather than the required 0.8442. It should use `lattice fcc 0.8442`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The response provides the single task-required LAMMPS input file, `in.lj_argon`, and the prompt explicitly required exactly one input file. |
| `INP.common.exact_filenames_used` | major | not_applicable | LAMMPS input filenames are supplied to `lmp -in <file>` and the format contract does not define a fixed filename. |
| `INP.common.file_identifiable` | major | satisfied | The file contains recognizable LAMMPS commands including `units`, `atom_style`, `pair_style`, and `fix`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `in.lj_argon` contains `units lj`, `atom_style atomic`, and `run 100000`. |
| `INP.common.no_binary_contents` | fatal | satisfied | No restart, trajectory, or other binary/runtime-generated file contents are fabricated. |
| `INP.common.no_invented_keywords` | fatal | satisfied | All directives used, including `lattice`, `region`, `create_box`, `create_atoms`, `velocity`, `pair_style`, `neigh_modify`, and `fix`, are valid LAMMPS commands. |
| `INP.common.no_output_as_input` | major | satisfied | The response authors only `in.lj_argon` and does not provide contents for `log.lammps`, dump files, or trajectory outputs. |
| `INP.common.no_truncation` | major | satisfied | The supplied input deck is complete and contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | The `region box block -1 1 -1 1 -1 1` spans only 2×2×2 fcc lattice cells, producing 32 atoms rather than 500,000, and `velocity all create 3.0 ...` sets temperature 3.0 rather than the required reduced temperature 0.72. |
