#!/usr/bin/env bash
# Symlink skills from this repo into an agent's skills directory.
#
# Usage:
#   bash scripts/install.sh [--target DIR] [--plugin NAME]... [--category NAME]... [--skill NAME]... [--copy] [--dry-run]
#
# Targets (default: ~/.agents/skills, read by Codex, Gemini CLI, Copilot, Cursor, OpenCode):
#   --target ~/.claude/skills      Claude Code, personal
#   --target .claude/skills        Claude Code, this project
#   --target .agents/skills        cross-tool, this project
# --plugin swe-core installs the default set; --plugin takes any name from .claude-plugin/marketplace.json.
# With no --plugin/--category/--skill, installs every skill.
# Existing entries with the same name are left untouched unless they are symlinks into this repo.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
target="$HOME/.agents/skills"
mode=link
dry=0
categories=()
skills=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target) target="$2"; shift 2 ;;
    --category) categories+=("$2"); shift 2 ;;
    --skill) skills+=("$2"); shift 2 ;;
    --plugin)
      members="$(python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); p=[x for x in m["plugins"] if x["name"]==sys.argv[2]]; sys.exit("unknown plugin: "+sys.argv[2]) if not p else print("\n".join(s.rsplit("/",1)[-1] for s in p[0]["skills"]))' "$repo/.claude-plugin/marketplace.json" "$2")" || exit 2
      while IFS= read -r m; do skills+=("$m"); done <<<"$members"
      shift 2 ;;
    --copy) mode=copy; shift ;;
    --dry-run) dry=1; shift ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

category_of() {
  sed -n 's/^  category: *"\{0,1\}\([a-z-]*\)"\{0,1\}$/\1/p' "$1/SKILL.md" | head -n 1
}

selected=()
for dir in "$repo"/skills/*/; do
  dir="${dir%/}"
  name="$(basename "$dir")"
  [ -f "$dir/SKILL.md" ] || continue
  if [ "${#categories[@]}" -eq 0 ] && [ "${#skills[@]}" -eq 0 ]; then
    selected+=("$dir"); continue
  fi
  for s in "${skills[@]}"; do [ "$s" = "$name" ] && selected+=("$dir") && continue 2; done
  cat="$(category_of "$dir")"
  for c in "${categories[@]}"; do [ "$c" = "$cat" ] && selected+=("$dir") && continue 2; done
done

if [ "${#selected[@]}" -eq 0 ]; then
  echo "no skills matched" >&2
  exit 1
fi

[ "$dry" -eq 1 ] || mkdir -p "$target"
installed=0
for dir in "${selected[@]}"; do
  name="$(basename "$dir")"
  dest="$target/$name"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$dir" ]; then
      echo "ok       $name (already linked)"; continue
    fi
    echo "skip     $name ($dest exists and is not ours)"; continue
  fi
  if [ "$dry" -eq 1 ]; then
    echo "would $mode $name -> $dest"; continue
  fi
  if [ "$mode" = copy ]; then cp -R "$dir" "$dest"; else ln -s "$dir" "$dest"; fi
  echo "$mode     $name"
  installed=$((installed + 1))
done
echo "$installed installed into $target"
