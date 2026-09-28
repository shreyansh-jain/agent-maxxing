#!/usr/bin/env python3
"""Validate every skill in skills/ and the marketplace against docs/SKILL-STANDARD.md.

Usage: python3 scripts/validate_skills.py [--strict]
  --strict  treat warnings as errors
Exit code 0 when clean, 1 when any error (or warning under --strict).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REQUIRED_METADATA = {"version", "category", "sources"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
RESERVED = ("claude", "anthropic")

DESCRIPTION_TARGET = 500
DESCRIPTION_MAX = 1024
BUNDLE_DESCRIPTION_BUDGET = 8000
BUNDLES = {"swe-all", "swe-core"}
BODY_WORDS_TARGET = 1500
BODY_LINES_MAX = 500
MIN_EVALS = 3
MIN_TRIGGERS_EACH = 6


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, where, msg):
        self.errors.append(f"ERROR  {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"WARN   {where}: {msg}")


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text, where, report):
    """Parse the portable subset: `key: value` lines plus one nested `metadata:` map."""
    if not text.startswith("---\n"):
        report.error(where, "SKILL.md must start with '---' frontmatter")
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        report.error(where, "frontmatter is not closed with '---'")
        return None, text
    block, body = text[4:end], text[end + 5:]
    data, current_map = {}, None
    for lineno, line in enumerate(block.splitlines(), start=2):
        if not line.strip():
            continue
        if line.startswith("  "):
            if current_map is None:
                report.error(where, f"line {lineno}: indented line outside a map")
                continue
            key, sep, value = line.strip().partition(":")
            if not sep or not value.strip():
                report.error(where, f"line {lineno}: metadata entries must be 'key: \"value\"'")
                continue
            if not (value.strip().startswith('"') or value.strip().startswith("'")):
                report.error(where, f"line {lineno}: metadata value for '{key}' must be a quoted string")
            current_map[key.strip()] = unquote(value)
            continue
        key, sep, value = line.partition(":")
        if not sep:
            report.error(where, f"line {lineno}: expected 'key: value'")
            continue
        key, value = key.strip(), value.strip()
        if value in ("|", ">", "|-", ">-") or value.startswith("["):
            report.error(where, f"line {lineno}: '{key}' must be a single-line scalar (no block scalars or lists)")
        if value == "":
            data[key] = current_map = {}
        else:
            data[key] = unquote(value)
            current_map = None
    return data, body


def check_skill(skill_dir, report, seen_names):
    where = f"skills/{skill_dir.name}"
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        report.error(where, "missing SKILL.md")
        return None
    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text, where, report)
    if fm is None:
        return None

    for key in fm:
        if key not in ALLOWED_KEYS:
            report.error(where, f"frontmatter key '{key}' is not in the Agent Skills spec (breaks claude.ai / API uploads)")

    name = fm.get("name", "")
    if not name:
        report.error(where, "missing 'name'")
    else:
        if not NAME_RE.match(name) or len(name) > 64:
            report.error(where, f"name '{name}' must match {NAME_RE.pattern} and be <=64 chars")
        if name != skill_dir.name:
            report.error(where, f"name '{name}' must equal directory name '{skill_dir.name}'")
        if any(r in name for r in RESERVED):
            report.error(where, f"name '{name}' contains a reserved word {RESERVED}")
        if name in seen_names:
            report.error(where, f"duplicate skill name '{name}'")
        seen_names.add(name)

    desc = fm.get("description", "")
    if not isinstance(desc, str) or not desc:
        report.error(where, "missing 'description'")
    else:
        if len(desc) > DESCRIPTION_MAX:
            report.error(where, f"description is {len(desc)} chars (max {DESCRIPTION_MAX})")
        elif len(desc) > DESCRIPTION_TARGET:
            report.warn(where, f"description is {len(desc)} chars (target <= {DESCRIPTION_TARGET})")
        if "Use when" not in desc:
            report.error(where, "description must contain a 'Use when ...' trigger clause")
        if re.search(r"\b(I|me|my|you|your)\b", desc):
            report.warn(where, "description should be third person")
        if "<" in desc and ">" in desc:
            report.error(where, "description must not contain XML-like tags")

    if fm.get("license") != "Apache-2.0":
        report.warn(where, "license should be 'Apache-2.0' for skills authored here")

    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        report.error(where, "missing 'metadata' map")
        meta = {}
    for key in REQUIRED_METADATA - set(meta):
        report.error(where, f"metadata.{key} is required")
    if meta.get("version") and not SEMVER_RE.match(meta["version"]):
        report.error(where, f"metadata.version '{meta['version']}' is not semver")

    lines = body.splitlines()
    words = len(body.split())
    if len(lines) > BODY_LINES_MAX:
        report.error(where, f"body is {len(lines)} lines (max {BODY_LINES_MAX}); move detail to references/")
    if words > BODY_WORDS_TARGET:
        report.warn(where, f"body is {words} words (target <= {BODY_WORDS_TARGET})")
    if not re.search(r"^# ", body, re.M):
        report.error(where, "body needs a '# Title'")
    if "## When to use" not in body:
        report.error(where, "body needs a '## When to use' section")
    if "**Not for:**" not in body:
        report.warn(where, "'## When to use' should name sibling skills under '**Not for:**'")
    if "@" in re.sub(r"`[^`]*`", "", body) and re.search(r"(^|\s)@[\w./-]+\.md", body):
        report.error(where, "do not force-load files with @path; link them instead")

    for md in [skill_md, *sorted((skill_dir / "references").glob("*.md"))]:
        content = md.read_text(encoding="utf-8")
        for target in LINK_RE.findall(content):
            if re.match(r"^[a-z]+:", target):
                continue
            if not (md.parent / target).exists():
                report.error(f"{where}/{md.relative_to(skill_dir)}", f"broken relative link '{target}'")
        if md.parent.name == "references" and len(content.splitlines()) > 100 and "## Contents" not in content:
            report.warn(f"{where}/{md.relative_to(skill_dir)}", "reference over 100 lines should start with '## Contents'")

    check_evals(skill_dir, name, where, report)
    return {"name": name, "category": meta.get("category", ""), "description": desc}


def load_json(path, where, report):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(where, f"missing {path.name}")
    except json.JSONDecodeError as exc:
        report.error(where, f"{path.name} is not valid JSON: {exc}")
    return None


def check_evals(skill_dir, name, where, report):
    evals = load_json(skill_dir / "evals" / "evals.json", where, report)
    if evals is not None:
        if evals.get("skill_name") != name:
            report.error(where, "evals.json skill_name must equal the skill name")
        items = evals.get("evals", [])
        if len(items) < MIN_EVALS:
            report.error(where, f"evals.json needs >= {MIN_EVALS} evals (has {len(items)})")
        ids = set()
        for item in items:
            missing = {"id", "prompt", "expected_output", "expectations"} - set(item)
            if missing:
                report.error(where, f"eval {item.get('id', '?')} missing {sorted(missing)}")
            if item.get("id") in ids:
                report.error(where, f"duplicate eval id {item.get('id')}")
            ids.add(item.get("id"))
            if not item.get("expectations"):
                report.error(where, f"eval {item.get('id', '?')} needs at least one expectation")

    triggers = load_json(skill_dir / "evals" / "triggers.json", where, report)
    if triggers is not None:
        if not isinstance(triggers, list):
            report.error(where, "triggers.json must be a JSON array")
            return
        pos = sum(1 for t in triggers if t.get("should_trigger") is True)
        neg = sum(1 for t in triggers if t.get("should_trigger") is False)
        if pos < MIN_TRIGGERS_EACH or neg < MIN_TRIGGERS_EACH:
            report.error(where, f"triggers.json needs >= {MIN_TRIGGERS_EACH} true and false queries (has {pos}/{neg})")
        if any(not t.get("query") for t in triggers):
            report.error(where, "every trigger needs a non-empty 'query'")


def check_marketplace(skills, report):
    where = ".claude-plugin/marketplace.json"
    data = load_json(MARKETPLACE, where, report)
    if data is None:
        return
    for key in ("name", "owner", "plugins"):
        if key not in data:
            report.error(where, f"missing top-level '{key}'")
    by_name = {s["name"]: s for s in skills}
    in_category_plugin = {}
    plugin_names = set()
    for plugin in data.get("plugins", []):
        pname = plugin.get("name", "?")
        if pname in plugin_names:
            report.error(where, f"duplicate plugin '{pname}'")
        plugin_names.add(pname)
        if not NAME_RE.match(pname):
            report.error(where, f"plugin name '{pname}' must be kebab-case")
        for key in ("source", "description"):
            if key not in plugin:
                report.error(where, f"plugin '{pname}' missing '{key}'")
        for path in plugin.get("skills", []):
            skill_name = Path(path).name
            if not (ROOT / path).joinpath("SKILL.md").is_file():
                report.error(where, f"plugin '{pname}' lists '{path}' which has no SKILL.md")
                continue
            if pname not in BUNDLES:
                if skill_name in in_category_plugin:
                    report.error(where, f"skill '{skill_name}' is in both '{in_category_plugin[skill_name]}' and '{pname}'")
                in_category_plugin[skill_name] = pname
                expected = f"swe-{by_name.get(skill_name, {}).get('category', '')}"
                if skill_name in by_name and pname != expected:
                    report.error(where, f"skill '{skill_name}' has category '{by_name[skill_name]['category']}' but sits in plugin '{pname}'")
    for plugin in data.get("plugins", []):
        chars = sum(len(by_name.get(Path(p).name, {}).get("description", "")) for p in plugin.get("skills", []))
        if plugin.get("name") != "swe-all" and chars > BUNDLE_DESCRIPTION_BUDGET:
            report.warn(where, f"plugin '{plugin.get('name')}' descriptions total {chars} chars (> {BUNDLE_DESCRIPTION_BUDGET}); risks silent catalog truncation")
    all_plugin = next((p for p in data.get("plugins", []) if p.get("name") == "swe-all"), None)
    all_listed = {Path(p).name for p in (all_plugin or {}).get("skills", [])}
    for name in by_name:
        if name not in in_category_plugin:
            report.error(where, f"skill '{name}' is not in any category plugin")
        if all_plugin is not None and name not in all_listed:
            report.error(where, f"skill '{name}' is missing from 'swe-all'")
    if all_plugin is None:
        report.error(where, "missing the 'swe-all' plugin")


def main():
    strict = "--strict" in sys.argv[1:]
    report, seen, skills = Report(), set(), []
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.is_dir() else []
    if not dirs:
        report.error("skills/", "no skills found")
    for skill_dir in dirs:
        result = check_skill(skill_dir, report, seen)
        if result:
            skills.append(result)
    check_marketplace(skills, report)
    total_desc = sum(len(s["description"]) for s in skills)

    for line in report.errors + report.warnings:
        print(line)
    print(f"\n{len(skills)} skills, {len(report.errors)} errors, {len(report.warnings)} warnings, "
          f"{total_desc} description chars total")
    failed = report.errors or (strict and report.warnings)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
