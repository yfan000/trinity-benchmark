#!/usr/bin/env python3
"""One normalized reader for the facility catalog. Everything else in the pipeline goes
through here.

The catalog (results/skills/trinity/catalog, a cache of github.com/zhenghh04/application_catalog
verified current with upstream HEAD 2026-05-13) holds 144 software entries, 9 systems and 114
performance records. Before this module the pipeline read a thin slice of it through
`trinity_generate.app_yaml()`, which had four problems that this module exists to fix:

  1. `yaml.safe_load` on a multi-document file raises. `software/frontier/gromacs.yaml` is a
     two-document stream whose second document is an entire GPU build — gpu_run_command,
     gpu_performance — invisible to every consumer.
  2. Parse errors were swallowed and `{}` returned, so two one-character syntax errors made
     Quantum ESPRESSO on Polaris contribute nothing, undetected. See catalog_repairs/.
  3. The same fact is spelled differently across systems: `queue` / `qos` / `partition`,
     `memory_per_node_gb: 512` vs `memory_per_node: "503GiB"`, `cpu_type` vs `cpu`,
     `install_path` vs `install_prefix`. Callers each re-derived this, or didn't.
  4. `aurora/vllm.yaml` has YAML comments INSIDE quoted scalars — `queue: "debug-scaling
     # or 'prod' for long-running"` — so the value a caller gets includes the commentary.

Two schema families coexist and consumers must not assume one. Most entries are "runtime"
records (name/description/input_detection/defaults/...); 14, nearly all of frontier/ and
sunspot/, are "build records" (app/system/status/install_prefix/built_date/compilers) with no
input information at all. `schema()` says which, and `has_contract()` says whether there is
enough to state an input-format contract.

Usage:
    python skills/catalog.py --fill        # coverage report + parse ledger
    python skills/catalog.py --parity      # assert we changed nothing on files that parse today
    python skills/catalog.py --repairs     # the upstream patch, ready to send
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "results" / "skills" / "trinity" / "catalog"
REPAIR_DIR = Path(__file__).resolve().parent / "catalog_repairs"
REPAIR_MANIFEST = REPAIR_DIR / "_manifest.yaml"

SCHEMA_RUNTIME = "runtime"
SCHEMA_BUILD_RECORD = "build_record"

# A comment that leaked into a quoted scalar. Two-or-more spaces before the `#` so that
# `#PBS`, `#SBATCH` and `md-#1` survive untouched.
_INLINE_COMMENT = re.compile(r"\s{2,}#.*$", re.S)

_WARNED: set[str] = set()


def _warn(msg: str) -> None:
    if msg not in _WARNED:
        _WARNED.add(msg)
        print(f"[catalog] {msg}", file=sys.stderr)


# --------------------------------------------------------------------------- repairs


@dataclass(frozen=True)
class Repair:
    path: str
    upstream_sha256: str
    error: str
    upstream_fix: str
    line: int
    old: str
    new: str
    status: str = "pending"   # applied | redundant | stale | pending


@lru_cache(maxsize=1)
def _repair_specs() -> dict[str, Repair]:
    if not REPAIR_MANIFEST.exists():
        return {}
    doc = yaml.safe_load(REPAIR_MANIFEST.read_text()) or {}
    return {r["path"]: Repair(**r) for r in (doc.get("repairs") or [])}


def _apply_repair(rel: str, text: str) -> tuple[str, str]:
    """Return (possibly repaired text, status). Never raises."""
    spec = _repair_specs().get(rel)
    if not spec:
        return text, "none"
    if hashlib.sha256(text.encode()).hexdigest() != spec.upstream_sha256:
        # Upstream changed. It may have been fixed (then the file now parses and we never got
        # here), or it may be broken in a NEW way. Either way, shadowing it with a repair
        # written against different bytes is worse than failing.
        return text, "stale"
    lines = text.splitlines()
    i = spec.line - 1
    if not (0 <= i < len(lines)) or lines[i] != spec.old:
        return text, "stale"
    lines[i] = spec.new
    return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), "applied"


# --------------------------------------------------------------------------- loading


def _merge(docs: list[dict]) -> dict:
    """Shallow-merge a multi-document stream, later documents winning.

    Only frontier/gromacs.yaml is multi-document today. Its doc 2 is a GPU variant carrying
    gpu_run_command and gpu_performance; merging rather than discarding is what makes those
    reachable, and shallow is right because the two documents describe one application.
    """
    out: dict = {}
    for d in docs:
        if isinstance(d, dict):
            out.update(d)
    return out


def _load_path(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text()
    rel = str(path.relative_to(CATALOG)) if CATALOG in path.parents else path.name
    try:
        return _merge(list(yaml.safe_load_all(text)))
    except yaml.YAMLError as first:
        repaired, status = _apply_repair(rel, text)
        if status == "applied":
            try:
                return _merge(list(yaml.safe_load_all(repaired)))
            except yaml.YAMLError as e:
                _warn(f"{rel}: repair applied but still unparseable: {e}")
                return {}
        if status == "stale":
            _warn(f"{rel}: has a repair on file but the bytes changed upstream — NOT applying "
                  f"it. Re-check the file and update catalog_repairs/_manifest.yaml.")
        else:
            _warn(f"{rel}: unparseable and no repair on file: "
                  f"{type(first).__name__}: {str(first)[:120]}")
        return {}


@lru_cache(maxsize=512)
def merged(system: str, app: str) -> dict:
    """The full entry for one (system, app), repaired and multi-document-merged."""
    return _load_path(CATALOG / "software" / system / f"{app}.yaml")


@lru_cache(maxsize=32)
def system_doc(system: str) -> dict:
    return _load_path(CATALOG / "systems" / f"{system}.yaml")


def _clean(v: Any) -> Any:
    """Strip a comment that leaked into a quoted scalar."""
    if isinstance(v, str):
        return _INLINE_COMMENT.sub("", v).strip()
    return v


# --------------------------------------------------------------------------- inputs


FileKind = Literal["extension", "filename", "glob", "directory"]


@dataclass(frozen=True)
class FileSpec:
    raw: str
    kind: FileKind
    ext: str | None
    base: str | None

    def __str__(self) -> str:
        return self.raw


def filespec(raw: str) -> FileSpec:
    """Classify one entry of required_inputs / input_files / output_patterns.

    These lists mix four things with no marker distinguishing them: bare extensions ('.nw'),
    literal filenames ('HPL.dat', 'input.xml'), globs ('*.lammps', 'data.*', 'output/*/x.pdb')
    and directories ('pseudo/'). Every consumer that treats them uniformly is wrong about
    three quarters of the catalog.
    """
    s = str(raw).strip()
    if s.endswith("/"):
        return FileSpec(s, "directory", None, s.rstrip("/"))
    if any(c in s for c in "*?[") or "/" in s:
        m = re.search(r"(\.[A-Za-z0-9_]+)$", s)
        return FileSpec(s, "glob", m.group(1) if m else None, None)
    if s.startswith(".") and s.count(".") == 1:
        return FileSpec(s, "extension", s, None)
    m = re.search(r"(\.[A-Za-z0-9_]+)$", s)
    if s.startswith("."):                      # '.scf.in' — a compound extension
        return FileSpec(s, "extension", m.group(1) if m else s, None)
    return FileSpec(s, "filename", m.group(1) if m else None, s)


@dataclass(frozen=True)
class Inputs:
    required: list[FileSpec] = field(default_factory=list)
    optional: list[FileSpec] = field(default_factory=list)
    outputs: list[FileSpec] = field(default_factory=list)
    extensions: list[str] = field(default_factory=list)
    filenames: list[str] = field(default_factory=list)
    markers: list[str] = field(default_factory=list)

    @property
    def authorable_outputs(self) -> list[FileSpec]:
        """Outputs the answer must NOT write contents for.

        Subtracting anything that is also an input matters: gromacs@sirius lists `md.gro` as an
        output while `.gro` is a legitimately authored input, so a naive read of
        output_patterns fires on correct work.
        """
        in_ext = {f.ext for f in (*self.required, *self.optional) if f.ext} | set(self.extensions)
        in_base = {f.base for f in (*self.required, *self.optional) if f.base} | set(self.filenames)
        return [f for f in self.outputs
                if (f.ext not in in_ext if f.ext else True) and f.base not in in_base]


def inputs(system: str, app: str) -> Inputs:
    d = merged(system, app)
    det = d.get("input_detection") or {}
    opt = list(d.get("optional_inputs") or [])
    req = list(d.get("required_inputs") or [])
    if not req and d.get("input_files"):
        # The catalog's convention is `input_files == required ∪ optional` — polaris/gromacs
        # has input_files [.tpr .gro .mdp .top], required [.tpr], optional [.gro .mdp .top …].
        # So falling back to input_files wholesale lists the optional files in both columns.
        # Subtract, and let the result stand even when it is empty: openmm@aurora records the
        # identical four entries as input_files AND optional_inputs, which under the convention
        # means nothing is required. Saying so is honest; printing the same four files as both
        # required and optional is incoherent to a reader. `fill_report` flags these for the
        # upstream issue list.
        req = [x for x in d["input_files"] if x not in set(opt)]
    return Inputs(
        required=[filespec(x) for x in req],
        optional=[filespec(x) for x in opt],
        outputs=[filespec(x) for x in (d.get("output_patterns") or [])],
        extensions=list(det.get("extensions") or []),
        filenames=list(det.get("filenames") or []),
        markers=list(det.get("content_markers") or []),
    )


# --------------------------------------------------------------------------- defaults


@dataclass(frozen=True)
class Defaults:
    nodes: int | None = None
    walltime_s: int | None = None
    ppn: int | None = None
    queue: str | None = None
    queue_field: str | None = None     # which of queue|qos|partition it came from
    account: str | None = None
    constraint: str | None = None
    filesystems: str | None = None
    raw: dict = field(default_factory=dict)


def _defaults_from(d: dict) -> Defaults:
    d = {k: _clean(v) for k, v in (d or {}).items()}
    qf = next((k for k in ("queue", "qos", "partition") if d.get(k)), None)
    return Defaults(
        nodes=d.get("nodes"), walltime_s=d.get("walltime"), ppn=d.get("ppn"),
        queue=d.get(qf) if qf else None, queue_field=qf,
        account=d.get("account"), constraint=d.get("constraint"),
        filesystems=d.get("filesystems") or ((d.get("custom_attributes") or {}) or {}).get("filesystems"),
        raw=d,
    )


def defaults(system: str, app: str) -> Defaults:
    return _defaults_from(merged(system, app).get("defaults") or {})


def job_defaults(system: str) -> Defaults:
    return _defaults_from(system_doc(system).get("job_defaults") or {})


# --------------------------------------------------------------------------- system


_GB = re.compile(r"([\d.]+)\s*(GiB|GB|TiB|TB)?", re.I)


def _to_gb(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    m = _GB.search(str(v))
    if not m:
        return None
    n = float(m.group(1))
    return n * 1024 if (m.group(2) or "").lower().startswith("t") else n


@dataclass(frozen=True)
class Hardware:
    nodes: int | None = None
    gpus_per_node: int | None = None
    gpu_type: str | None = None
    cpus_per_node: int | None = None
    memory_per_node_gb: float | None = None
    cpu_type: str | None = None
    raw: dict = field(default_factory=dict)


def hardware(system: str) -> Hardware:
    h = {k: _clean(v) for k, v in (system_doc(system).get("hardware") or {}).items()}
    return Hardware(
        nodes=h.get("nodes"), gpus_per_node=h.get("gpus_per_node"),
        gpu_type=h.get("gpu_type") or None,
        cpus_per_node=h.get("cpus_per_node") or h.get("threads_per_node"),
        # sophia writes `memory_per_node: "503GiB"`; everyone else `memory_per_node_gb: 512`
        memory_per_node_gb=_to_gb(h.get("memory_per_node_gb") or h.get("memory_per_node")),
        cpu_type=h.get("cpu_type") or h.get("cpu"),
        raw=h,
    )


@dataclass(frozen=True)
class Mount:
    name: str
    mount_path: str
    remote_base_path: str | None = None


def storage(system: str) -> list[Mount]:
    out = []
    for name, v in (system_doc(system).get("storage") or {}).items():
        if isinstance(v, dict) and v.get("mount_path"):
            out.append(Mount(name, v["mount_path"], v.get("remote_base_path") or None))
    return out


def software_build_dir(system: str) -> str | None:
    return system_doc(system).get("software_build_dir") or None


@lru_cache(maxsize=512)
def performance(system: str, app: str) -> dict:
    """A measured benchmark record. 114 files exist; only 5 are populated, all on Polaris."""
    return _load_path(CATALOG / "performance" / system / f"{app}.yaml")


@dataclass(frozen=True)
class Queue:
    name: str
    min_nodes: int | None = None
    max_nodes: int | None = None
    min_walltime: int | None = None
    max_walltime: int | None = None
    routing: bool = False
    notes: str | None = None
    raw: dict = field(default_factory=dict)


def queues(system: str) -> dict[str, Queue]:
    out = {}
    for name, v in ((system_doc(system).get("scheduler") or {}).get("queues") or {}).items():
        v = v or {}
        out[name] = Queue(name, v.get("min_nodes"), v.get("max_nodes"),
                          v.get("min_walltime"), v.get("max_walltime"),
                          bool(v.get("routing")), v.get("notes"), v)
    return out


def reservations(system: str) -> dict:
    return system_doc(system).get("reservations") or {}


def scheduler_kind(system: str) -> str:
    return ("Slurm" if (system_doc(system).get("scheduler") or {}).get("type") == "slurm"
            else "PBS Pro")


# --------------------------------------------------------------------------- introspection


def schema(system: str, app: str) -> str:
    d = merged(system, app)
    if "install_prefix" in d or ("app" in d and "name" not in d):
        return SCHEMA_BUILD_RECORD
    return SCHEMA_RUNTIME


def has_contract(system: str, app: str) -> bool:
    i = inputs(system, app)
    return bool(i.markers or i.filenames or i.extensions or i.required)


def list_apps(system: str) -> list[tuple[str, str, str]]:
    out = []
    for f in sorted((CATALOG / "software" / system).glob("*.yaml")):
        d = merged(system, f.stem)
        out.append((f.stem, d.get("name") or d.get("app") or f.stem, d.get("description") or ""))
    return out


def systems() -> list[str]:
    return sorted(p.stem for p in (CATALOG / "systems").glob("*.yaml")
                  if not p.stem.startswith("_"))


# Dotted paths that resolve to a normalized accessor rather than a literal walk, so a
# requirement YAML can name `defaults.queue` and get the dialect-collapsed value.
_ALIASES: dict[str, Any] = {
    "defaults.queue":   lambda s, a: defaults(s, a).queue,
    "defaults.ppn":     lambda s, a: defaults(s, a).ppn,
    "defaults.nodes":   lambda s, a: defaults(s, a).nodes,
    "defaults.account": lambda s, a: defaults(s, a).account,
    "hardware.memory_per_node_gb": lambda s, a: hardware(s).memory_per_node_gb,
    "hardware.cpu_type":           lambda s, a: hardware(s).cpu_type,
    "install_path": lambda s, a: merged(s, a).get("install_path")
                                 or merged(s, a).get("install_prefix"),
}


def get(system: str, app: str | None, dotted: str, default=None):
    """Dotted-path read with normalization-aware aliases and `a|b` alternation.

    `required_inputs|input_files` is an alternation on purpose: 97 entries carry one and 96 the
    other, and collapsing it to a single path silently changes behaviour on dozens of files.
    """
    for alt in dotted.split("|"):
        alt = alt.strip()
        if alt in _ALIASES and app is not None:
            v = _ALIASES[alt](system, app)
            if v not in (None, [], {}, ""):
                return v
            continue
        doc = merged(system, app) if app else system_doc(system)
        cur: Any = doc
        for part in alt.split("."):
            if not isinstance(cur, dict) or part not in cur:
                cur = None
                break
            cur = cur[part]
        if cur not in (None, [], {}, ""):
            return _clean(cur) if isinstance(cur, str) else cur
    return default


# --------------------------------------------------------------------------- reporting


# --------------------------------------------------------------------------- rendering


@dataclass(frozen=True)
class Section:
    label: str
    keys: list[str]
    budget: int


# Priority order for the raw catalog text handed to the REFERENCE-ANSWER GENERATOR.
#
# This replaces `system_cfg[:2600]` / `app_cfg[:2200]` at judge.py:616. Those clips were not
# merely lossy, they were inverted: Globus UUIDs and ClearML queue hashes sit at the TOP of
# every system file and survived, while `hardware` and `job_defaults` sit at the BOTTOM and
# were cut on 6 of 9 systems. vllm@frontier lost 71% of its entry including run_command and
# defaults — so the Claude reference answer for that anchor was written without them.
#
# Projection does most of the work. Dropping the endpoint IDs, which no generator can use,
# brings odo.yaml from 11,727 chars to about 2,200 — under the OLD budget, so nothing needs
# clipping at all in the common case.
SYSTEM_SECTIONS = [
    Section("identity",     ["name", "facility", "description"], 450),
    Section("hardware",     ["hardware"], 600),
    Section("queues",       ["scheduler"], 2100),
    Section("job_defaults", ["job_defaults"], 350),
    Section("storage",      ["storage", "software_build_dir"], 450),
    Section("reservations", ["reservations"], 300),
]

APP_SECTIONS = [
    # `app`/`status`/`install_prefix`/`binaries`/`gpu_run_command` are the build-record
    # spellings. Without them the 15 build-record entries and frontier/gromacs doc 2 would
    # render empty — and doc 2's gpu_run_command is the single most valuable field the
    # multi-document recovery buys.
    Section("identity", ["name", "app", "description", "category", "version",
                         "build_status", "status"], 500),
    Section("inputs",   ["required_inputs", "optional_inputs", "input_files",
                         "input_detection", "output_patterns"], 900),
    Section("launch",   ["run_command", "gpu_run_command", "binary", "binaries",
                         "setup", "modules"], 1600),
    Section("sizing",   ["defaults", "scaling_notes", "gpu_support", "gpu_notes"], 700),
    Section("build",    ["install_path", "install_prefix", "notes"], 400),
]


def render_sections(doc: dict, sections: list[Section]) -> str:
    """Labelled YAML sections, each independently budgeted, clipping announced when it happens.

    Keys in no section are dropped — that is a projection, not a clip, and it is deliberate:
    the endpoint UUIDs and ClearML hashes carry nothing a generator can act on.
    """
    out = []
    for s in sections:
        sub = {k: doc[k] for k in s.keys if doc.get(k) not in (None, "", [], {})}
        if not sub:
            continue
        body = yaml.safe_dump(sub, sort_keys=False, default_flow_style=False,
                              allow_unicode=True, width=100).rstrip()
        if len(body) > s.budget:
            body = (body[:s.budget].rstrip()
                    + f"\n[... {s.label} clipped, {len(body) - s.budget} chars omitted]")
        out.append(f"## {s.label}\n{body}")
    return "\n\n".join(out)


def render_system(system: str) -> str:
    return render_sections(system_doc(system), SYSTEM_SECTIONS)


def render_app(system: str, app: str, extra: dict | None = None) -> str:
    doc = dict(merged(system, app))
    if extra:
        doc = {**doc, **extra}
    return render_sections(doc, APP_SECTIONS)


def render_audit() -> list[dict]:
    """Per-anchor before/after sizes and what, if anything, still clips."""
    rows = []
    for sysn in systems():
        d = CATALOG / "software" / sysn
        raw_sys = (CATALOG / "systems" / f"{sysn}.yaml")
        for f in sorted(d.glob("*.yaml")) if d.exists() else []:
            r = render_app(sysn, f.stem)
            rows.append({"kind": "app", "what": f"{sysn}/{f.stem}",
                         "raw": len(f.read_text()), "rendered": len(r),
                         "clipped": "clipped," in r})
        if raw_sys.exists():
            r = render_system(sysn)
            rows.append({"kind": "system", "what": sysn, "raw": len(raw_sys.read_text()),
                         "rendered": len(r), "clipped": "clipped," in r})
    return rows


def parse_ledger() -> dict:
    ok, broken, repaired, stale = [], [], [], []
    for f in sorted(CATALOG.rglob("*.yaml")):
        rel = str(f.relative_to(CATALOG))
        text = f.read_text()
        try:
            list(yaml.safe_load_all(text))
            ok.append(rel)
            if rel in _repair_specs():
                repaired.append((rel, "redundant"))
        except yaml.YAMLError:
            _, status = _apply_repair(rel, text)
            if status == "applied" and _load_path(f):
                repaired.append((rel, "applied"))
            elif status == "stale":
                stale.append(rel)
            else:
                broken.append(rel)
    return {"ok": ok, "broken": broken, "repaired": repaired, "stale": stale}


def fill_report() -> dict:
    fields = ["name", "description", "version", "binary", "install_path", "modules", "setup",
              "run_command", "gpu_support", "gpu_notes", "scaling_notes", "required_inputs",
              "input_files", "optional_inputs", "output_patterns", "defaults", "build_status",
              "keywords", "notes"]
    n = Counter()
    det = Counter()
    schemas = Counter()
    quirks: dict[str, list[str]] = {"all_inputs_optional": [], "no_inputs_recorded": [],
                                    "no_ppn": []}
    total = 0
    for sysn in systems():
        d = CATALOG / "software" / sysn
        if not d.exists():
            continue
        for f in sorted(d.glob("*.yaml")):
            total += 1
            doc = merged(sysn, f.stem)
            for k in fields:
                if doc.get(k):
                    n[k] += 1
            i = inputs(sysn, f.stem)
            for k, v in (("extensions", i.extensions), ("filenames", i.filenames),
                         ("content_markers", i.markers)):
                if v:
                    det[k] += 1
            schemas[schema(sysn, f.stem)] += 1
            where = f"{sysn}/{f.stem}"
            if not i.required and i.optional:
                quirks["all_inputs_optional"].append(where)
            if not (i.required or i.optional or i.markers or i.extensions or i.filenames):
                quirks["no_inputs_recorded"].append(where)
            if doc.get("defaults") and not defaults(sysn, f.stem).ppn:
                quirks["no_ppn"].append(where)
    return {"total": total, "fields": n, "detection": det, "schemas": schemas,
            "quirks": quirks}


def _main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fill", action="store_true")
    ap.add_argument("--parity", action="store_true")
    ap.add_argument("--repairs", action="store_true")
    a = ap.parse_args()

    if a.repairs:
        led = parse_ledger()
        print("# Upstream patch for github.com/zhenghh04/application_catalog\n")
        for spec in _repair_specs().values():
            st = dict(led["repaired"]).get(spec.path, "broken")
            print(f"--- {spec.path}   [{st}]")
            print(f"    {spec.error}")
            print(f"    fix: {spec.upstream_fix}")
            print(f"    -{spec.old}")
            print(f"    +{spec.new}\n")
        return 0

    if a.parity:
        bad = 0
        for f in sorted(CATALOG.rglob("*.yaml")):
            text = f.read_text()
            try:
                want = _merge(list(yaml.safe_load_all(text)))
            except yaml.YAMLError:
                continue                      # only files that parse today are in scope
            rel = f.relative_to(CATALOG).parts
            got = (merged(rel[1], f.stem) if rel[0] == "software"
                   else system_doc(f.stem) if rel[0] == "systems" else _load_path(f))
            if rel[0] in ("software", "systems") and got != want:
                bad += 1
                print(f"  DIFF {f.relative_to(CATALOG)}")
        print(f"parity: {'OK — no file that parses today changed' if not bad else f'{bad} DIFFS'}")
        return 1 if bad else 0

    led = parse_ledger()
    rep = fill_report()
    print(f"catalog: {CATALOG.relative_to(ROOT)}")
    print(f"  files parsing cleanly   {len(led['ok'])}")
    print(f"  repaired                {len([r for r in led['repaired'] if r[1]=='applied'])}"
          f"   {[r[0] for r in led['repaired'] if r[1]=='applied']}")
    print(f"  redundant repairs       {len([r for r in led['repaired'] if r[1]=='redundant'])}"
          f"   (upstream fixed these — delete from the manifest)")
    print(f"  stale repairs           {len(led['stale'])}   {led['stale']}")
    print(f"  still broken            {len(led['broken'])}   {led['broken']}")
    print(f"\nsoftware entries: {rep['total']}   schemas: {dict(rep['schemas'])}")
    print(f"\n{'field':<22}{'non-empty':>10}{'':>4}pct")
    for k, v in rep["fields"].most_common():
        print(f"  {k:<20}{v:>10}{'':>4}{v/rep['total']:.0%}")
    print(f"\n{'input_detection':<22}{'non-empty':>10}")
    for k, v in rep["detection"].most_common():
        print(f"  {k:<20}{v:>10}{'':>4}{v/rep['total']:.0%}")
    print(f"\ndata-quality flags for the upstream report:")
    for k, v in rep["quirks"].items():
        print(f"  {k:<22}{len(v):>4}   {', '.join(v[:6])}{' …' if len(v) > 6 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
