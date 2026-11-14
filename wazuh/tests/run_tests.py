#!/usr/bin/env python3
"""Run every test case in wazuh/tests/cases/*.json through wazuh-logtest
inside the running Wazuh manager container and compare the results."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CONTAINER = os.environ.get("CONTAINER", "wazuh-manager")
CASES_DIR = Path(__file__).parent / "cases"
PHASE1 = "**Phase 1: Completed pre-decoding."


def run_logtest(lines):
    """Send all lines through one logtest session, return one output block per line."""
    cmd = ["docker", "exec", "-i", CONTAINER, "/var/ossec/bin/wazuh-logtest", "-q"]
    stdin = "\n".join(lines) + "\n"
    try:
        out = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=120).stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    return out.split(PHASE1)[1:]


def parse(block):
    decoder = re.search(r"\*\*Phase 2: Completed decoding\.\s+name: '([^']+)'", block)
    phase3 = block.split("**Phase 3: Completed filtering (rules).", 1)
    rule = level = None
    if len(phase3) == 2:
        rid = re.search(r"id: '(\d+)'", phase3[1])
        lvl = re.search(r"level: '(\d+)'", phase3[1])
        rule = rid.group(1) if rid else None
        level = int(lvl.group(1)) if lvl else None
    return {
        "decoder": decoder.group(1) if decoder else None,
        "rule": rule,
        "level": level,
        "alert": "**Alert to be generated." in block,
    }


def main():
    files = sorted(CASES_DIR.glob("*.json"))
    if not files:
        print(f"No test cases found in {CASES_DIR}")
        return 1

    failures = 0
    total = 0
    for f in files:
        cases = json.loads(f.read_text())
        blocks = run_logtest([c["log"] for c in cases])
        print(f"\n== {f.name} ==")
        for i, case in enumerate(cases):
            total += 1
            if i >= len(blocks):
                print(f"  FAIL  {case['name']}: no logtest output for this line")
                failures += 1
                continue
            got = parse(blocks[i])
            problems = []
            for key in ("decoder", "rule", "level", "alert"):
                if key in case and str(case[key]) != str(got[key]):
                    problems.append(f"{key}: expected {case[key]!r}, got {got[key]!r}")
            if problems:
                failures += 1
                print(f"  FAIL  {case['name']}")
                for p in problems:
                    print(f"          {p}")
            else:
                print(f"  PASS  {case['name']}")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
