#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)

DEFAULT_INPUT = os.path.join(REPO_ROOT, "data", "samples", "争议样本.txt")
DEFAULT_SECTION = "MEMORY"
DEFAULT_PROTOLING = os.path.join(REPO_ROOT, "docs", "protoling", "SOUL_protoling_v6.proto")
AUDIT_LOG = os.path.join(REPO_ROOT, "data", "logs", "audit_log.jsonl")
OUTPUT_DIR = os.path.join(REPO_ROOT, "data", "tests")
AGENT_SCRIPT = os.path.join(BASE_DIR, "agent_immune_system.py")


def resolve_path(path: str) -> str:
    if not path:
        return path
    if os.path.isabs(path):
        return path
    return os.path.join(REPO_ROOT, path)


def read_samples(path: str, limit: int) -> List[str]:
    samples: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f.readlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            samples.append(line)
            if len(samples) >= limit:
                break
    return samples


def last_result_line(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    for line in reversed(lines):
        if any(key in line for key in ["Staged", "Quarantined", "Dropped"]):
            return line
    return lines[-1] if lines else ""


def read_new_logs(offset: int) -> (int, List[Dict]):
    if not os.path.exists(AUDIT_LOG):
        return offset, []
    with open(AUDIT_LOG, "r", encoding="utf-8") as f:
        f.seek(offset)
        data = f.read()
        new_offset = f.tell()
    entries = []
    for line in data.splitlines():
        try:
            entries.append(json.loads(line))
        except Exception:
            continue
    return new_offset, entries


def extract_llm(entry: Dict) -> Dict:
    llm = entry.get("llm") or []
    if not llm:
        return {}
    item = llm[0]
    return {
        "is_parasitic": item.get("is_parasitic"),
        "conflicts_core_identity": item.get("conflicts_core_identity"),
        "risk_level": item.get("risk_level"),
        "reason": item.get("reason"),
        "suggested_action": item.get("suggested_action"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch test for agent_immune_system.py")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--section", default=DEFAULT_SECTION)
    parser.add_argument("--llm", action="store_true")
    parser.add_argument("--providers", default="deepseek")
    parser.add_argument("--consensus", default="all")
    parser.add_argument("--mode", default="balanced")
    parser.add_argument("--protoling", default=DEFAULT_PROTOLING)
    parser.add_argument("--no-protoling", action="store_true")
    args = parser.parse_args()

    input_path = resolve_path(args.input)
    protoling_path = resolve_path(args.protoling)

    samples = read_samples(input_path, args.limit)
    if not samples:
        print("No samples found.")
        return

    offset = os.path.getsize(AUDIT_LOG) if os.path.exists(AUDIT_LOG) else 0

    output_lines: List[str] = []
    for idx, text in enumerate(samples, start=1):
        cmd = [
            sys.executable,
            AGENT_SCRIPT,
            "write",
            "--section",
            args.section,
            "--text",
            text,
            "--mode",
            args.mode,
            "--providers",
            args.providers,
            "--consensus",
            args.consensus,
            "--protoling",
            protoling_path,
        ]
        if args.llm:
            cmd.append("--llm")
        if args.no_protoling:
            cmd.append("--no-protoling")

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
        output = (result.stdout or "") + (result.stderr or "")
        status_line = last_result_line(output)

        offset, new_entries = read_new_logs(offset)
        matched = None
        for entry in reversed(new_entries):
            if entry.get("text") == text:
                matched = entry
                break

        llm_info = extract_llm(matched) if matched else {}

        line_block = [
            f"[{idx}] input: {text}",
            f"result: {status_line}",
            f"llm: {json.dumps(llm_info, ensure_ascii=False)}",
            "-" * 40,
        ]
        print("\n".join(line_block))
        output_lines.extend(line_block)

        if idx < len(samples):
            time.sleep(args.interval)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%m%d_%H:%M:%S")
    out_name = os.path.join(OUTPUT_DIR, f"测试记录_{stamp}.txt")
    with open(out_name, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")
    print(f"Saved: {out_name}")


if __name__ == "__main__":
    main()
