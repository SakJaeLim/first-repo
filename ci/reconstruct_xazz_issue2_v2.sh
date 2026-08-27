#!/usr/bin/env bash
set -euo pipefail

output_path="${1:?usage: reconstruct_xazz_issue2_v2.sh OUTPUT_PATH}"

{
  cat ci/xazz_issue2_v2.patch.b64.part00
  cat ci/xazz_issue2_v2.patch.b64.part01
  cat ci/xazz_issue2_v2.patch.b64.part02
  cat ci/xazz_issue2_v2.patch.b64.part03
  cat ci/xazz_issue2_v2.patch.b64.part04
  cat ci/xazz_issue2_v2.patch.b64.part05
  cat ci/xazz_issue2_v2.patch.b64.part06
  cat ci/xazz_issue2_v2.patch.b64.part07.sub00
  cat ci/xazz_issue2_v2.patch.b64.part07.sub01
  cat ci/xazz_issue2_v2.patch.b64.part07.sub02
  cat ci/xazz_issue2_v2.patch.b64.part07.sub03
  cat ci/xazz_issue2_v2.patch.b64.part07.sub04
  cat ci/xazz_issue2_v2.patch.b64.part07.sub05
  cat ci/xazz_issue2_v2.patch.b64.part07.sub06
  cat ci/xazz_issue2_v2.patch.b64.part08
  cat ci/xazz_issue2_v2.patch.b64.part09
} | base64 -d | gzip -d > "$output_path"

sha256sum "$output_path"
