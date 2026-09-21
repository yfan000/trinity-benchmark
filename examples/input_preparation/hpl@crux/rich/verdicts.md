# Verdicts — hpl@crux, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `59db62c64621`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the sole catalog-required input file under the exact filename "HPL.dat". |
| `INP.common.exact_filenames_used` | major | satisfied | The answer labels the fixed-name input exactly "HPL.dat". |
| `INP.common.file_identifiable` | major | satisfied | The contents include both HPL identification markers, including "HPLinpack benchmark input file" and "HPL.out". |
| `INP.common.mandatory_sections_present` | major | satisfied | The deck contains the required HPL sections/labels: "HPLinpack benchmark input file", "Ns", "NBs", "Ps", and "Qs". |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, checkpoint, or other runtime-generated file contents are supplied. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The answer uses the standard positional HPL.dat fields and comments shown by the supplied HPL format example, without introducing unsupported directives. |
| `INP.common.no_output_as_input` | major | satisfied | Although "HPL.out" is referenced as the HPL output filename within HPL.dat, the answer does not author separate contents for HPL.out or any log file. |
| `INP.common.no_truncation` | major | satisfied | The HPL.dat deck is written in full with no ellipses, TODOs, placeholders, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The deck specifies the requested "50000" Ns value, "232" NBs value, and a 2 by 2 process grid via "2 Ps" and "2 Qs". |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each declared count is 1 and is followed by exactly one corresponding value: 50000 for Ns, 232 for NBs, and one P/Q pair of 2 and 2 for the single grid. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The stated 2x2 grid is represented by P=2 and Q=2, yielding four MPI ranks for the requested process grid. |
| `INP.hpl.header_and_output_lines` | fatal | satisfied | It begins with "HPLinpack benchmark input file" and includes "HPL.out      output file name (if any)" plus "6            device out". |
| `INP.hpl.positional_format` | fatal | satisfied | The deck is line-ordered with numeric values followed by descriptive labels, not KEYWORD=value or KEYWORD:value assignments. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the sole required catalog input file under the exact filename "HPL.dat". |
| `INP.common.exact_filenames_used` | major | satisfied | The answer names the fixed-name input exactly "HPL.dat". |
| `INP.common.file_identifiable` | major | satisfied | The file begins with "HPLinpack benchmark input file" and includes the standard HPL output marker "HPL.out". |
| `INP.common.mandatory_sections_present` | major | satisfied | HPL.dat includes the required HPLinpack header and the Ns, NBs, Ps, and Qs labeled fields. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, checkpoint, runtime-generated, or output file contents are authored. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The deck uses standard positional HPL.dat fields and valid HPL option labels/comments, without invented directives. |
| `INP.common.no_output_as_input` | major | satisfied | It does not provide a separate fenced content block for HPL.out or any log; "HPL.out" appears only as the required output-name field within HPL.dat. |
| `INP.common.no_truncation` | major | satisfied | The supplied HPL.dat is complete and contains no ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The stated workload values are represented exactly: N=50000, NB=232, and a 2 by 2 process grid. |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each declared count is 1 and is followed by exactly one corresponding value: 50000 for Ns, 232 for NBs, and one P/Q grid pair of 2 and 2. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The requested 2x2 process grid contains 2*2=4 MPI ranks, consistent with the workload's specified process grid. |
| `INP.hpl.header_and_output_lines` | fatal | satisfied | The first line is "HPLinpack benchmark input file", followed by "HPL.out" and the device-out line "6". |
| `INP.hpl.positional_format` | fatal | satisfied | All HPL values are supplied in HPL's line-ordered positional format; no KEYWORD=value or KEYWORD:value assignments are used. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the sole catalog-required input file under the exact filename "HPL.dat". |
| `INP.common.exact_filenames_used` | major | satisfied | The answer labels the input file exactly "HPL.dat", which is the fixed filename required by HPL. |
| `INP.common.file_identifiable` | major | satisfied | The file begins with "HPLinpack benchmark input file" and includes the standard "HPL.out" output-name line. |
| `INP.common.mandatory_sections_present` | major | satisfied | HPL.dat contains the required positional HPL fields, including HPLinpack, Ns, NBs, Ps, and Qs. |
| `INP.common.no_binary_contents` | fatal | satisfied | The answer writes only the textual HPL.dat configuration and does not invent binary or runtime-generated file contents. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The deck uses standard positional HPL fields and algorithm-option labels such as PFACTs, NBMINs, BCASTs, DEPTHs, and RFACTs. |
| `INP.common.no_output_as_input` | major | satisfied | HPL.out is referenced only as the output filename within HPL.dat; no separate contents for HPL.out or logs are authored. |
| `INP.common.no_truncation` | major | satisfied | The HPL.dat deck is fully written without ellipses, placeholders, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The declared workload values match the prompt: N=50000, NB=232, and a 2 by 2 process grid. |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each relevant count is 1 and is followed by exactly one corresponding value: 50000 for Ns, 232 for NBs, and Ps/Qs values 2/2 for one grid. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The specified 2 by 2 process grid uses 2*2=4 MPI ranks, consistent with the implied rank count of the requested grid. |
| `INP.hpl.header_and_output_lines` | fatal | satisfied | The first line is "HPLinpack benchmark input file", followed by "HPL.out" and the device-out line "6". |
| `INP.hpl.positional_format` | fatal | satisfied | HPL.dat is presented in HPL's required line-ordered positional format rather than KEYWORD=value syntax. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The response provides a file explicitly named "HPL.dat", which is the sole catalog-required input. |
| `INP.common.exact_filenames_used` | major | satisfied | The response includes the fixed filename "HPL.dat" required by HPL. |
| `INP.common.file_identifiable` | major | satisfied | The emitted content contains the HPL identification marker "HPLinpack benchmark input file" and the "HPL.out" output-name line. |
| `INP.common.mandatory_sections_present` | major | satisfied | Each emitted deck includes the required HPL labels/sections: "HPLinpack", "Ns", "NBs", "Ps", and "Qs". |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, checkpoint, or other runtime-generated file contents are authored. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The HPL parameter labels and positional fields used are standard HPL.dat fields rather than invented directives. |
| `INP.common.no_output_as_input` | major | satisfied | It does not author an HPL.out or .log file; "HPL.out" appears only as the output filename setting within HPL.dat. |
| `INP.common.no_truncation` | major | satisfied | The decks are written without ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The provided HPL.dat specifies the stated workload values: N=50000, NB=232, P=2, and Q=2. |
| `INP.hpl.count_lines_match` | fatal | satisfied | Each deck declares one problem size, one NB, and one process grid, followed by exactly one corresponding value for each. |
| `INP.hpl.grid_matches_ranks` | major | satisfied | The stated 2x2 process grid has P×Q=2×2=4 MPI ranks, consistent with the workload's specified process grid. |
| `INP.hpl.header_and_output_lines` | fatal | **violated** | HPL.dat does not begin with "HPLinpack benchmark input file"; its first line is "# HPLinpack benchmark input file". |
| `INP.hpl.positional_format` | fatal | **violated** ⚠︎ flipped across runs | The HPL.dat code content starts with three added comment lines before the positional HPL title; this shifts every required positional field so HPL would not read the title/output/device lines in their required positions. |
