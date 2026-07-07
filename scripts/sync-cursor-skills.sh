#!/usr/bin/env bash
# Sync canonical skills from this library into Cursor skill directories.
# Usage: ./scripts/sync-cursor-skills.sh [--scope project|global|both] [--force]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCOPE="both"
FORCE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)
      SCOPE="$2"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    -h | --help)
      echo "Usage: $0 [--scope project|global|both] [--force]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

declare -a TARGETS=()
case "$SCOPE" in
  project) TARGETS=("$REPO_ROOT/.cursor/skills") ;;
  global) TARGETS=("$HOME/.cursor/skills") ;;
  both) TARGETS=("$REPO_ROOT/.cursor/skills" "$HOME/.cursor/skills") ;;
  *)
    echo "Invalid scope: $SCOPE (use project, global, or both)" >&2
    exit 1
    ;;
esac

# Canonical skill source directories (relative to repo root).
# Prefer one source per skill; duplicates in vendor trees are intentionally omitted.
CANONICAL_PATHS=(
  # Taste / design direction
  front-end/taste-skill/skills/taste-skill
  front-end/taste-skill/skills/taste-skill-v1
  front-end/taste-skill/skills/redesign-skill
  front-end/taste-skill/skills/minimalist-skill
  front-end/taste-skill/skills/brutalist-skill
  front-end/taste-skill/skills/soft-skill
  front-end/taste-skill/skills/gpt-tasteskill
  front-end/taste-skill/skills/brandkit
  front-end/taste-skill/skills/image-to-code-skill
  front-end/taste-skill/skills/stitch-skill
  front-end/taste-skill/skills/imagegen-frontend-web
  front-end/taste-skill/skills/imagegen-frontend-mobile
  front-end/taste-skill/skills/output-skill
  # Motion
  front-end/skills/skills/emil-design-eng
  front-end/skills/skills/animation-vocabulary
  front-end/skills/skills/review-animations
  # Frontend quality
  front-end/impeccable/.cursor/skills/impeccable
  # UI/UX intelligence
  front-end/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max
  front-end/ui-ux-pro-max-skill/.claude/skills/design
  front-end/ui-ux-pro-max-skill/.claude/skills/design-system
  front-end/ui-ux-pro-max-skill/.claude/skills/brand
  front-end/ui-ux-pro-max-skill/.claude/skills/banner-design
  front-end/ui-ux-pro-max-skill/.claude/skills/ui-styling
  front-end/ui-ux-pro-max-skill/.claude/skills/slides
  # Components / specialized
  front-end/ui/skills/shadcn
  front-end/ui/skills/migrate-radix-to-base
  front-end/webgpu-claude-skill/skills/webgpu-threejs-tsl
  # InsForge
  back-end/InsForge/.agents/skills/insforge-dev
  back-end/InsForge/.agents/skills/insforge-dev/backend
  back-end/InsForge/.agents/skills/insforge-dev/dashboard
  back-end/InsForge/.agents/skills/insforge-dev/ui
  back-end/InsForge/.agents/skills/insforge-dev/shared-schemas
  back-end/InsForge/.agents/skills/insforge-dev/docs
  back-end/InsForge/.agents/skills/insforge-dev/e2e-testing
  # Caveman
  back-end/caveman/skills/caveman
  back-end/caveman/skills/caveman-compress
  back-end/caveman/skills/cavecrew
  back-end/caveman/skills/caveman-stats
  back-end/caveman/skills/caveman-help
  back-end/caveman/skills/caveman-review
  back-end/caveman/skills/caveman-commit
)

# Compound Engineering skills (dynamic)
while IFS= read -r skill_dir; do
  CANONICAL_PATHS+=("${skill_dir#"$REPO_ROOT"/}")
done < <(find "$REPO_ROOT/back-end/compound-engineering-plugin/skills" -mindepth 1 -maxdepth 1 -type d ! -path '*/.*' | sort)

get_skill_name() {
  local skill_md="$1"
  sed -n 's/^name:[[:space:]]*//p' "$skill_md" | head -1 | tr -d '"'"'"
}

linked=0
skipped=0

for rel_path in "${CANONICAL_PATHS[@]}"; do
  src="$REPO_ROOT/$rel_path"
  skill_md="$src/SKILL.md"

  if [[ ! -f "$skill_md" ]]; then
    echo "skip (missing SKILL.md): $rel_path" >&2
    skipped=$((skipped + 1))
    continue
  fi

  name="$(get_skill_name "$skill_md")"
  if [[ -z "$name" ]]; then
    echo "skip (no name): $rel_path" >&2
    skipped=$((skipped + 1))
    continue
  fi

  for target_root in "${TARGETS[@]}"; do
    mkdir -p "$target_root"
    dest="$target_root/$name"

    if [[ -e "$dest" && ! -L "$dest" ]]; then
      if [[ "$FORCE" == "true" ]]; then
        rm -rf "$dest"
      else
        echo "skip (real directory exists; use --force): $dest" >&2
        skipped=$((skipped + 1))
        continue
      fi
    fi

    link_target="$src"
    if [[ "$target_root" == "$REPO_ROOT/.cursor/skills" ]]; then
      link_target="$(python3 -c "import os.path; print(os.path.relpath('$src', '$target_root'))")"
    fi

    ln -sfn "$link_target" "$dest"
    linked=$((linked + 1))
  done

  echo "linked: $name -> $rel_path"
done

echo ""
echo "Done. Linked $linked skill paths (scope=$SCOPE). Skipped $skipped."
echo "Restart Cursor or reload the window so skill discovery picks up changes."
