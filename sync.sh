#!/usr/bin/env bash
# Link Astrid development workflows and shared references locally.
# This installs only folders owned by this repository; it does not sync globally.
#
# Install the entrypoint, shared references and packages from roles/ and shared/workstreams/.
# Each installed skill keeps its astrid-dev-* name, and a flat symlink in the
# destination, regardless of its source category. No duplicate skill copies.
# Links into skills/ whose folder no longer exists (renamed or removed skills)
# are retired. Nothing else in a destination is touched.

set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
TARGET_DIRS=()
EXPLICIT_TARGETS=0
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: sync.sh [--dry-run] [--destination SKILL_DIR ...]

Links the Astrid skill packages and shared references into each destination.

Without --destination, links into whichever of ~/.claude/skills,
~/.codex/skills and ~/.agents/skills exist, and skips the others. It fails
only if none exist. This script never creates them.

With --destination, each named directory must exist, for example:
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
      EXPLICIT_TARGETS=1
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
retargeted=0
synced_targets=0

# Collect the folders to link, checking each skill's declared name.
SOURCES=()
for src in "$SKILLS_DIR/astrid-dev" "$SKILLS_DIR/shared" "$SKILLS_DIR"/roles/astrid-dev-*/ "$SKILLS_DIR"/shared/workstreams/astrid-dev-*/; do
  src="${src%/}"
  [[ -d "$src" && ! -L "$src" ]] || continue
  name="$(basename -- "$src")"
  if [[ "$name" != "astrid-dev" && "$name" != "shared" && "$name" != astrid-dev-* ]]; then
    printf 'invalid installed package name %s (expected astrid-dev-*)\n' "$name" >&2
    errors=$((errors + 1))
    continue
  fi
  if [[ -f "$src/SKILL.md" ]]; then
    declared="$(sed -n '1{/^---$/!q};2,/^---$/{s/^name:[[:space:]]*//p}' "$src/SKILL.md" | head -n 1)"
    declared="${declared%"${declared##*[![:space:]]}"}"
    if [[ "$declared" != "$name" ]]; then
      printf 'invalid %s (SKILL.md name is "%s", expected "%s"; not linked)\n' "$src" "$declared" "$name" >&2
      errors=$((errors + 1))
      continue
    fi
  fi
  SOURCES+=("$src")
done

if ((${#SOURCES[@]} == 0)); then
  printf 'incomplete %s (no folders to link)\n' "$SKILLS_DIR" >&2
  exit 1
fi

for target_dir in "${TARGET_DIRS[@]}"; do
  if [[ ! -d "$target_dir" ]]; then
    if ((EXPLICIT_TARGETS)); then
      printf 'incomplete %s (destination directory missing; create it before syncing)\n' "$target_dir" >&2
      errors=$((errors + 1))
    else
      printf 'absent %s (not present; skipped)\n' "$target_dir"
    fi
    continue
  fi
  synced_targets=$((synced_targets + 1))

  # Retire links that point into this repository's skills/ at a folder that
  # no longer exists. Directories, files and other links are left untouched.
  for dest in "$target_dir"/*; do
    [[ -L "$dest" ]] || continue
    current="$(readlink "$dest")"
    [[ "$current" == "$SKILLS_DIR/"* ]] || continue
    [[ -d "$current" ]] && continue
    if ((DRY_RUN)); then
      printf 'would-retire %s -> %s (folder no longer in this repository)\n' "$dest" "$current"
    elif rm -- "$dest"; then
      printf 'retired %s (folder no longer in this repository)\n' "$dest"
      retired=$((retired + 1))
    else
      printf 'incomplete %s (could not retire stale symlink)\n' "$dest" >&2
      errors=$((errors + 1))
    fi
  done

  for src in "${SOURCES[@]}"; do
    name="$(basename -- "$src")"
    dest="$target_dir/$name"

    if [[ -L "$dest" ]]; then
      current="$(readlink "$dest")"
      if [[ "$current" == "$src" ]]; then
        printf 'skip   %s (already linked)\n' "$dest"
        skipped=$((skipped + 1))
      else
        # Move only links installed by this repository's earlier layout.
        # Legacy paths are preserved as directory symlinks for historical docs,
        # but installed skill links should point at the canonical package.
        legacy=""
        if [[ "$src" == "$SKILLS_DIR/shared/workstreams/"* ]]; then
          if [[ "$name" == "astrid-dev-plan" ]]; then
            legacy="$SKILLS_DIR/roles/$name"
          else
            legacy="$SKILLS_DIR/capabilities/$name"
          fi
        fi
        if [[ -n "$legacy" && "$current" == "$legacy" && -L "$legacy" && -d "$legacy" ]]; then
          if ((DRY_RUN)); then
            printf 'would-retarget %s -> %s (legacy %s)\n' "$dest" "$src" "$legacy"
          elif ln -sfn -- "$src" "$dest"; then
            printf 'retargeted %s -> %s\n' "$dest" "$src"
            retargeted=$((retargeted + 1))
          else
            printf 'incomplete %s (could not retarget legacy link)\n' "$dest" >&2
            errors=$((errors + 1))
          fi
        else
          printf 'conflict %s -> %s (foreign symlink; leaving untouched)\n' "$dest" "$current" >&2
          errors=$((errors + 1))
        fi
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

if ((synced_targets == 0 && !EXPLICIT_TARGETS)); then
  printf 'incomplete (none of the default destinations exist; create one or pass --destination)\n' >&2
  errors=$((errors + 1))
fi

printf '\ndone: %s created, %s already linked, %s retargeted, %s retired, %s incomplete/conflicting/invalid\n' "$created" "$skipped" "$retargeted" "$retired" "$errors"
((errors == 0))
