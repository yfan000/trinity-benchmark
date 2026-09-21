# Verdicts — gromacs@sirius, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `5e044ce413ea`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer authors `.mdp`, `.gro`, and `.top` sources and gives `gmx grompp ... -o prod.tpr`, which produces the catalog-required `.tpr` without attempting to author it. |
| `INP.common.exact_filenames_used` | major | not_applicable | GROMACS input filenames are command-line arguments and the format contract sets `fixed_filenames: false`. |
| `INP.common.file_identifiable` | major | satisfied | `production.mdp` contains recognizable GROMACS keys such as `integrator`, `nsteps`, `coulombtype`, and `vdwtype`, while `topol.top` has `[ system ]` and `[ molecules ]`. |
| `INP.common.mandatory_sections_present` | major | **violated** | `system.gro` declares `34000` atoms but supplies only a small subset of coordinate records plus literal omission lines, so it is not a parseable complete GRO coordinate section. |
| `INP.common.no_binary_contents` | fatal | satisfied | No `.tpr` contents are fabricated; it is only designated as the output of the supplied `gmx grompp` command. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The MDP directives used, including `compressed_x_precision`, `fourierspacing`, `refcoord_scaling`, and `constraint_algorithm`, are real GROMACS MDP options. |
| `INP.common.no_output_as_input` | major | satisfied | The answer does not write contents for runtime outputs such as `md.log`, `md.edr`, trajectories, checkpoints, or runtime `md.gro`. |
| `INP.common.no_truncation` | major | **violated** | The purported `system.gro` explicitly contains `... (protein atoms 11–1960 omitted for brevity) ...` and `... (water atoms 10006–33977 omitted for brevity) ...`. |
| `INP.common.values_match_physical_system` | major | **violated** | The stated 7.842 nm cubic box has about 482 nm^3 volume, for which 20 NaCl pairs correspond to roughly 0.069 M rather than the required 0.15 M; the shown coordinate/topology atom numbering and counts are also internally inconsistent. |
| `INP.gromacs.grompp_step_stated` | major | satisfied | It gives `gmx grompp -f production.mdp -c system.gro -p topol.top -o prod.tpr -maxwarn 1`. |
| `INP.gromacs.mdp_keys_real` | fatal | satisfied | All supplied MDP keys are valid GROMACS options; no invented input-language keywords are present. |
| `INP.gromacs.required_mdp_fields` | major | satisfied | `production.mdp` sets `integrator = md`, `nsteps = 2500000`, `coulombtype = PME`, and `vdwtype = Cut-off`. |
| `INP.gromacs.tpr_not_authored` | fatal | satisfied | The answer explicitly says the binary run input is produced by `gmx grompp` and provides no textual `.tpr` content. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The three requested source files are supplied and the stated `gmx grompp ... -o production.tpr` command constructs the catalog-required `.tpr`. |
| `INP.common.exact_filenames_used` | major | not_applicable | GROMACS accepts `.mdp`, `.gro`, and `.top` filenames as arguments to `gmx grompp`; its format contract sets `fixed_filenames: false`. |
| `INP.common.file_identifiable` | major | satisfied | The answer provides recognizable GROMACS `.mdp` directives and a topology with `[ system ]` and `[ molecules ]`, as well as intended GRO coordinate content. |
| `INP.common.mandatory_sections_present` | major | **violated** | The `.gro` text is not a valid complete GRO structure: after its title/count interpretation, `Lysozyme solvated system` occurs where the first coordinate record must be, and the coordinate records are omitted. |
| `INP.common.no_binary_contents` | fatal | satisfied | The answer does not provide textual contents for the binary `.tpr`; it only gives a command to generate it. |
| `INP.common.no_invented_keywords` | fatal | **violated** ⚠︎ flipped across runs | The MDP uses `vdw-type`, but the real GROMACS MDP option is `vdwtype` (without a hyphen); `vdw-type` is not a valid MDP keyword. |
| `INP.common.no_output_as_input` | major | satisfied | No runtime output such as `md.log`, `md.edr`, trajectories, checkpoints, or final runtime GRO output is authored as an input file. |
| `INP.common.no_truncation` | major | **violated** | The GRO block explicitly contains `... [33,990 lines of coordinates omitted for brevity] ...`, so the required coordinate file is truncated. |
| `INP.common.values_match_physical_system` | major | **violated** | With a 6.5 nm cubic box, 45 NaCl pairs corresponds to about 0.27 M rather than the requested 0.15 M; 10,500 waters would instead imply roughly 28–29 NaCl pairs for 0.15 M. |
| `INP.gromacs.grompp_step_stated` | major | satisfied | The answer states `gmx grompp -f production.mdp -c system.gro -p topol.top -o production.tpr`. |
| `INP.gromacs.mdp_keys_real` | fatal | **violated** ⚠︎ flipped across runs | `vdw-type` is not a real GROMACS MDP key; the supported key is `vdwtype`. |
| `INP.gromacs.required_mdp_fields` | major | **violated** ⚠︎ flipped across runs | Although `integrator`, `nsteps`, and `coulombtype` are present, the required valid `vdwtype` field is absent; the answer instead writes invalid `vdw-type`. |
| `INP.gromacs.tpr_not_authored` | fatal | satisfied | `production.tpr` is not written as text; the answer says it is produced by `gmx grompp`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer authors `.mdp`, `.gro`, and `.top` and provides `gmx grompp ... -o prod.tpr`, which produces the catalog-required `.tpr` without attempting to author it. |
| `INP.common.exact_filenames_used` | major | not_applicable | GROMACS input filenames are selected through `gmx grompp` command-line arguments and the format contract sets `fixed_filenames: false`. |
| `INP.common.file_identifiable` | major | satisfied | The files contain recognizable GROMACS syntax and markers, including `integrator`, `nsteps`, `coulombtype`, `[ system ]`, and `[ molecules ]`. |
| `INP.common.mandatory_sections_present` | major | **violated** | `conf.gro` is not a complete coordinate file matching its declared atom count, and `topol.top` lists `Protein 1` without including or defining a Protein molecule topology. |
| `INP.common.no_binary_contents` | fatal | satisfied | The answer does not write `.tpr` contents and explicitly states that `gmx grompp` generates `prod.tpr`. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The `.mdp` keys used, including `cutoff-scheme`, `coulombtype`, `vdwtype`, `tcoupl`, `pcoupl`, and LINCS controls, are GROMACS options. |
| `INP.common.no_output_as_input` | major | satisfied | No runtime output such as `md.log`, `md.edr`, trajectory, checkpoint, or final `.gro` output is authored as an input file. |
| `INP.common.no_truncation` | major | **violated** | The purported `conf.gro` contains explicit placeholders such as `... (remaining protein atoms) ...` and therefore is not written out complete. |
| `INP.common.values_match_physical_system` | major | **violated** | The topology specifies 15,000 three-site waters (45,000 water atoms alone) plus protein and 440 ions, contradicting the stated approximately 34,000-atom system and the `conf.gro` header of 34,000 atoms. |
| `INP.gromacs.grompp_step_stated` | major | satisfied | It provides `gmx grompp -f md.mdp -c conf.gro -p topol.top -o prod.tpr -maxwarn 1`. |
| `INP.gromacs.mdp_keys_real` | fatal | satisfied | All parameter names in the supplied `.mdp` are real GROMACS MDP options. |
| `INP.gromacs.required_mdp_fields` | major | satisfied | The `.mdp` explicitly sets `integrator = md`, `nsteps = 2500000`, `coulombtype = PME`, and `vdwtype = Cut-off`. |
| `INP.gromacs.tpr_not_authored` | fatal | satisfied | No `.tpr` text is supplied; the answer says the three source files are compiled into `prod.tpr` by `gmx grompp`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer supplies `.mdp`, `.gro`, and `.top` source files and states `gmx grompp -f md.mdp -c conf.gro -p topol.top -o system.tpr`, which produces the catalog-required `.tpr`. |
| `INP.common.exact_filenames_used` | major | not_applicable | GROMACS source filenames are command-line arguments to `gmx grompp`, and the format contract sets `fixed_filenames: false`. |
| `INP.common.file_identifiable` | major | satisfied ⚠︎ flipped across runs | The answer contains recognisable GROMACS MDP directives (`integrator`, `nsteps`, `coulombtype`) and topology sections (`[ system ]`, `[ molecules ]`). |
| `INP.common.mandatory_sections_present` | major | **violated** | `conf.gro` lacks the required title line and declares `34 000` atoms while providing only six coordinate records; the supplied ITPs also define `[ moleculetype ]` without a required `[ atoms ]` section. |
| `INP.common.no_binary_contents` | fatal | satisfied | The `.tpr` is not written as text; it is only named as the output of the grompp command. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The MDP directives used, including `integrator`, `dt`, `nsteps`, `coulombtype`, `tcoupl`, and `pcoupl`, are GROMACS MDP options; the topology section/directive names are also GROMACS syntax. |
| `INP.common.no_output_as_input` | major | satisfied | No contents are authored for runtime outputs such as `md.log`, `md.edr`, trajectories, checkpoints, or the runtime `md.gro`. |
| `INP.common.no_truncation` | major | **violated** | The GRO file explicitly purports to describe `34 000` atoms but supplies only six coordinate lines, so the required coordinate input is incomplete. |
| `INP.common.values_match_physical_system` | major | **violated** | `nsteps = 50000000` with `dt = 0.002` ps is 100 ns, not the requested 5 ns; additionally, `[ molecules ]` lists only `SOL 2` and `LYZ 1`, with no Na+ or Cl- and no counts compatible with ~34,000 atoms. |
| `INP.gromacs.grompp_step_stated` | major | satisfied | It states `gmx grompp -f md.mdp -c conf.gro -p topol.top -o system.tpr`. |
| `INP.gromacs.mdp_keys_real` | fatal | satisfied | The MDP uses real GROMACS run-control, nonbonded, coupling, and output options; underscore spellings such as `vdw_type` are accepted GROMACS forms. |
| `INP.gromacs.required_mdp_fields` | major | satisfied ⚠︎ flipped across runs | The MDP sets `integrator = md-vv`, `nsteps = 50000000`, `coulombtype = PME`, and `vdw_type = Cut-off`. |
| `INP.gromacs.tpr_not_authored` | fatal | satisfied | The answer does not provide a fenced `.tpr` content block and says `gmx grompp` generates `system.tpr`. |
