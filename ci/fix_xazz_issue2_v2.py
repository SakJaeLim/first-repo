#!/usr/bin/env python3
"""Apply the post-review DSL/remediation corrections to an applied Issue #2 patch.

This helper exists only in the external validation harness. The publish job
includes the resulting corrections in the final validated patch.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SELECT = re.compile(r"select\(\[(?P<body>[^\]]*)\]\)")


def fix_select_syntax(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        parts = [part.strip() for part in match.group("body").split(",") if part.strip()]
        fixed: list[str] = []
        for part in parts:
            if len(part) >= 2 and part[0] == part[-1] == '"':
                candidate = part[1:-1]
                if IDENTIFIER.fullmatch(candidate):
                    part = candidate
            fixed.append(part)
        return f"select([{', '.join(fixed)}])"

    return SELECT.sub(replace, text)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: fix_xazz_issue2_v2.py REPOSITORY_ROOT")

    root = Path(sys.argv[1]).resolve()
    security_path = root / "xazz-server/src/security.rs"
    security = fix_select_syntax(security_path.read_text(encoding="utf-8"))

    security = replace_once(
        security,
        """                let safe_columns: Vec<String> = target
                    .state
                    .columns
                    .values()
                    .filter(|column| passthrough_allowed(column))
                    .map(|column| column.name.clone())
                    .collect();
""",
        """                let safe_columns: Vec<String> = target
                    .state
                    .columns
                    .values()
                    .filter(|column| {
                        passthrough_allowed(column) && is_xazz_identifier(&column.name)
                    })
                    .map(|column| column.name.clone())
                    .collect();
""",
        "safe-column identifier filter",
    )
    security = replace_once(
        security,
        """                    let selected = safe_columns
                        .iter()
                        .map(|column| format!(\"\\\"{}\\\"\", escape_xzz_string(column)))
                        .collect::<Vec<_>>()
                        .join(\", \");
""",
        """                    let selected = safe_columns.join(\", \");
""",
        "valid select emission",
    )
    security = replace_once(
        security,
        "fn passthrough_allowed(column: &ColumnState) -> bool {\n",
        """fn is_xazz_identifier(value: &str) -> bool {
    let mut chars = value.chars();
    let Some(first) = chars.next() else {
        return false;
    };
    (first.is_ascii_alphabetic() || first == '_')
        && chars.all(|ch| ch.is_ascii_alphanumeric() || ch == '_')
}

fn passthrough_allowed(column: &ColumnState) -> bool {
""",
        "identifier helper insertion",
    )
    security_path.write_text(security, encoding="utf-8")

    example_path = root / "examples/security/patient_unsafe.xzz"
    example_path.write_text(
        fix_select_syntax(example_path.read_text(encoding="utf-8")),
        encoding="utf-8",
    )

    dataset_path = root / "experiments/slm_guardrail/data/security_remediation_seed.jsonl"
    records: list[str] = []
    for line_number, raw_line in enumerate(
        dataset_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line.strip():
            continue
        record = json.loads(raw_line)
        for key in ("input", "output"):
            record[key] = fix_select_syntax(record[key])
        records.append(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
    dataset_path.write_text("\n".join(records) + "\n", encoding="utf-8")

    remaining = []
    for path in (security_path, example_path, dataset_path):
        if 'select(["' in path.read_text(encoding="utf-8"):
            remaining.append(str(path.relative_to(root)))
    if remaining:
        raise RuntimeError(f"quoted select identifiers remain in: {remaining}")

    print("applied valid select syntax and deterministic remediation corrections")


if __name__ == "__main__":
    main()
