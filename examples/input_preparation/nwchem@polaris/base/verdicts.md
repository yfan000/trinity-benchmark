# Verdicts — nwchem@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `98dca67530dc`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides ten complete `.nw` files, one at each of `run_01/input.nw` through `run_10/input.nw`. |
| `INP.common.exact_filenames_used` | major | not_applicable | NWChem input decks are selected by a command-line filename and the catalog specifies no fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | Each file is recognizably an NWChem deck, containing markers including `start`, `geometry`, `basis`, `dft`, `task`, and `echo`. |
| `INP.common.mandatory_sections_present` | major | satisfied | Every deck includes both a `geometry units angstrom ... end` block and a final `task dft energy` directive. |
| `INP.common.no_binary_contents` | fatal | satisfied | No database, wavefunction, checkpoint, or other runtime-generated/binary file contents are invented. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The decks use valid NWChem directives and blocks, including `start`, `geometry`, `symmetry`, `basis`, `charge`, `dft`, `mult`, `xc`, `grid`, `convergence energy`, and `task dft energy`. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `.nw` input files and does not provide contents for `.out`, `.log`, `.db`, `.movecs`, or other runtime outputs. |
| `INP.common.no_truncation` | major | satisfied | All ten input decks are fully written with no ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** ⚠︎ flipped across runs | Although the O-H distances are effectively the requested values, the coordinates correspond to an H-O-H angle of about 104.36° (e.g. run_01 has atan2(0.7109,0.5519)*2), not the specified fixed 104.5°; the discrepancy is larger than four-decimal coordinate rounding. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides ten `.nw` files, one in each required `run_01/` through `run_10/` subdirectory. |
| `INP.common.exact_filenames_used` | major | not_applicable | NWChem inputs are command-line-selected `.nw` files and the format contract does not specify a fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | Each file is recognisably an NWChem deck, containing `echo`, `geometry`, `basis`, `dft`, and `task` directives. |
| `INP.common.mandatory_sections_present` | major | satisfied | Every deck contains both a `geometry ... end` block and a final `task dft` directive. |
| `INP.common.no_binary_contents` | fatal | satisfied | No database, wavefunction, checkpoint, or other runtime-generated/binary file contents are invented. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The decks use valid NWChem constructs: `echo`, `title`, `geometry units angstrom`, `basis`, `* library 6-31G*`, `dft`, `xc b3lyp`, `grid medium`, and `task dft`. |
| `INP.common.no_output_as_input` | major | satisfied | The answer writes only `.nw` input decks and does not provide contents for `.out`, `.log`, `.db`, `.movecs`, or other runtime outputs. |
| `INP.common.no_truncation` | major | satisfied | All ten input decks are fully written with no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | Although each deck has H–O distances approximately equal to its stated sweep value, the supplied second-H coordinates correspond to an H–O–H angle of about 105.1°, not the required fixed 104.5°; for example at 0.90 Å the required H2 coordinates are approximately `-0.225342 0.871333 0.000000`, rather than `-0.234145 0.869331 0.000000`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides ten `.nw` decks, one under each required `run_01` through `run_10` subdirectory. |
| `INP.common.exact_filenames_used` | major | not_applicable | NWChem input decks are command-line-selected `.nw` files; the format contract does not specify a fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | Each file uses recognizable NWChem constructs including `start`, `geometry`, `basis`, `dft`, and `task`. |
| `INP.common.mandatory_sections_present` | major | satisfied | Every deck contains both a `geometry ... end` block and a final `task dft energy` directive. |
| `INP.common.no_binary_contents` | fatal | satisfied | No database, wavefunction, checkpoint, or other runtime-generated binary content is fabricated. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The decks use valid NWChem directives and blocks: `title`, `start`, `geometry`, `symmetry`, `basis`, `dft`, `xc`, `mult`, `convergence`, `grid`, and `task dft energy`. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `.nw` input files and does not provide contents for `.out`, `.log`, `.db`, or `.movecs` runtime outputs. |
| `INP.common.no_truncation` | major | satisfied | All ten input decks are fully written with no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** ⚠︎ flipped across runs | Although the O-H distances are approximately the stated sweep values, the symmetric H coordinates use an H-O-H angle of about 104.0 degrees (e.g. run_01 has H vectors ±(0.7092,0.5540,0), whose dot product gives cos(angle)≈-0.242), not the required fixed 104.5 degrees. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides ten `.nw` inputs at `run_01/water.nw` through `run_10/water.nw`, satisfying the required NWChem input extension and requested sweep layout. |
| `INP.common.exact_filenames_used` | major | not_applicable | NWChem inputs are selected by the invocation and the catalog specifies no fixed required filename. |
| `INP.common.file_identifiable` | major | satisfied | The files clearly use NWChem-style directives including `start H2O`, `geometry`, `basis`, `charge`, and `task`. |
| `INP.common.mandatory_sections_present` | major | satisfied | Every supplied deck contains both a `geometry ... end` block and a `task dft single-point` directive, the format's genuinely mandatory sections. |
| `INP.common.no_binary_contents` | fatal | satisfied | No database, wavefunction, restart, or other runtime-generated/binary file contents are supplied. |
| `INP.common.no_invented_keywords` | fatal | **violated** | `b3lyp` is not a standalone NWChem input directive; B3LYP must be selected within a `dft` block (for example, `dft` / `xc b3lyp` / `end`). Also, the standard single-point task form is `task dft energy`, not `task dft single-point`. |
| `INP.common.no_output_as_input` | major | satisfied | The answer writes only `.nw` files and does not author any listed runtime outputs such as `.out`, `.log`, `.db`, or `.movecs`. |
| `INP.common.no_truncation` | major | satisfied | All ten run-specific input decks are written in full without ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | The coordinates place the two hydrogens on perpendicular axes, e.g. `H 0.91 0. 0.` and `H 0. 0. 0.9`, giving a 90-degree H-O-H angle rather than the required 104.5 degrees; for runs 02–10 one O-H bond also remains fixed at 0.90 Å. |
