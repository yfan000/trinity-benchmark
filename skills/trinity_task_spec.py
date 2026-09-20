"""Trinity agent benchmark — the four pre-submission subtasks.

These are the steps between "a scientist wants a result" and "a job is in the queue":

    Software selection -> Input preparation -> Resource selection -> PBS job creation

Each sample is self-contained: an agent receives one subtask and never sees the originating
conversation. The governing rule is that the prompt states the task explicitly but withholds
the answer being tested — `leak_terms` encodes what must not appear, and the generator
enforces it by regenerating anything that leaks.

Every sample is anchored to a real (system, application) pair from zhenghh04/application_catalog,
cached under results/skills/trinity/catalog/. That matters twice over: the workload can cite
true hardware and queue limits, and the grading key is drawn from the catalog's own YAML
rather than invented — the expected module lines, run command, input extensions, queue and
node defaults are facts, not opinions.
"""
from __future__ import annotations

_APP_NAMES = ["LAMMPS", "GROMACS", "NAMD", "OpenMM", "VASP", "Quantum ESPRESSO", "QE ",
              "CP2K", "NWChem", "PySCF", "GAMESS", "QMCPACK", "HACC", "FLASH", "Nek5000",
              "NekRS", "OpenFOAM", "AlphaFold", "ESMFold", "OpenFold", "Chai", "WRF",
              "MOOSE", "Megatron", "DeepSpeed"]
# --nproc_per_node is torchrun's --ppn: a Resource-selection prompt carrying
# "torchrun --nproc_per_node=8" states the ranks-per-node answer in launch syntax.
_RES = ["select=", "ncpus=", "ngpus=", "walltime=", "-l select", "--ppn", "mpiexec -n",
        "--nproc_per_node", "ntasks-per-node", "srun -n "]
_PBS = ["#PBS", "qsub ", "module load", "module swap", "PrgEnv-"]

LEAK_PATTERNS = [
    r"\buse (?:all )?\d+\s*(?:GPUs?|nodes?|ranks?|cores?)",
    r"\brequest(?:ing)? \d+\s*(?:GPUs?|nodes?|ranks?)",
    r"\bstandard practice[^.]{0,80}?\d+\s*(?:GPUs?|ranks?|nodes?)",
    # prescriptive only — "maximum walltime of 1 hour" is queue policy the agent needs
    r"\b(?:use|request|set|choose|specify)\s+(?:a\s+)?walltime of \d",
    r"\b\d+\s*(?:nodes?|GPUs?) for \d+\s*(?:hours?|minutes?)",
    r"\b\d+\s*ranks? per GPU",
    r"\brun (?:it |this )?(?:on|with) \d+\s*(?:GPUs?|nodes?)",
    # Prose that pre-decides the sizing without using any forbidden token. Token matching
    # missed these entirely: "the team has confirmed that a single node is sufficient" is
    # the answer, written in fluent English.
    r"\b(?:a |one )?single node is (?:sufficient|enough|adequate)",
    r"\bis (?:sufficient|enough) to (?:complete|run|finish|fit)",
    r"\bhas confirmed that\b",
    r"\bfits (?:on|in|within) (?:a|one) (?:single )?node",
    r"\bshould (?:use|target|request|select) the \w+ queue",
    r"\bthe \w+ queue is the (?:right|correct|appropriate|only) (?:choice|option)",
    # The charge account is withheld everywhere: recognising that one is required, and
    # supplying it, is part of what Batch job creation tests.
    r"\b(?:account|allocation|project code|charge account)\s*[:=]\s*\S+",
    r"\b(?:under|using) (?:project |account )?(?:account|allocation) [`\"']?\w+",
    r"-A\s+\w+",
]

SUBTASKS = {
    "Software selection": {
        # The catalog is SUPPLIED. The instruction said "consult the system's software
        # catalog" while no catalog was in the prompt and the models have no tools, so they
        # were guessing from memory and inventing module names to fill the gap. Supplying it
        # turns this into what it should be: match a workload to what is actually installed.
        "needs_software_list": True,
        "order": 1,
        "goal": "Choose, from the software installed on the target system, the application "
                "suited to a described scientific workload.",
        "instructions": ("Consult the system's software catalog and identify the installed "
                         "application best suited to this workload and architecture."),
        "output": "Return the selected application and briefly explain why it fits.",
        "leak_terms": _APP_NAMES,
        "withhold": "which application to use",
        "key_fields": ["app", "description", "gpu_support"],
    },
    "Input preparation": {
        "needs_physical_system": True,
        "order": 2,
        "goal": "Determine and construct the input files the chosen application requires.",
        # The file inventory is supplied (which artifacts the app consumes) but NOT the
        # content markers. Inventory is retrievable and the orchestrator can inject it; one
        # model never produced HACC's only required file. Grammar is the thing being tested
        # — a model that writes a confident, structurally invalid deck is exactly what must
        # not go in an unattended pipeline — so the markers stay withheld.
        "needs_input_spec": True,
        "instructions": ("Determine the parameters and configuration the application "
                         "requires for this workload, then write out each input file in "
                         "full. Do NOT write a job script or scheduler directives — input "
                         "files only."),
        # "Prepare the required input files" was unanswerable: the model reaches a chat API
        # with no filesystem, and the judge duly penalised 13 answers for not having written
        # anything to disk. What is actually being tested is whether it knows the right files
        # and the right contents, so the deliverable is the text of those files.
        "output": ("For each required file, give its filename and its complete contents in a "
                   "fenced code block, then one line on why each is needed. You are writing "
                   "file contents as text; you have no filesystem access and are not expected "
                   "to create anything on disk."),
        "leak_terms": _RES + _PBS,
        "withhold": "the exact file set and parameters",
        # input_detection.content_markers is the gradeable part: it says what must appear
        # *inside* each file, not merely which extensions to create.
        "key_fields": ["input_files", "required_inputs", "optional_inputs",
                       "input_detection", "output_patterns"],
    },
    "Resource selection": {
        "needs_physical_system": True,
        "needs_machine_spec": True,
        "order": 3,
        "goal": "Size the allocation — nodes, GPUs, ranks, walltime and queue.",
        "instructions": ("Using the workload, the application's scaling behaviour and the "
                         "system's queue policy, determine nodes, GPUs, ranks per node, "
                         "walltime and the queue to target. Do NOT write a job script or "
                         "scheduler directives — give the specification and the reasoning."),
        "output": "Provide the resource specification and the reasoning behind each choice.",
        # _PBS excluded on purpose: this subtask withholds numbers, not batch syntax.
        "leak_terms": _RES,
        "numeric_answer": True,
        "withhold": "the node/GPU/rank counts, walltime and queue",
        # There is no single right allocation. The catalog's `defaults` are a one-node
        # functional smoke test (LAMMPS: 1 node, 1800 s, queue debug) and were being treated
        # as the expected answer — 176 of 234 baseline answers carry a defect citing them,
        # so a model that sized correctly for a 500,000-atom run was marked down for not
        # matching a config meant to prove the binary starts.
        "grading_note": (
            "There is no single correct allocation for this subtask. Judge whether the "
            "choice is DEFENSIBLE for the physical system stated in the prompt and LEGAL "
            "under the queue limits given, and whether the reasoning is sound and free of "
            "invented facts.\n"
            "The catalog's `defaults` field is a one-node functional smoke test, NOT the "
            "expected answer for a production workload. Do NOT deduct for deviating from "
            "it; a larger allocation than the default is usually correct when the physical "
            "system is large. Only treat the defaults as informative for the rank-per-node "
            "and GPU-per-rank ratio, which is a property of the build.\n"
            "Judge the legality check on its substance, not its layout: if all three limits are "
        "compared and the verdicts are right, the form they are presented in — table, list "
        "or prose — is not a defect and must not be deducted for.\n"
        "DO deduct for: a request outside the stated queue's node or walltime limits, a "
            "queue that does not exist on that system, a rank/GPU layout inconsistent with "
            "the hardware, arithmetic that does not follow, or fabricated timing evidence."),
        "key_fields": ["defaults", "scaling_notes", "gpu_notes"],
    },
    "Batch job creation": {
        "needs_physical_system": True,
        "order": 4,
        "goal": "Write the submittable batch script for the target system's scheduler.",
        # Not "PBS job creation": the catalog spans ALCF (PBS Pro) and OLCF/NERSC (Slurm),
        # and knowing which scheduler a system runs is itself part of the capability. An
        # agent that emits #PBS on Frontier is wrong.
        # setup lines and run_command are supplied: "invented module / version" was 24.5%
        # of this subtask's defects and site facts (module use /soft/modulefiles,
        # -l filesystems=) another 9.5%. Neither is knowable without the catalog, and the
        # orchestrator has it. Assembling a correct script is still the work.
        "needs_app_setup": True,
        "instructions": ("Write a valid batch script for this system's scheduler that "
                         "requests the allocation, sets up the software environment using "
                         "the supplied module lines, and launches the application "
                         "correctly."),
        "output": "Return the complete batch script.",
        # The scheduler is now GIVEN, not withheld. Withholding it made this subtask
        # measure one recall fact: 87 of 117 answers failed purely by reaching for Slurm on
        # a PBS machine, which drowned out everything else about script quality. In
        # deployment the orchestrator knows the target machine and can state it. What stays
        # withheld is the script itself — directives, modules, launcher, resource mapping.
        "leak_terms": _PBS,
        "gives_scheduler": True,
        "withhold": ("the directive syntax, module lines, resource mapping and launch "
                     "command — the script itself"),
        # "porting from another facility" is excluded here: describing the source system's
        # scheduler inevitably names one of the two, which is half the answer.
        "skip_variations": ["porting from a different facility's system"],
        "key_fields": ["setup", "modules", "run_command", "binary"],
    },
}

# (domain, catalog app, system) — restricted to pairs SMOKE_TESTS.md confirms are actually
# installed and executable. The catalog lists software that is catalogued, which is not the
# same thing: on Polaris it records CP2K, Flash, HPL, OpenFOAM and WRF as "not present", and
# a Software-selection sample whose correct answer is missing software tests nothing useful.
#
# Both schedulers are represented on purpose — ALCF runs PBS Pro, OLCF and NERSC run Slurm —
# so Batch job creation tests whether the agent knows which one the target system uses.
ANCHORS = [
    ('Protein structure prediction (XPU)',       'chai_lab',       'aurora'),
    ('Quantum chemistry / AIMD',                 'cp2k',           'aurora'),
    ('Molecular dynamics (biomolecular)',        'gromacs',        'aurora'),
    ('Cosmology',                                'hacc',           'aurora'),
    ('Dense linear algebra',                     'hpl',            'aurora'),
    ('Molecular dynamics',                       'lammps',         'aurora'),
    ('Fluid dynamics (spectral element)',        'nek5000',        'aurora'),
    ('Computational fluid dynamics',             'nekrs',          'aurora'),
    ('Computational chemistry',                  'nwchem',         'aurora'),
    ('Molecular dynamics (biophysics)',          'openmm',         'aurora'),
    ('Electronic structure (DFT)',               'qe',             'aurora'),
    ('Quantum Monte Carlo',                      'qmcpack',        'aurora'),
    ('Dense linear algebra',                     'hpl',            'crux'),
    ('Molecular dynamics',                       'lammps',         'crux'),
    ('Electronic structure (DFT)',               'qe',             'crux'),
    ('Molecular dynamics (AMD GPU)',             'gromacs_hip',    'frontier'),
    ('Protein structure prediction (open)',      'openfold',       'frontier'),
    ('LLM inference serving',                    'vllm',           'frontier'),
    ('Protein structure prediction',             'alphafold',      'perlmutter'),
    ('Cosmology',                                'hacc',           'perlmutter'),
    ('Molecular dynamics (biophysics)',          'openmm',         'perlmutter'),
    ('Quantum Monte Carlo',                      'qmcpack',        'perlmutter'),
    ('LLM inference serving',                    'vllm',           'perlmutter'),
    ('Molecular dynamics (biomolecular)',        'gromacs',        'polaris'),
    ('Cosmology',                                'hacc',           'polaris'),
    ('Molecular dynamics',                       'lammps',         'polaris'),
    ('Nuclear / multiphysics',                   'moose',          'polaris'),
    ('Molecular dynamics (biomolecular)',        'namd',           'polaris'),
    ('Computational fluid dynamics',             'nekrs',          'polaris'),
    ('Computational chemistry',                  'nwchem',         'polaris'),
    ('Quantum Monte Carlo',                      'qmcpack',        'polaris'),
    ('LLM inference serving',                    'vllm',           'polaris'),
    ('Molecular dynamics (biomolecular)',        'gromacs',        'sirius'),
    ('Molecular dynamics',                       'lammps',         'sirius'),
    ('Electronic structure (DFT)',               'qe',             'sirius'),
    ('Quantum Monte Carlo',                      'qmcpack',        'sirius'),
    ('Distributed LLM training',                 'deepspeed',      'sophia'),
    ('Deep learning training',                   'pytorch',        'sophia'),
    ('Quantum Monte Carlo',                      'qmcpack',        'sophia'),
]
VARIATIONS = [
    "first run of this workload on this machine",
    "scaling up from a working small-scale run",
    "a production campaign that must fit the queue limits",
    "reproducing a collaborator's earlier result",
    "a deadline run where turnaround matters most",
    "restarting from a checkpoint after an interruption",
    "a parameter sweep of many similar runs",
    "porting from a different facility's system",
    "an unfamiliar user following a group's existing recipe",
    "a benchmarking run to establish scaling behaviour",
]


# A concrete, checkable physical system per application.
#
# Feedback on the first cut: Input preparation was too vague to grade — "classical MD,
# single-system benchmark input" gives a grader nothing to check an input deck against.
# A specification like "3C-SiC, 2x2x2 supercell, 60 Ry cutoff, 4x4x4 k-grid" does: the
# produced input either contains those values or it does not. Resource selection needs the
# same numbers for a different reason — you cannot size an allocation without knowing how
# big the physical system is.
#
# Where the catalog's performance/ records already name a real benchmark that was actually
# run, that exact system is used rather than an invented one (marked CATALOG below).
PHYSICAL_SYSTEMS = {
    "qe":          ("3C-SiC in the zinc-blende structure, 2x2x2 conventional supercell "
                    "(64 atoms), SCF total-energy calculation, plane-wave cutoff 60 Ry, "
                    "charge-density cutoff 480 Ry, 4x4x4 Monkhorst-Pack k-grid, PBE "
                    "functional, ultrasoft pseudopotentials"),
    "cp2k":        ("liquid water, 64 H2O molecules in a 12.42 Angstrom cubic periodic box, "
                    "Born-Oppenheimer MD in the NVT ensemble at 300 K, BLYP-D3, DZVP-MOLOPT "
                    "basis, 400 Ry cutoff, 0.5 fs timestep, 1000 steps"),
    "nwchem":      ("a single water molecule, B3LYP/6-31G* single-point energy"),   # CATALOG
    "pyscf":       ("benzene C6H6, RHF/cc-pVDZ single-point energy followed by MP2"),
    "lammps":      ("Lennard-Jones argon, 500,000 atoms on an fcc lattice, reduced density "
                    "0.8442, reduced temperature 0.72, NVE, 100,000 timesteps, "
                    "cutoff 2.5 sigma"),
    "namd":        ("solvated ApoA1 benchmark, 92,224 atoms, NPT at 310 K and 1 atm, 2 fs "
                    "timestep with rigid bonds, PME electrostatics, 12 Angstrom cutoff, "
                    "500,000 steps"),
    "gromacs":     ("hen egg-white lysozyme solvated in TIP3P water with 0.15 M NaCl, "
                    "~34,000 atoms, NPT at 300 K, 2 fs timestep, PME, 5 ns production"),
    "gromacs_hip": ("satellite tobacco mosaic virus (STMV) in explicit solvent, 1,066,628 "
                    "atoms, NPT at 300 K, 2 fs timestep, PME, 10 ns production"),
    "openmm":      ("Lennard-Jones fluid of 125,000 argon atoms, 1000 MD steps"),    # CATALOG
    "qmcpack":     ("bulk silicon in the diamond structure, 2x2x2 supercell (64 atoms), "
                    "diffusion Monte Carlo with a Slater-Jastrow trial wavefunction from a "
                    "prior DFT run, 4096 walkers, timestep 0.005 Ha^-1, 200 DMC blocks"),
    "hacc":        ("gravity-only cosmological N-body, 1024^3 particles in a 256 Mpc/h box, "
                    "LCDM with Omega_m=0.31, evolved from z=200 to z=0 in 200 steps"),
    "nekrs":       ("turbulent pipe flow at friction Reynolds number 550, 32,000 spectral "
                    "elements at polynomial order 7, 20,000 timesteps, statistics collected "
                    "over the final 10,000"),
    "nek5000":     ("turbulent channel flow at friction Reynolds number 180, 16,384 spectral "
                    "elements at polynomial order 8, 50,000 timesteps"),
    "moose":       ("2D transient heat conduction in a composite slab, 100x100 quadrilateral "
                    "mesh, Dirichlet boundaries at 300 K and 500 K, 50 timesteps of 0.1 s"),
    "alphafold":   ("human ubiquitin (UniProt P0CG48), 76-residue monomer, full database "
                    "search, 5 models with relaxation"),
    "openfold":    ("CASP14 target T1050, 779-residue monomer, full MSA search, 5 models"),
    "chai_lab":    ("the 7-residue peptide ACDEFGH, 3 trunk recycles, 50 diffusion steps"),  # CATALOG
    "hpl":         ("HPL LINPACK, problem size N=50000, block size NB=232, 2x2 process grid"),  # CATALOG
    "vllm":        ("Llama-3.1-8B offline inference, 50 prompts, max_tokens=50, "
                    "tensor parallel size 4"),                                        # CATALOG
    "deepspeed":   ("GPT feed-forward block, hidden size 2048, 12 layers, sequence length "
                    "512, batch size 8, ZeRO stage 1, 20 training steps"),             # CATALOG
    "pytorch":     ("ResNet-50 image classification on a 100,000-image subset, batch size "
                    "256 per GPU, mixed precision, 10 epochs"),
}


# ---------------------------------------------------------------------------------------
# Prompting rules folded in after preview testing.
#
# Each rule below targets a defect cluster actually counted in graded preview answers, not a
# guess at what might help. They are kept separate from `instructions` above so the baseline
# wording stays readable and so an A/B run can drop them with one flag.
#
#   Resource selection  — 20 defects sorted into 5 clusters: illegal/non-existent queue (3),
#                         fabricated performance evidence (4), arithmetic that does not
#                         follow (3), rank/GPU layout contradicting the build (3), supplied
#                         scaling guidance ignored (2).
#   Input preparation   — invented keywords, text written into binary files, and (introduced
#                         by the worked example itself) values and comment headers copied
#                         out of the example.
# ---------------------------------------------------------------------------------------
EXTRA_RULES = {
    # v4 = v2 restored verbatim, plus the two highest-reach Batch job creation rules and
    # nothing else.
    #
    # v3 replaced all of this with six clustered rules per subtask and regressed hard:
    # gpt-oss 15/40 -> 4/36 fully correct, completeness on Software selection 1.93 -> 1.14,
    # outright wrong-application picks 2/30 -> 6/28. The mechanism was not the judge policing
    # compliance (only 7% of defects cited a rule) but the rules changing behaviour: telling
    # a model to ground every claim in a catalog field and say nothing the catalog omits
    # taught it that a sparse entry disqualifies a code, so it picked whichever application
    # had the richest metadata over the one that fits the science. Six obligations also
    # create six new ways to be incomplete.
    #
    # So only Batch job creation is touched here, with two rules rather than six. It had the
    # most headroom (12/40, with 71% of its defects prompt-attributable) and is the most
    # mechanical of the four, which is where prescription is least likely to backfire.
    "Input preparation": (
        "\nThe prompt must additionally require the agent to:\n"
        "  (a) use only directives and keywords it is certain exist in this application's "
        "input format — omit a feature rather than invent a keyword for it;\n"
        "  (b) never fabricate the contents of binary or runtime-generated files (databases, "
        "wavefunction or checkpoint files, restart files, outputs) — list those as produced "
        "at runtime instead of writing text into them;\n"
        "  (c) treat any worked example given as a demonstration of FORM ONLY: block names, "
        "keyword spellings, card ordering. Its numerical values, chemical species, "
        "pseudopotential filenames and comment headers describe a DIFFERENT system and must "
        "not be carried over;\n"
        # (d) used to ask for a closing self-check. The rule it served,
        # INP.common.self_check_demonstrated, was removed in r21 after firing on 35 of 40
        # answers and making a pass arithmetically impossible for the whole subtask. The
        # instruction outlived the rule, so models were still spending output on a ritual
        # nothing scored. The underlying property is still checked, by
        # INP.qe.nat_matches_positions and friends, against the deck itself rather than
        # against the model's claim about it.
        "  (d) make sure any count you declare matches the entries you actually write out "
        "(a declared atom count against the positions listed, for example)."),
    "Resource selection": (
        "\nThe prompt must additionally require the agent to:\n"
        # Measured on v2: 5 of 40 answers requested something the scheduler would reject
        # outright — 36h walltime in a 24h queue, 19h in a 2h queue, a node count below the
        # queue minimum, a queue that does not exist. The old wording asked the agent to
        # state that the request fits; agents duly stated it and shipped the violation
        # anyway. So the order is inverted here: size the work first, then pick a queue that
        # admits it, and treat a failed check as something to fix rather than to report.
        "  (a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:\n"
        "        1. size the work and derive the walltime you actually need;\n"
        "        2. go through the supplied queue table and eliminate every queue whose "
        "maximum walltime is below that figure, or whose node range excludes your node "
        "count, naming for each the limit that rules it out;\n"
        "        3. choose from what survives, and state the verdict against each of the "
        "three limits separately — node minimum, node maximum, maximum walltime — giving the "
        "requested value, the limit and whether it passes. Any clear presentation will do; a "
        "table is fine.\n"
        "      Every one of those three lines must read PASS. If any reads FAIL, the answer "
        "is not finished: change the node count, cut the walltime, or move to a queue that "
        "admits the request, then redo the check. A request that breaches any limit is "
        "rejected by the scheduler at submission and is worth nothing, however well reasoned "
        "— never present one as the answer, and never round a walltime up past the cap;\n"
        "  (b) take ranks-per-node and GPUs-per-rank from the supplied application defaults, "
        "which are a property of how the code was built — only the NODE COUNT is the agent's "
        "to choose;\n"
        # The DERIVED/ASSUMED taxonomy was removed after measurement: the prompts supply
        # problem SIZE but never a RATE, so DERIVED was unreachable, and 8 of 9 firings of the
        # rule enforcing it were models picking the impossible branch. Asking for a label with
        # one valid option manufactures a failure mode.
        "  (c) do not claim a timing or throughput figure was measured or observed when the "
        "prompt supplies none; state plainly what you assumed and what margin you added;\n"
        "  (d) honour any scaling guidance supplied with the application, or say why it does "
        "not apply to this run;\n"
        "  (e) close with a plain restatement of nodes, ranks per node, total ranks, GPUs per "
        "node, walltime and queue, showing that total ranks = nodes x ranks per node."),
    # The only change from v2. Phrased to point at the supplied blocks rather than to name
    # what is in them — writing the directive names here would put the answer in the prompt.
    "Batch job creation": (
        "\nThe prompt must additionally require the agent to:\n"
        "  (a) request resources in exactly the form the supplied site conventions and worked "
        "example demonstrate, including every element they show, and add no per-chunk "
        "resource they omit, since nodes on these systems are allocated exclusively;\n"
        "  (b) include the full boilerplate: a job-name directive, output and error "
        "directives pointing at concrete paths under the stated working directory, an "
        "explicit change into that directory using the scheduler's own variable rather than a "
        "hardcoded path, and creation of any directory those paths reference."),
}

for _st, _extra in EXTRA_RULES.items():
    SUBTASKS[_st]["instructions"] += _extra

# Assets the agent cannot discover without tools; see skills/trinity_site.py for the
# measured effect of supplying each.
SUBTASKS["Batch job creation"]["needs_conventions"] = True
SUBTASKS["Batch job creation"]["gives_account"] = True
SUBTASKS["Input preparation"]["needs_deck_example"] = True
# Every subtask after the first is answered independently, so it must be told what the
# earlier stages correctly produced rather than left to re-derive them.
for _st, _sp in SUBTASKS.items():
    _sp["needs_prior_context"] = _sp["order"] >= 2


# ---------------------------------------------------------------------------------------
# A/B arms.
#
# BASE is v7 behaviour, untouched. RICH adds the catalog material the models were being graded
# against but never shown — most sharply `input_detection.content_markers`, which the judge
# greps for and the prompt omitted.
#
# The overlay touches ONLY "Input preparation", and that gating is load-bearing rather than
# tidiness: the same contract handed to Software selection leaks the application name on 7 of
# 39 anchors, because `log.lammps`, `OpenMM`, `NAMD` and `DeepSpeed` appear inside
# content_markers, filenames and output_patterns. `--leak-audit` asserts those 7 findings still
# appear as a negative control; a clean result there means the gate broke.
ARMS = {
    "base": {},
    "rich": {"Input preparation": {"needs_format_contract": True,
                                   "needs_system_context": True,
                                   "needs_input_scaling": True}},
}


def apply_arm(arm: str) -> dict:
    """SUBTASKS with an arm's overlay applied. Deep-copied — never mutates the module dict."""
    import copy
    if arm not in ARMS:
        raise KeyError(f"unknown arm {arm!r}; have {sorted(ARMS)}")
    out = copy.deepcopy(SUBTASKS)
    for st, flags in ARMS[arm].items():
        out[st].update(flags)
    return out


# ---------------------------------------------------------------------------------------
# The 10-anchor evaluation subset (40 samples: 10 x 4 subtasks).
#
# Stratified rather than sampled, so a 40-sample run still spans what varies:
#   all 7 systems - both schedulers (Perlmutter and Frontier are Slurm, the rest PBS Pro)
#   9 distinct applications across 9 scientific domains
#   3 of the 10 have a verified upstream input deck (nwchem, lammps, qe) and 7 do not, so
#   the effect of the Input-preparation worked example stays visible rather than assumed.
# ---------------------------------------------------------------------------------------
SUBSET = [
    ("Computational chemistry",             "nwchem",    "polaris"),
    ("Molecular dynamics",                  "lammps",    "polaris"),
    ("Computational fluid dynamics",        "nekrs",     "polaris"),
    ("Electronic structure (DFT)",          "qe",        "aurora"),
    ("Quantum Monte Carlo",                 "qmcpack",   "aurora"),
    ("Dense linear algebra",                "hpl",       "crux"),
    ("Molecular dynamics (biomolecular)",   "gromacs",   "sirius"),
    ("Protein structure prediction",        "alphafold", "perlmutter"),
    ("LLM inference serving",               "vllm",      "frontier"),
    ("Deep learning training",              "pytorch",   "sophia"),
]
assert all(a in ANCHORS for a in SUBSET), "subset must be drawn from verified anchors"
