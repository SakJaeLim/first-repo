# Xazz Issue #2 — Validated delivery

Target: `x1zzdev/Xazz` Issue #2, **Policy-as-Code 정적 가드레일 및 sLM 코드 보정 API 구축**.

## Implemented MVP

- AST/data-lineage Policy-as-Code validation
- Direct identifier, quasi-identifier, sensitive attribute and unsafe sink rules
- Pre-execution rejection (`HTTP 422`, runner is not invoked)
- Deterministic safe-plan remediation
- Optional local Ollama proposer with deterministic revalidation/fallback
- SHA-256 policy/code/audit evidence
- Synthetic healthcare policy, unsafe/safe `.xzz` demos
- Qwen2.5-Coder-1.5B + Unsloth QLoRA/GGUF/Ollama reproducibility scaffold

## Validation

Green GitHub Actions run:

- https://github.com/SakJaeLim/first-repo/actions/runs/33032919657

Checks passed:

- synthetic corpus validation
- Python syntax validation
- `cargo fmt --all -- --check`
- focused unit tests (17)
- focused Clippy with `-D warnings`
- `cargo test --workspace`
- workspace Clippy baseline
- security API build
- API smoke test: unsafe rejected, safe approved, remediation approved, execution denied with audit receipt

## Honest model status

The repository contains the training, GGUF export and Ollama serving **scaffold**. It does not contain a trained LoRA adapter or GGUF weight, and no claim is made that GPU fine-tuning or model-quality evaluation has already been completed.

## Upstream delivery blocker

The connected GitHub App can read `x1zzdev/Xazz`, but GitHub returns `403 Resource not accessible by integration` for branch creation, commits, issue comments and PR creation because the app is not installed for the `x1zzdev` organization. The implementation and final patch are prepared; upstream submission requires either the app installation on `x1zzdev/Xazz` or a real `SakJaeLim/Xazz` fork.
