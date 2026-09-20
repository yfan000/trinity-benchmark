#!/usr/bin/env python3
"""Cache ALCF documentation pages that ground the synthetic HPC task instances.

The instances have to contain real ALCF specifics — actual queue names, real PBS directive
syntax, the filesystems people actually mount — or the mapping is measuring a model's idea
of HPC rather than HPC. Pages are cached to disk so generation is reproducible and does not
re-hit the docs site on every run.

Usage:
    python skills/hpc_fetch_docs.py           # fetch anything not already cached
    python skills/hpc_fetch_docs.py --force   # re-fetch everything
"""
from __future__ import annotations
import argparse
import re
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "results" / "skills" / "hpc" / "docs"

BASE = "https://docs.alcf.anl.gov"
# Paths taken from https://docs.alcf.anl.gov/sitemap.xml, not guessed — the obvious-looking
# URLs (e.g. /polaris/hardware-overview/machine-overview/) mostly 404.
PAGES = {
    "polaris-running-jobs":    "/polaris/running-jobs/",
    "polaris-using-gpus":      "/polaris/running-jobs/using-gpus/",
    "polaris-compiling":       "/polaris/compiling-and-linking/",
    "polaris-programming":     "/polaris/compiling-and-linking/polaris-programming-models/",
    "polaris-spack":           "/polaris/applications-and-libraries/libraries/spack-pe/",
    "polaris-containers":      "/polaris/containers/containers/",
    "polaris-debug-cudagdb":   "/polaris/debugging-tools/CUDA-GDB/",
    "polaris-perf-nsight":     "/polaris/performance-tools/NVIDIA-Nsight/",
    "aurora-running-jobs":     "/aurora/running-jobs-aurora/",
    "aurora-debugging":        "/aurora/debugging/",
    "aurora-perf-tools":       "/aurora/performance-tools/",
    "aurora-node-perf":        "/aurora/node-performance-overview/node-performance-overview/",
    "sophia-running-jobs":     "/sophia/queueing-and-running-jobs/running-jobs/",
    "running-jobs-overview":   "/running-jobs/",
    "example-job-scripts":     "/running-jobs/example-job-scripts/",
    "qsub-options":            "/running-jobs/not_in_nav/pbs-qsub-options-table/",
    "machine-reservations":    "/running-jobs/machine-reservations/",
    "known-issues":            "/running-jobs/known-issues/",
    "queue-scheduling":        "/policies/queue-scheduling/",
    "data-globus":             "/data-management/data-transfer/using-globus/",
    "data-sftp-scp":           "/data-management/data-transfer/sftp-scp/",
    "data-filesystems":        "/data-management/filesystem-and-storage/",
    "data-quotas":             "/data-management/filesystem-and-storage/disk-quota/",
    "data-hpss":               "/data-management/filesystem-and-storage/hpss/",
    "globus-compute":          "/services/globus-compute/",
}


def to_text(html: str) -> str:
    """Strip an mkdocs page down to readable text, keeping code blocks intact.

    Code is the part that matters here — a task instance is only grounded if it carries a
    real `qsub` line — so <pre>/<code> content is preserved verbatim while chrome is dropped.
    """
    html = re.sub(r"<(script|style|nav|header|footer)\b[^>]*>.*?</\1>", " ", html,
                  flags=re.S | re.I)
    html = re.sub(r"<pre[^>]*>(.*?)</pre>", lambda m: "\n```\n" + m.group(1) + "\n```\n",
                  html, flags=re.S | re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</(p|div|li|h[1-6]|tr)>", "\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", "", html)
    for entity, char in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                         ("&#39;", "'"), ("&nbsp;", " ")):
        html = html.replace(entity, char)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return "\n".join(line.rstrip() for line in html.splitlines()).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ok = failed = skipped = 0

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        for name, path in PAGES.items():
            out = DOCS_DIR / f"{name}.md"
            if out.exists() and not args.force:
                skipped += 1
                continue
            url = BASE + path
            try:
                r = client.get(url)
                r.raise_for_status()
                text = to_text(r.text)
                if len(text) < 500:
                    print(f"  THIN  {name}: only {len(text)} chars — check the URL")
                    failed += 1
                    continue
                out.write_text(f"<!-- source: {url} -->\n\n{text}\n")
                print(f"  ok    {name}: {len(text):,} chars")
                ok += 1
            except Exception as e:
                print(f"  FAIL  {name}: {type(e).__name__}: {str(e)[:90]}")
                failed += 1
            time.sleep(0.4)  # be polite to the docs host

    print(f"\n{ok} fetched, {skipped} already cached, {failed} failed -> {DOCS_DIR}")
    return 1 if ok == 0 and skipped == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
