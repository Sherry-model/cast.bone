#!/usr/bin/env python3
import argparse
import json
import os
import re
from typing import Dict, List, Tuple


V1_REQUIRED_BLOCKS = {
    "CORE_IDENTITY",
    "SAFETY_CONSTRAINTS",
    "EXPRESSION_BOUNDARY",
    "PREFERENCE",
    "AUDIT",
    "IMMUNE_SYSTEM",
}


def detect_version(text: str) -> str:
    if "∇Capsule.Soul" in text:
        return "v1"
    if "∇SOUL.v3" in text:
        return "v3"
    if "capsule::" in text:
        return "v5"
    return "unknown"


def parse_v1_permissions(text: str) -> Dict[str, str]:
    permissions: Dict[str, str] = {}
    pattern = re.compile(r"^\s*([A-Z_]+)\s*\[([^\]]+)\]\s*\{", re.MULTILINE)
    for match in pattern.finditer(text):
        name = match.group(1).strip()
        perm = match.group(2).strip()
        permissions[name] = perm
    return permissions


def validate_v1(text: str) -> Tuple[bool, Dict, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if "∇Capsule.Soul" not in text:
        errors.append("missing_root")

    permissions = parse_v1_permissions(text)
    missing = V1_REQUIRED_BLOCKS - set(permissions.keys())
    if missing:
        errors.append(f"missing_blocks:{','.join(sorted(missing))}")

    for name, perm in permissions.items():
        if not perm.startswith("∇"):
            warnings.append(f"permission_not_tagged:{name}")

    return len(errors) == 0, permissions, errors, warnings


def validate_v3(text: str) -> Tuple[bool, Dict, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if "∇schema.lock" not in text:
        errors.append("missing_schema_lock")
    if "∇seal.signature" not in text:
        errors.append("missing_signature")
    return len(errors) == 0, {}, errors, warnings


def validate_v5(text: str) -> Tuple[bool, Dict, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    capsules = re.findall(r"^\s*capsule::[A-Za-z0-9_.-]+\s*\{", text, re.MULTILINE)
    if not capsules:
        errors.append("missing_capsules")
    if "∇capsule.permissions" not in text and "∇capsule.lock" not in text and "∇permissions.root" not in text:
        warnings.append("missing_permissions_fields")
    return len(errors) == 0, {}, errors, warnings


def validate_file(path: str) -> Dict:
    if not os.path.exists(path):
        return {
            "ok": False,
            "version": "unknown",
            "errors": ["file_not_found"],
            "warnings": [],
            "permissions": {},
        }
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    version = detect_version(text)
    if version == "v1":
        ok, permissions, errors, warnings = validate_v1(text)
    elif version == "v3":
        ok, permissions, errors, warnings = validate_v3(text)
    elif version == "v5":
        ok, permissions, errors, warnings = validate_v5(text)
    else:
        ok, permissions, errors, warnings = False, {}, ["unknown_format"], []

    return {
        "ok": ok,
        "version": version,
        "errors": errors,
        "warnings": warnings,
        "permissions": permissions,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="ProtoLing minimal validator")
    parser.add_argument("--file", required=True)
    parser.add_argument("--json", action="store_true", help="Print JSON output")
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

