# Verdicts — hpl@crux, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `59db62c64621`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the sole catalog-required input file under the name "HPL.dat". |
| `INP.common.exact_filenames_used` | major | satisfied | The fixed filename required by HPL is given exactly as "HPL.dat". |
| `INP.common.file_identifiable` | major | satisfied | The file begins with "HPLinpack benchmark input file" and contains the standard HPL output line "HPL.out      output file name (if any)". |
| `INP.common.mandatory_sections_present` | major | satisfied | HPL.dat includes the required HPL title and the Ns, NBs, Ps, and Qs positional sections. |
| `INP.common.no_binary_contents` | fatal | satisfied | The answer writes only the textual HPL.dat control deck and does not invent contents for binary or runtime-generated files. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The deck uses standard positional HPL.dat fields and labels such as PFACTs, RFACTs, BCASTs, DEPTHs, and SWAP. |
| `INP.common.no_output_as_input` | major | satisfied | No separate contents are authored for HPL.out or any log file; HPL.out appears only as HPL.dat's runtime output filename setting. |
| `INP.common.no_truncation` | major | satisfied | The HPL.dat deck is complete and contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The declared workload values match the prompt: one N of 50000, one NB of 232, and a 2 by 2 process grid. |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each relevant count is 1 and is followed by exactly one corresponding value: 50000, 232, and the single P/Q grid pair 2 and 2. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The requested 2x2 process grid has P×Q=4 MPI ranks, consistent with the stated grid. |
| `INP.hpl.header_and_output_lines` | fatal | satisfied | The first line is "HPLinpack benchmark input file" and the deck includes both the HPL.out output-file and device-out (6) lines. |
| `INP.hpl.positional_format` | fatal | satisfied | Parameters are supplied in HPL's required line-ordered count/value format rather than as KEYWORD=value pairs. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the sole required catalog input file under the exact name "HPL.dat". |
| `INP.common.exact_filenames_used` | major | satisfied | The response labels the supplied fixed-name input file exactly "HPL.dat". |
| `INP.common.file_identifiable` | major | satisfied | The first deck line is "HPLinpack benchmark input file", identifying it as HPL input. |
| `INP.common.mandatory_sections_present` | major | satisfied | The deck includes the required HPL positional labels and sections, including "Ns", "NBs", "Ps", and "Qs". |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, checkpoint, log, or other runtime-generated file contents are authored. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The response uses the standard positional HPL.dat fields and valid accompanying labels such as "PFACTs", "BCASTs", and "DEPTHs". |
| `INP.common.no_output_as_input` | major | satisfied | It does not provide contents for HPL.out or any log file; "HPL.out" appears only as the required output-name field within HPL.dat. |
| `INP.common.no_truncation` | major | satisfied | The HPL.dat content is fully written with no ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The requested workload values are correctly represented: "50000        Ns", "232          NBs", "2            Ps", and "2            Qs". |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each declared count is 1 and is followed by exactly one corresponding value: 50000 for Ns, 232 for NBs, and 2/2 for the single P-by-Q grid. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The specified process grid is "2 Ps" by "2 Qs", giving 4 MPI ranks, consistent with the stated 2x2 process grid. |
| `INP.hpl.header_and_output_lines` | fatal | satisfied | It begins with "HPLinpack benchmark input file" and includes both "HPL.out      output file name (if any)" and the device-out line. |
| `INP.hpl.positional_format` | fatal | satisfied | The deck is written in HPL's required line-ordered positional format rather than using keyword-value assignments. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the sole catalog-required input file under the exact filename `HPL.dat`. |
| `INP.common.exact_filenames_used` | major | satisfied | The answer labels the fixed-name HPL input exactly as `HPL.dat`. |
| `INP.common.file_identifiable` | major | satisfied | The file begins with `HPLinpack benchmark input file` and includes the standard `HPL.out` output-file line. |
| `INP.common.mandatory_sections_present` | major | satisfied ⚠︎ flipped across runs | `HPL.dat` includes the required HPL title and positional `Ns`, `NBs`, `Ps`, and `Qs` sections. |
| `INP.common.no_binary_contents` | fatal | satisfied | The answer authors only the text HPL.dat input and does not invent contents for binary or runtime-generated files. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The deck uses HPL's standard positional input layout and standard HPL labels/comments such as `PFACTs`, `RFACTs`, `BCASTs`, and `DEPTHs`. |
| `INP.common.no_output_as_input` | major | satisfied | `HPL.out` is only named within HPL.dat as HPL's runtime output target; no contents are authored for `HPL.out` or any log file. |
| `INP.common.no_truncation` | major | satisfied | The supplied HPL.dat is complete and contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The declared workload values match the prompt: `50000 Ns`, `232 NBs`, `2 Ps`, and `2 Qs`; remaining tuning values are not fixed by the prompt. |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each declared count is 1 and is followed by exactly one corresponding N value, NB value, and P/Q grid pair. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The file declares `2 Ps` and `2 Qs`, producing the stated 2x2 process grid (four MPI ranks), and no conflicting rank count is given. |
| `INP.hpl.header_and_output_lines` | fatal | satisfied | The first content line is exactly `HPLinpack benchmark input file`, followed by `HPL.out      output file name (if any)` and the device-out line. |
| `INP.hpl.positional_format` | fatal | satisfied ⚠︎ flipped across runs | All HPL parameters are supplied as values followed by descriptive labels, not as `KEYWORD=value` or `KEYWORD: value` pairs. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides a file headed "### HPL.dat", which is the sole catalog-required input. |
| `INP.common.exact_filenames_used` | major | satisfied | The required fixed filename is used exactly as "HPL.dat". |
| `INP.common.file_identifiable` | major | satisfied | The proposed HPL.dat contains the identifying strings "HPLinpack benchmark input file" and "HPL.out". |
| `INP.common.mandatory_sections_present` | major | satisfied | The HPL.dat content includes the required HPL labels/sections: "HPLinpack", "Ns", "NBs", "Ps", and "Qs". |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary or runtime-generated file contents are invented; the runtime outputs are only listed as produced at runtime. |
| `INP.common.no_invented_keywords` | fatal | **violated** ⚠︎ flipped across runs | The answer invents unsupported purported input files and formats such as "system.topology", "system.resources", and "system.architecture"; HPL opens only HPL.dat and has no such input language. |
| `INP.common.no_output_as_input` | major | satisfied | "HPL.out" and "*.log" are explicitly marked "*produced at runtime*" and no file contents are supplied for them. |
| `INP.common.no_truncation` | major | satisfied | The authored HPL.dat and the additional text files are written without ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | Within HPL.dat, the specified workload values are correctly represented as N=50000, NB=232, and P=Q=2, with no direct contradiction of the stated CPU-only Crux workload. |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each declared count is 1 and is followed by exactly one corresponding value: 50000 for Ns, 232 for NBs, and one P/Q grid pair of 2 and 2. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The declared 2 by 2 process grid corresponds to 4 MPI ranks, as implied by the stated 2x2 grid. |
| `INP.hpl.header_and_output_lines` | fatal | **violated** | The first HPL.dat content line is "# HPLinpack benchmark input file", rather than beginning exactly with "HPLinpack benchmark input file" as required; the output-file and device lines are otherwise present. |
| `INP.hpl.positional_format` | fatal | satisfied ⚠︎ flipped across runs | The HPL.dat parameters use HPL's positional value-then-label layout and do not use prohibited KEYWORD=value or KEYWORD:value syntax. |
