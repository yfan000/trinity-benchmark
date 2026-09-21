#!/usr/bin/env python3
"""Generate MATRIX.md from application_catalog/software/<system>/*.yaml files."""
from __future__ import annotations
import glob
import os
import re
from collections import defaultdict
from datetime import date

CATALOG = os.path.dirname(os.path.abspath(__file__))
SW_DIR = os.path.join(CATALOG, "software")

SYSTEMS = ["aurora", "polaris", "crux", "sophia", "sirius",
           "frontier", "perlmutter", "sunspot", "odo"]


def parse_yaml_min(path: str) -> dict:
    """Minimal YAML parser pulling top-level scalar fields we care about."""
    out: dict = {}
    text = open(path).read()
    for key in ("name", "version", "binary", "install_path",
                "install_prefix", "build_status", "category"):
        m = re.search(rf'^{key}:\s*"?([^"\n]+?)"?\s*$', text, re.M)
        if m:
            out[key] = m.group(1).strip()
    return out


def status(meta: dict) -> str:
    """Return ✓ if a real path is recorded, ~ if yaml exists but no path, — if absent."""
    p = meta.get("binary") or meta.get("install_path") or meta.get("install_prefix")
    if not p or p in ("python", "python3", "deepspeed", "gmx", "namd3",
                      "vasp_std", "xhpl", "nekrs"):
        return "~"
    if p.startswith("/"):
        return "✓"
    return "~"


# Collect per-(app, system) data
by_app: dict[str, dict[str, dict]] = defaultdict(dict)
for sys in SYSTEMS:
    sd = os.path.join(SW_DIR, sys)
    if not os.path.isdir(sd):
        continue
    for yml in sorted(glob.glob(os.path.join(sd, "*.yaml"))):
        app = os.path.basename(yml).replace(".yaml", "")
        if app.startswith("_"):
            continue
        by_app[app][sys] = parse_yaml_min(yml)

apps = sorted(by_app.keys())

# Build matrix
out = []
out.append(f"# Application × System Matrix\n")
out.append(f"Generated: {date.today().isoformat()}  |  "
           f"{len(apps)} apps  |  {len(SYSTEMS)} systems\n")
out.append("Legend: ✓ = installed path recorded, "
           "~ = yaml exists but path empty, — = not catalogued\n")

# Table header
hdr = "| Application | " + " | ".join(s.capitalize() for s in SYSTEMS) + " |"
sep = "|" + "---|" * (len(SYSTEMS) + 1)
out.append(hdr)
out.append(sep)
for app in apps:
    cells = []
    for s in SYSTEMS:
        if s in by_app[app]:
            cells.append(status(by_app[app][s]))
        else:
            cells.append("—")
    out.append(f"| **{app}** | " + " | ".join(cells) + " |")

# Install paths section
out.append("\n## Install Paths\n")
for app in apps:
    out.append(f"### {app}\n")
    out.append("| System | Version | Install Path |")
    out.append("|--------|---------|-------------|")
    for s in SYSTEMS:
        if s not in by_app[app]:
            continue
        meta = by_app[app][s]
        ver = meta.get("version", "—") or "—"
        path = (meta.get("binary") or meta.get("install_path")
                or meta.get("install_prefix") or "")
        if not path or not path.startswith("/"):
            path = "*(not recorded)*"
        else:
            path = f"`{path}`"
        out.append(f"| {s} | {ver} | {path} |")
    out.append("")

# Write
matrix_path = os.path.join(CATALOG, "MATRIX.md")
with open(matrix_path, "w") as f:
    f.write("\n".join(out) + "\n")

# Summary stats
print(f"Wrote {matrix_path}")
print(f"  apps: {len(apps)}, systems: {len(SYSTEMS)}")
for s in SYSTEMS:
    n = sum(1 for a in apps
            if s in by_app[a] and status(by_app[a][s]) == "✓")
    total = sum(1 for a in apps if s in by_app[a])
    print(f"  {s}: {n}/{total} apps with full path")
