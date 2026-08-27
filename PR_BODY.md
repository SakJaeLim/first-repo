## Summary
- add deterministic Policy-as-Code inspection over Xazz AST and lineage
- block identifiers, unsafe row-level sensitive output, unsafe training inputs, and unsafe local paths before execution
- add local analyze/remediate/execute endpoints with exact-origin CORS, request limit, timeout, and deterministic revalidation
- preserve policy provenance and clarify that DP does not replace identifier removal or aggregation
- add synthetic healthcare examples and Qwen2.5-Coder/Unsloth QLoRA + Ollama scaffold

## Verification
Validated on Ubuntu, Windows, and macOS; Visual IDE build/contract/contrast tests also pass.

## Remaining Issue #2 work
Actual CUDA QLoRA training, GGUF/public weights, model card, and trained-model evaluation are not claimed by this PR.

Refs #2
