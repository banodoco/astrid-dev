#!/usr/bin/env bash
# Link Astrid development workflows and shared references locally.
# This installs only skills owned by this repository; it does not sync globally.

set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
SKILL_NAMES=(astrid-dev astrid-dev-plan astrid-dev-bugfix astrid-dev-iterate astrid-dev-release astrid-dev-shared)
OBSOLETE_NAMES=(astrid-dev-manage astrid-dev-work astrid-dev-advise)
TARGET_DIRS=()
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: sync.sh [--dry-run] [--destination SKILL_DIR ...]

Without --destination, links into existing ~/.claude/skills, ~/.codex/skills,
and ~/.agents/skills directories. Missing destination directories are reported
as incomplete; this script never creates them.

Use --destination to select one or more existing skill directories, for example:
  ./sync.sh --dry-run --destination "/tmp/codex fixture/skills"
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
retired=0

for target_dir in "${TARGET_DIRS[@]}"; do
  if [[ ! -d "$target_dir" ]]; then
    printf 'incomplete %s (destination directory missing; create it before syncing)\n' "$target_dir" >&2
    errors=$((errors + 1))
    continue
  fi

  # Retire only exact symlinks from old names to this repository's old folders.
  # Directories, regular files, and links to any other target are left untouched.
  for name in "${OBSOLETE_NAMES[@]}"; do
    old_src="$SKILLS_DIR/$name"
    dest="$target_dir/$name"
    if [[ -L "$dest" ]] && [[ "$(readlink "$dest")" == "$old_src" ]]; then
      if ((DRY_RUN)); then
        printf 'would-retire %s -> %s (obsolete repository-owned symlink)\n' "$dest" "$old_src"
      elif rm -- "$dest"; then
        printf 'retired %s (obsolete repository-owned symlink)\n' "$dest"
        retired=$((retired + 1))
      else
        printf 'incomplete %s (could not retire obsolete symlink)\n' "$dest" >&2
        errors=$((errors + 1))
      fi
    fi
  done

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

printf '\ndone: %s created, %s already linked, %s retired, %s incomplete/conflicting\n' "$created" "$skipped" "$retired" "$errors"
((errors == 0))
