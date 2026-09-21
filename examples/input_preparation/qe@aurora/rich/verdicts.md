# Verdicts — qe@aurora, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `7c0545914355`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The requested input file `3csic_64atom.scf.in` is provided in full. |
| `INP.common.exact_filenames_used` | major | not_applicable | Quantum ESPRESSO `pw.x` reads an input filename supplied with `-in`; this format has no fixed mandatory filename. |
| `INP.common.file_identifiable` | major | satisfied | The QE PW input markers `&CONTROL`, `&SYSTEM`, `&ELECTRONS`, and `ATOMIC_SPECIES` are present, with case-insensitive Fortran/QE formatting. |
| `INP.common.mandatory_sections_present` | major | satisfied | The file contains `&control`, `&system`, `&electrons`, `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`, and `K_POINTS`. |
| `INP.common.no_binary_contents` | fatal | satisfied | The answer does not invent contents for UPF files, wavefunctions, XML, save directories, or other runtime-generated/binary files. |
| `INP.common.no_invented_keywords` | fatal | satisfied | `calculation`, `prefix`, `outdir`, `pseudo_dir`, `tstress`, `tprnfor`, `verbosity`, `ibrav`, `celldm`, cutoffs, occupations, smearing, and electronic settings are valid pw.x input keywords. |
| `INP.common.no_output_as_input` | major | satisfied | Only the requested `.scf.in` input is authored; no `.out`, `.xml`, or `.save` runtime output is written. |
| `INP.common.no_truncation` | major | satisfied | The deck is fully enumerated with no ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | Although `nat=64` and the listed coordinates target a cubic 2x2x2 conventional supercell, `ibrav=2` makes QE use an FCC primitive cell of volume a^3/4 rather than the required cubic supercell of volume a^3; many listed sites are therefore periodic duplicates and the actual periodic structure is not the stated 64-atom supercell. |
| `INP.qe.ibrav_consistent` | major | **violated** | `ibrav = 2` defines an FCC primitive lattice, whereas the explicitly listed coordinates and `celldm(1)=16.48` describe a cubic supercell edge; a 2x2x2 conventional cubic supercell should use, for example, `ibrav=1` with that edge or `ibrav=0` plus cubic `CELL_PARAMETERS`. |
| `INP.qe.namelist_syntax` | fatal | satisfied | All namelist assignments use literal numeric, logical, or quoted-string values; no arithmetic expressions are used. |
| `INP.qe.nat_matches_positions` | fatal | satisfied | `nat = 64` is declared and there are 64 coordinate lines: 32 Si plus 32 C. |
| `INP.qe.no_card_terminator` | major | satisfied | No `/` card terminator appears after `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`, or `K_POINTS`; slashes are used only to close namelists. |
| `INP.qe.ntyp_matches_species` | fatal | satisfied | `ntyp = 2` is declared and `ATOMIC_SPECIES` contains exactly the two entries Si and C. |
| `INP.qe.pseudopotentials_plausible` | major | satisfied ⚠︎ flipped across runs | The Si and C entries reference element-matched PBE ultrasoft UPF pseudopotentials (`Si.pbe-us.UPF` and `C.pbe-us.UPF`). |
| `INP.qe.required_cards` | fatal | satisfied | The input contains `ATOMIC_SPECIES`, `ATOMIC_POSITIONS (alat)`, and `K_POINTS automatic` cards. |
| `INP.qe.required_namelists` | fatal | satisfied | `&control`, `&system`, and `&electrons` are each present and each ends with `/`. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | **violated** ⚠︎ flipped across runs | The catalog lists .scf.in, .relax.in, .bands.in, and .pw.in as required input types, but the answer provides only 3csic_64atom.scf.in. |
| `INP.common.exact_filenames_used` | major | not_applicable | pw.x reads an input filename supplied with -in and has no fixed mandatory input filename. |
| `INP.common.file_identifiable` | major | satisfied | The file contains the Quantum ESPRESSO pw.x markers '&control', '&system', '&electrons', and 'ATOMIC_SPECIES'. |
| `INP.common.mandatory_sections_present` | major | satisfied | The submitted input contains &control, &system, &electrons, ATOMIC_SPECIES, ATOMIC_POSITIONS, and K_POINTS sections. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, pseudopotential, restart, wavefunction, XML, or save-directory contents are fabricated. |
| `INP.common.no_invented_keywords` | fatal | satisfied | calculation, outdir, pseudo_dir, ibrav, celldm(1), nat, ntyp, ecutwfc, ecutrho, and conv_thr are valid pw.x input keywords. |
| `INP.common.no_output_as_input` | major | satisfied | The answer writes only an input deck and does not author output.*, XML, or .save runtime output contents. |
| `INP.common.no_truncation` | major | satisfied | The input deck is fully enumerated without ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | Although nat=64 and the cutoffs/k-grid match the request, celldm(1)=10.26 bohr with ibrav=2 describes an approximately 5.43 Å primitive fcc cell rather than a 2x2x2 conventional 3C-SiC supercell (edge approximately 8.716 Å); the listed coordinates therefore do not define the requested periodic supercell. |
| `INP.qe.ibrav_consistent` | major | **violated** | ibrav=2 fixes the cell to a single fcc primitive cell, while the positions extend over a 2x2x2 conventional-cell region; no explicit supercell CELL_PARAMETERS card is supplied, so the periodic cell is inconsistent with the intended 64-atom supercell. |
| `INP.qe.namelist_syntax` | fatal | satisfied | All namelist assignments use Fortran literals, including 1.0d-8, with no arithmetic expressions. |
| `INP.qe.nat_matches_positions` | fatal | satisfied | The deck declares nat=64 and provides 64 ATOMIC_POSITIONS entries. |
| `INP.qe.no_card_terminator` | major | satisfied | No '/' card terminator appears after ATOMIC_SPECIES, ATOMIC_POSITIONS, or K_POINTS. |
| `INP.qe.ntyp_matches_species` | fatal | satisfied | The deck declares ntyp=2 and provides exactly two ATOMIC_SPECIES entries, Si and C. |
| `INP.qe.pseudopotentials_plausible` | major | **violated** | The generic filenames 'Si.pbe-n-uspp.UPF' and 'C.pbe-n-uspp.UPF' are not established QE PBE ultrasoft pseudopotential filenames; a known family such as Si.pbe-n-rrkjus_psl.1.0.0.UPF and C.pbe-n-rrkjus_psl.1.0.0.UPF should be referenced. |
| `INP.qe.required_cards` | fatal | satisfied | ATOMIC_SPECIES, ATOMIC_POSITIONS (alat), and K_POINTS cards are all present. |
| `INP.qe.required_namelists` | fatal | satisfied | &control, &system, and &electrons are each present and each is terminated by '/'. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The requested SCF input file is provided with the required filename `3csic_64atom.scf.in`. |
| `INP.common.exact_filenames_used` | major | not_applicable | pw.x accepts an input filename supplied with `-in`; its input format does not require a fixed filename. |
| `INP.common.file_identifiable` | major | satisfied | The content is recognisable as a Quantum ESPRESSO pw.x deck through `&control`, `&system`, `&electrons`, `ATOMIC_SPECIES`, and `ATOMIC_POSITIONS`. |
| `INP.common.mandatory_sections_present` | major | **violated** | The file contains the three namelists, ATOMIC_SPECIES, and ATOMIC_POSITIONS, but it never contains the required `K_POINTS` card. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary pseudopotential, wavefunction, restart, XML, or other runtime-generated file contents are invented. |
| `INP.common.no_invented_keywords` | fatal | satisfied | `calculation`, `prefix`, `pseudo_dir`, `outdir`, `tstress`, `tprnfor`, `verbosity`, `ibrav`, `celldm(1)`, `nat`, `ntyp`, `ecutwfc`, `ecutrho`, and `conv_thr` are valid pw.x input keywords. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only an input deck and does not provide contents for output, XML, save-directory, or other runtime-generated files. |
| `INP.common.no_truncation` | major | **violated** | The fenced input ends abruptly at the incomplete line `C  0`, without completing the 64 positions or the K_POINTS card. |
| `INP.common.values_match_physical_system` | major | **violated** | The specified 4x4x4 k-grid is absent, and the incomplete/duplicated ATOMIC_POSITIONS data do not describe a complete 64-atom 2x2x2 zinc-blende SiC supercell. |
| `INP.qe.ibrav_consistent` | major | **violated** | `ibrav = 2` with `celldm(1) = 8.2590` defines the primitive FCC cell at roughly the conventional SiC lattice constant, not a doubled 2x2x2 conventional supercell; the listed crystal coordinates also extend beyond 1 and include duplicates rather than consistently defining that supercell. |
| `INP.qe.namelist_syntax` | fatal | satisfied | All namelist assignments use literal numeric, logical, or quoted-string values; no arithmetic expression is used as a namelist value. |
| `INP.qe.nat_matches_positions` | fatal | **violated** | The deck declares `nat = 64`, but only 53 position records are started before the answer ends, with the final record malformed as `C  0`. |
| `INP.qe.no_card_terminator` | major | satisfied | No `/` card terminator is written after `ATOMIC_SPECIES` or `ATOMIC_POSITIONS`; slashes are used only to terminate namelists. |
| `INP.qe.ntyp_matches_species` | fatal | satisfied | `ntyp = 2` matches the two ATOMIC_SPECIES entries, `Si` and `C`. |
| `INP.qe.pseudopotentials_plausible` | major | satisfied | `Si.pbe-n-rrkjus.UPF` and `C.pbe-n-rrkjus.UPF` are plausible PBE RRKJUS ultrasoft pseudopotential names for Si and C. |
| `INP.qe.required_cards` | fatal | **violated** | `ATOMIC_SPECIES` and `ATOMIC_POSITIONS` are present, but there is no `K_POINTS` card. |
| `INP.qe.required_namelists` | fatal | satisfied | `&control`, `&system`, and `&electrons` are each present and each is terminated by `/`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | **violated** | Only `3csic_64atom.scf.in` is produced, while the catalog lists `.scf.in`, `.relax.in`, `.bands.in`, and `.pw.in` as required inputs. |
| `INP.common.exact_filenames_used` | major | not_applicable | pw.x accepts an input filename supplied with `-in` and has no fixed mandatory input filename. |
| `INP.common.file_identifiable` | major | satisfied | The file has recognizable Quantum ESPRESSO pw.x markers including `&CONTROL`, `&SYSTEM`, `&ELECTRONS`, and `ATOMIC_SPECIES`. |
| `INP.common.mandatory_sections_present` | major | satisfied | The produced file contains `&CONTROL`, `&SYSTEM`, `&ELECTRONS`, `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`, and `K_POINTS`. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, wavefunction, restart, XML, or other runtime-generated file contents are written. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The namelist keywords used, such as `calculation`, `restart_mode`, `ecutrho`, `input_dft`, `ecutfock`, and `diagonalization`, are Quantum ESPRESSO pw.x keywords. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only an input deck and does not provide contents for output, XML, or `.save` runtime products. |
| `INP.common.no_truncation` | major | **violated** | `pseudo_dir = '/path/to/pseudopotentials'` is an unresolved placeholder path. |
| `INP.common.values_match_physical_system` | major | **violated** | The deck declares `nat = 64` for a 64-atom 2x2x2 conventional supercell but supplies only 16 atomic positions; additionally, the `K_POINTS` card does not specify the required automatic 4x4x4 Monkhorst-Pack form. |
| `INP.qe.ibrav_consistent` | major | **violated** | `ibrav = 2` with `celldm(1) = 10.26` and the listed `(alat)` coordinates does not describe the requested 2x2x2 conventional 3C-SiC supercell; no explicit supercell cell vectors are supplied. |
| `INP.qe.namelist_syntax` | fatal | satisfied | All namelist assignments use literal numeric, logical, or quoted-string values; no arithmetic expression is used. |
| `INP.qe.nat_matches_positions` | fatal | **violated** | `nat = 64` is declared, but the `ATOMIC_POSITIONS` card contains only 8 Si lines and 8 C lines, for 16 positions total. |
| `INP.qe.no_card_terminator` | major | satisfied | No `/` terminator is placed after an atomic-position or other card. |
| `INP.qe.ntyp_matches_species` | fatal | satisfied | `ntyp = 2` matches the two `ATOMIC_SPECIES` entries, Si and C. |
| `INP.qe.pseudopotentials_plausible` | major | **violated** | `Si.uspp.UPF` and `C.uspp.UPF` are generic unsupported names that do not identify known PBE ultrasoft pseudopotentials, and the referenced pseudopotential directory is a placeholder. |
| `INP.qe.required_cards` | fatal | satisfied | The `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`, and `K_POINTS` cards are present. |
| `INP.qe.required_namelists` | fatal | satisfied | `&CONTROL`, `&SYSTEM`, and `&ELECTRONS` are all present and each is terminated by `/`. |
