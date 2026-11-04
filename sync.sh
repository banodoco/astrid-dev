#!/usr/bin/env bash
# Link this repository's portable Astrid development skills into local skill dirs.
# The missing-only symlink behavior is adapted from poms_skills/sync.sh.
# This script does not manage global instructions or perform cloud/remote sync.

set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
SKILL_NAMES=(
  astrid-dev-plan
  astrid-dev-manage
  astrid-dev-work
  astrid-dev-advise
  astrid-dev-release
  astrid-dev-shared
)
TARGET_DIRS=()
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: sync.sh [--dry-run] [--destination SKILL_DIR ...]

Without --destination, links into existing ~/.claude/skills, ~/.codex/skills,
and ~/.agents/skills directories. Missing destination directories are reported
as incomplete; this script never creates them.

Use --destination to select one or more existing skill directories, for example:
  ./sync.sh --dry-run --destination /tmp/codex-fixture/skills
USAGE
}

while (($#)); do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --destination)
      if (($# < 2)) || [[ -z "$2" ]]; then
        echo "error: --destination requires a directory path" >&2
        usage >&2
        exit 2
      fi
      TARGET_DIRS+=("$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ((${#TARGET_DIRS[@]} == 0)); then
  TARGET_DIRS=(
    "${HOME:?HOME must be set}/.claude/skills"
    "${HOME:?HOME must be set}/.codex/skills"
    "${HOME:?HOME must be set}/.agents/skills"
  )
fi

errors=0
created=0
skipped=0

for target_dir in "${TARGET_DIRS[@]}"; do
  if [[ ! -d "$target_dir" ]]; then
    printf 'incomplete %s (destination directory missing; create it before syncing)\n' "$target_dir" >&2
    errors=$((errors + 1))
    continue
  fi

  for name in "${SKILL_NAMES[@]}"; do
    src="$SKILLS_DIR/$name"
    dest="$target_dir/$name"

    if [[ ! -d "$src" ]]; then
      printf 'incomplete %s (source skill directory missing)\n' "$src" >&2
      errors=$((errors + 1))
      continue
    fi

    if [[ -L "$dest" ]]; then
      current="$(readlink "$dest")"
      if [[ "$current" == "$src" ]]; then
        printf 'skip   %s (already linked)\n' "$dest"
        skipped=$((skipped + 1))
      else
        printf 'conflict %s -> %s (foreign symlink; leaving untouched)\n' "$dest" "$current" >&2
        errors=$((errors + 1))
      fi
    elif [[ -e "$dest" ]]; then
      printf 'conflict %s (entry exists and is not the expected symlink; leaving untouched)\n' "$dest" >&2
      errors=$((errors + 1))
    elif ((DRY_RUN)); then
      printf 'would-link %s -> %s\n' "$dest" "$src"
    elif ln -s "$src" "$dest"; then
      printf 'linked %s -> %s\n' "$dest" "$src"
      created=$((created + 1))
    else
      printf 'incomplete %s (could not create symlink)\n' "$dest" >&2
      errors=$((errors + 1))
    fi
  done
done

printf '\ndone: %s created, %s already linked, %s incomplete/conflicting\n' "$created" "$skipped" "$errors"
((errors == 0))
