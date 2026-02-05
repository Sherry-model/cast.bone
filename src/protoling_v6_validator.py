#!/usr/bin/env python3
import argparse
import json
import os
import re
from typing import Dict, List, Tuple


def detect_version(text: str) -> str:
    if "capsule::" in text and "capsule::permissions.schema" in text:
        return "v6"
    if "capsule::" in text:
        return "v5"
    return "unknown"


def extract_capsules(text: str) -> List[Tuple[str, str]]:
    lines = text.splitlines()
    capsules: List[Tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^\s*capsule::([A-Za-z0-9_.-]+)\s*\{", line)
        if not match:
            i += 1
            continue
        name = match.group(1)
        brace = line.count("{") - line.count("}")
        block_lines = [line]
        i += 1
        while i < len(lines) and brace > 0:
            line = lines[i]
            brace += line.count("{") - line.count("}")
            block_lines.append(line)
            i += 1
        capsules.append((name, "\n".join(block_lines)))
    return capsules


def parse_list(value: str) -> List[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    items = []
    for raw in value.split(","):
        token = raw.strip().strip('"').strip("'")
        if token:
            items.append(token)
    return items


def parse_permissions_schema(text: str) -> Dict:
    schema = {
        "capsule_default": "append",
        "strict_prefix": [".kernel", ".witness", ".switch"],
        "write_policy": "deny-unknown",
        "error_strategy": "layered-risk",
    }
    match = re.search(r"capsule::permissions\.schema\s*\{", text)
    if not match:
        return schema
    start = match.start()
    sub = text[start:]
    # quick capture of schema block
    brace = 0
    body = []
    for ch in sub:
        if ch == "{":
            brace += 1
        elif ch == "}":
            brace -= 1
        body.append(ch)
        if brace == 0:
            break
    block = "".join(body)

    m = re.search(r"∇capsule\.default\s*=\s*\"([^\"]+)\"", block)
    if m:
        schema["capsule_default"] = m.group(1).strip()
    m = re.search(r"∇capsule\.strict_prefix\s*=\s*(\[[^\]]*\])", block)
    if m:
        schema["strict_prefix"] = parse_list(m.group(1))
    m = re.search(r"∇write\.policy\s*=\s*\"([^\"]+)\"", block)
    if m:
        schema["write_policy"] = m.group(1).strip()
    m = re.search(r"∇error\.strategy\s*=\s*\"([^\"]+)\"", block)
    if m:
        schema["error_strategy"] = m.group(1).strip()
    return schema


def parse_capsule_permissions(name: str, block: str, schema: Dict) -> Dict:
    raw_perm = None
    match = re.search(r"∇capsule\.permissions\s*=\s*\"([^\"]+)\"", block)
    if match:
        raw_perm = match.group(1).strip()
    locked = re.search(r"∇capsule\.lock\s*=", block) is not None

    write_allow: List[str] = []
    match = re.search(r"∇write\.allow\s*=\s*(\[[^\]]*\])", block)
    if match:
        write_allow = parse_list(match.group(1))

    strict_prefixes = schema.get("strict_prefix", [])
    is_critical = any(prefix in name for prefix in strict_prefixes) or name.endswith("permissions.schema")

    if is_critical:
        effective = "immutable"
    elif raw_perm:
        effective = raw_perm
    elif locked:
        effective = "immutable"
    else:
        effective = schema.get("capsule_default", "append")

    return {
        "permissions": raw_perm or "",
        "effective_permission": effective,
        "write_allow": write_allow,
        "locked": locked,
        "critical": is_critical,
    }


def default_section_map() -> Dict[str, str]:
    return {
        "CORE_IDENTITY": "soul.kernel",
        "SAFETY_BOUNDARIES": "soul.kernel",
        "MEMORY": "behavior.protocol",
        "PREFERENCES": "aesthetic.core",
        "AUDIT_MARKS": "soul.kernel",
    }


def validate_file(path: str) -> Dict:
    if not os.path.exists(path):
        return {
            "ok": False,
            "version": "unknown",
            "errors": ["file_not_found"],
            "warnings": [],
            "capsules": {},
            "schema": {},
            "section_map": default_section_map(),
        }
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    version = detect_version(text)
    errors: List[str] = []
    warnings: List[str] = []

    schema = parse_permissions_schema(text)
    capsules = extract_capsules(text)
    if not capsules:
        errors.append("missing_capsules")
    capsule_map: Dict[str, Dict] = {}
    for name, block in capsules:
        if name == "permissions.schema":
            continue
        capsule_map[name] = parse_capsule_permissions(name, block, schema)

    if "permissions.schema" not in [name for name, _ in capsules]:
        warnings.append("missing_permissions_schema")

    ok = len(errors) == 0
    return {
        "ok": ok,
        "version": "v6" if version == "v6" else version,
        "errors": errors,
        "warnings": warnings,
        "capsules": capsule_map,
        "schema": {
            "capsule_default": schema.get("capsule_default", "append"),
            "strict_prefix": schema.get("strict_prefix", []),
            "write_policy": schema.get("write_policy", "deny-unknown"),
            "error_strategy": schema.get("error_strategy", "layered-risk"),
        },
        "section_map": default_section_map(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="ProtoLing v6 minimal validator")
    parser.add_argument("--file", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate_file(args.file)
    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        status = "OK" if report["ok"] else "FAIL"
        print(f"{status} version={report['version']}")
        if report["errors"]:
            print(f"errors: {', '.join(report['errors'])}")
        if report["warnings"]:
            print(f"warnings: {', '.join(report['warnings'])}")
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
