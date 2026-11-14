#!/usr/bin/env python3
"""Run every test case in tests/cases/*.json through the Wazuh logtest service
and compare the results.

Runs ON the Wazuh manager (inside the CI container, or on Alduin), as root:
  /var/ossec/framework/python/bin/python3 run_tests.py
"""
import json
import socket
import struct
import sys
import time
from pathlib import Path

LOGTEST_SOCKET = "/var/ossec/queue/sockets/logtest"
CASES_DIR = Path(__file__).parent / "cases"


def logtest(event, token=None):
    """Send one event to the logtest socket and return the decoded JSON reply."""
    request = {
        "version": 1,
        "origin": {"name": "run_tests", "module": "wazuh-logtest"},
        "command": "log_processing",
        "parameters": {"event": event, "log_format": "syslog", "location": "stdin"},
    }
    if token:
        request["parameters"]["token"] = token
    payload = json.dumps(request).encode()

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(LOGTEST_SOCKET)
    s.sendall(struct.pack("<I", len(payload)) + payload)
    size = struct.unpack("<I", s.recv(4, socket.MSG_WAITALL))[0]
    reply = s.recv(size, socket.MSG_WAITALL)
    s.close()
    return json.loads(reply.decode())


def wait_for_logtest(retries=12, delay=5):
    for attempt in range(1, retries + 1):
        try:
            logtest("warmup")
            return True
        except (FileNotFoundError, ConnectionRefusedError, OSError) as e:
            print(f"  (logtest not ready, attempt {attempt}: {e})")
            time.sleep(delay)
    return False


def summarize(reply):
    data = reply.get("data", {})
    out = data.get("output", {}) or {}
    decoder = out.get("decoder", {}) or {}
    rule = out.get("rule", {}) or {}
    return {
        "error": reply.get("error", 0),
        "messages": data.get("messages", []),
        "token": data.get("token"),
        "decoders": {decoder.get("name"), decoder.get("parent")} - {None},
        "rule": rule.get("id"),
        "level": rule.get("level"),
        "alert": bool(data.get("alert", False)),
    }


def main():
    files = sorted(CASES_DIR.glob("*.json"))
    if not files:
        print(f"No test cases found in {CASES_DIR}")
        return 1
    if not wait_for_logtest():
        print(f"Could not reach the logtest socket at {LOGTEST_SOCKET}")
        return 1

    failures = total = 0
    for f in files:
        print(f"\n== {f.name} ==")
        token = None
        for case in json.loads(f.read_text()):
            total += 1
            try:
                got = summarize(logtest(case["log"], token))
            except Exception as e:  # noqa: BLE001
                failures += 1
                print(f"  FAIL  {case['name']}: {e}")
                continue
            token = got["token"] or token

            problems = []
            if got["error"]:
                problems.append(f"logtest error {got['error']}: {got['messages']}")
            if "decoder" in case and case["decoder"] not in got["decoders"]:
                problems.append(f"decoder: expected {case['decoder']!r}, got {sorted(got['decoders']) or None}")
            if "rule" in case and str(case["rule"]) != str(got["rule"]):
                problems.append(f"rule: expected {case['rule']!r}, got {got['rule']!r}")
            if "level" in case and str(case["level"]) != str(got["level"]):
                problems.append(f"level: expected {case['level']!r}, got {got['level']!r}")
            if "alert" in case and bool(case["alert"]) != got["alert"]:
                problems.append(f"alert: expected {case['alert']!r}, got {got['alert']!r}")

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
