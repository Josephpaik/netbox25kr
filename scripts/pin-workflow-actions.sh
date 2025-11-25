#!/usr/bin/env bash
set -euo pipefail
# Usage:
#   GITHUB_TOKEN=... bash scripts/pin-workflow-actions.sh
#
# 목적: .github/workflows의 uses: 항목들 중 v3/v4는 유지하고,
#       그 외의 태그(v1, v5, v9 등)는 해당 태그가 가리키는 최종 커밋 SHA(40자)로 대체.
#       또한 uses: 값에 남아있는 <> 꺾쇠괄호를 제거.
#
# 변경 대상 파일 목록(필요시 더 추가하세요)
WORKFLOW_FILES=(
  ".github/workflows/ci.yml"
  ".github/workflows/update-translation-strings.yml"
  ".github/workflows/close-stale-issues.yml"
  ".github/workflows/close-incomplete-issues.yml"
)

# 태그를 SHA로 바꿀 대상 액션과 태그 (key: owner/repo, value: tag)
# 사용자 요청: v3와 v4는 유지하므로 목록에 포함하지 않음.
declare -A TARGET_TAGS=(
  ["actions/setup-python"]="v5"
  ["actions/create-github-app-token"]="v1"
  ["actions/stale"]="v9"
)

GH_TOKEN="${GITHUB_TOKEN:-}"
API_HDR=()
if [[ -n "$GH_TOKEN" ]]; then
  API_HDR=(-H "Authorization: token ${GH_TOKEN}")
fi

# Get final commit sha for owner/repo tag (handles annotated tag)
get_final_sha() {
  owner_repo="$1"
  tag="$2"
  echo "Resolving ${owner_repo}@${tag}..."
  # Query refs/tags/<tag>
  ref_json=$(curl -sS "${API_HDR[@]}" "https://api.github.com/repos/${owner_repo}/git/refs/tags/${tag}" || true)
  sha=$(echo "$ref_json" | grep -m1 '"sha"' | sed -E 's/.*"sha": *"([^"]+)".*/\1/' || true)
  # If we couldn't find via refs API, try tags list (fallback)
  if [[ -z "$sha" ]]; then
    echo "  refs API didn't return a sha; trying tags list..."
    sha=$(curl -sS "${API_HDR[@]}" "https://api.github.com/repos/${owner_repo}/tags" | grep -B2 "\"name\": \"${tag}\"" -A2 | grep '"sha"' | head -n1 | sed -E 's/.*"sha": *"([^"]+)".*/\1/' || true)
  fi
  if [[ -z "$sha" ]]; then
    echo "ERROR: could not resolve ${owner_repo}@${tag}" >&2
    return 1
  fi
  # If the ref pointed to a tag object (annotated tag), dereference to get commit sha
  # Check object type in ref_json
  obj_type=$(echo "$ref_json" | grep -m1 '"type"' | sed -E 's/.*"type": *"([^"]+)".*/\1/' || true)
  if [[ "$obj_type" == "tag" ]]; then
    # dereference tag object to get the underlying commit
    echo "  Tag appears annotated; dereferencing tag object ${sha}..."
    tag_json=$(curl -sS "${API_HDR[@]}" "https://api.github.com/repos/${owner_repo}/git/tags/${sha}" || true)
    commit_sha=$(echo "$tag_json" | grep -m1 '"sha"' | sed -E 's/.*"sha": *"([^"]+)".*/\1/' || true)
    if [[ -n "$commit_sha" ]]; then
      sha="$commit_sha"
    fi
  fi
  # Validate 40-hex
  if [[ ! "$sha" =~ ^[0-9a-f]{40}$ ]]; then
    # fallback: try git ls-remote
    echo "  Resolved sha is not 40-hex; trying git ls-remote fallback..."
    fallback=$(git ls-remote "https://github.com/${owner_repo}.git" "refs/tags/${tag}" 2>/dev/null | awk '{print $1}' | head -n1 || true)
    if [[ "$fallback" =~ ^[0-9a-f]{40}$ ]]; then
      sha="$fallback"
    fi
  fi
  if [[ ! "$sha" =~ ^[0-9a-f]{40}$ ]]; then
    echo "ERROR: final commit SHA for ${owner_repo}@${tag} could not be resolved to 40-hex." >&2
    return 1
  fi
  echo "$sha"
}

# Build replacements map
declare -A REPL
for key in "${!TARGET_TAGS[@]}"; do
  tag="${TARGET_TAGS[$key]}"
  sha="$(get_final_sha "$key" "$tag")" || exit 1
  REPL["${key}@${tag}"]="$sha"
done

echo "Replacement mapping:"
for k in "${!REPL[@]}"; do
  echo "  $k -> ${REPL[$k]}"
done

# Apply replacements in target files
for wf in "${WORKFLOW_FILES[@]}"; do
  if [[ ! -f "$wf" ]]; then
    echo "Skipping (not found): $wf"
    continue
  fi
  echo "Processing $wf ..."
  cp "$wf" "${wf}.bak"
  tmp="$(mktemp)"
  cp "$wf" "$tmp"

  # Remove any angle brackets around uses: values
  sed -i -E 's/uses:[[:space:]]*<([^>]+)>/uses: \1/g' "$tmp"

  # For each replacement, replace owner/repo@tag with owner/repo@<sha>
  for key in "${!REPL[@]}"; do
    owner_repo="${key%@*}"
    tag="${key#*@}"
    sha="${REPL[$key]}"
    # Replace occurrences: allow optional <>
    # Use perl for safe in-place, maintaining indentation
    perl -0777 -pe "s/(uses:\s*${owner_repo}@)<?${tag}>?/\\1${sha}/g" -i "$tmp"
  done

  # Save back only if changed
  if ! diff -q "$wf" "$tmp" >/dev/null 2>&1; then
    mv "$tmp" "$wf"
    echo "Updated $wf (backup at ${wf}.bak)"
  else
    rm -f "$tmp"
    echo "No changes for $wf"
  fi
done

echo "All done. Run 'git diff' to review changes. Backups saved with .bak extension."
