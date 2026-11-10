#!/usr/bin/env python3
"""
Team NERV Battle Runner: Fast Parallel Reconnaissance Suite
Runs crawler.js, audit_accessibility.js, and security_probe.py in parallel.
Dumps aggregated output into evidence/recon_summary.json for instant agent analysis.
"""

import sys
import json
import subprocess
import time
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = WORKSPACE_ROOT / "evidence"
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"

def run_cmd(cmd_list: list[str]) -> tuple[int, str, str]:
    start = time.time()
    proc = subprocess.run(cmd_list, capture_output=True, text=True, cwd=str(WORKSPACE_ROOT))
    duration = round(time.time() - start, 2)
    return proc.returncode, proc.stdout, proc.stderr, duration

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/battle_runner.py <TARGET_URL>")
        sys.exit(1)

    target_url = sys.argv[1].strip()
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n========================================================")
    print(f" 🚀 TEAM NERV BATTLE RUNNER: TARGET RECONNAISSANCE")
    print(f" Target: {target_url}")
    print(f" Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"========================================================\n")

    summary = {
        "target_url": target_url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "crawler": {},
        "accessibility": {},
        "security": {}
    }

    # 1. Run Crawler
    print("[1/3] Running Crawler & DOM Sniffer...")
    code, out, err, dur = run_cmd(["node", str(SCRIPTS_DIR / "crawler.js"), target_url])
    summary["crawler"] = {
        "status": "success" if code == 0 else "error",
        "duration_sec": dur,
        "stdout": out,
        "stderr": err
    }
    print(f"  └── Finished in {dur}s (Exit code: {code})")

    # 2. Run Accessibility Audit
    print("[2/3] Running Axe-core WCAG 2.1 AA Audit...")
    code, out, err, dur = run_cmd(["node", str(SCRIPTS_DIR / "audit_accessibility.js"), target_url])
    summary["accessibility"] = {
        "status": "success" if code == 0 else "error",
        "duration_sec": dur,
        "stdout": out,
        "stderr": err
    }
    print(f"  └── Finished in {dur}s (Exit code: {code})")

    # 3. Run Security Header Probe & Route Recon
    print("[3/3] Running HTTP Security Header & Route Probe...")
    code, out, err, dur = run_cmd(["python3", str(SCRIPTS_DIR / "security_probe.py"), target_url, "--recon"])
    summary["security"] = {
        "status": "success" if code == 0 else "error",
        "duration_sec": dur,
        "stdout": out,
        "stderr": err
    }
    print(f"  └── Finished in {dur}s (Exit code: {code})")

    # Save aggregated report
    summary_path = EVIDENCE_DIR / "recon_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\n[✓] Aggregated reconnaissance saved to: {summary_path}")
    print("========================================================\n")

if __name__ == "__main__":
    main()
