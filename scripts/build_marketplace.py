#!/usr/bin/env python3
"""Regenerate .claude-plugin/marketplace.json from each skill's metadata.category.

Usage: python3 scripts/build_marketplace.py [--check]
  --check  exit 1 if the file on disk differs from what would be generated
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".claude-plugin" / "marketplace.json"

VERSION = "0.2.0"

CATEGORIES = {
    "lead": "Principal-engineer triage and leadership: complexity assessment, end-to-end product playbook, technical debt.",
    "product": "Product engineering: scoping the smallest valuable increment and measuring outcomes.",
    "define": "Clarify intent and write specs before any code.",
    "architect": "System architecture, capacity, domain and data modeling, resilience, threat modeling, privacy, design docs.",
    "plan": "Turn specs into reviewable implementation plans and pressure-test them.",
    "build": "Implementation: incremental delivery, TDD, test strategy, E2E, accessibility, LLM features, interfaces, refactoring.",
    "debug": "Root-cause debugging, flaky-test triage, and evidence before claiming done.",
    "review": "Multi-axis code review, receiving review feedback, and security audits.",
    "operate": "Production: performance, safe database migrations, observability, incidents, cloud cost.",
    "ship": "Delivery: git, CI pipelines and fixes, infrastructure as code, feature flags, dependency upgrades, shipping.",
    "docs": "Decision records, release docs, and agent context files (AGENTS.md / CLAUDE.md).",
    "agents": "Working with agents: dispatching subagents, session handoffs, authoring and evaluating skills.",
}

# The default install: the skills used on most engineering tasks, kept under an 8,000-character
# description budget so it fits every runtime's startup skill catalog.
CORE = [
    "assessing-complexity",
    "clarifying-intent",
    "writing-specs",
    "planning-implementation",
    "implementing-incrementally",
    "test-driven-development",
    "debugging-systematically",
    "verifying-before-completion",
    "reviewing-code",
    "receiving-code-review",
    "simplifying-code",
    "grounding-in-official-docs",
    "onboarding-to-codebases",
    "fixing-ci-failures",
    "writing-commits-and-prs",
    "shipping-changes",
    "dispatching-subagents",
    "auditing-security",
]

CATEGORY_RE = re.compile(r'^  category: "([a-z-]+)"$', re.M)


def discover():
    skills = {}
    for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
        match = CATEGORY_RE.search(skill_md.read_text(encoding="utf-8"))
        category = match.group(1) if match else ""
        if category not in CATEGORIES:
            sys.exit(f"{skill_md.parent.name}: category '{category}' is not one of {sorted(CATEGORIES)}")
        skills[skill_md.parent.name] = category
    missing = [name for name in CORE if name not in skills]
    if missing:
        sys.exit(f"CORE lists skills that do not exist: {missing}")
    return skills


def plugin(name, description, skill_names):
    return {
        "name": name,
        "description": description,
        "source": "./",
        "strict": False,
        "category": "development",
        "skills": [f"./skills/{s}" for s in skill_names],
    }


def build(skills):
    plugins = [
        plugin("swe-core", "The default set: the skills used on most engineering tasks, from triage to shipping.", CORE),
        plugin("swe-all", "Every skill in this marketplace, covering the full product-engineering lifecycle.", sorted(skills)),
    ]
    for category, description in CATEGORIES.items():
        members = sorted(s for s, c in skills.items() if c == category)
        if members:
            plugins.append(plugin(f"swe-{category}", description, members))
    return {
        "name": "skills-map",
        "owner": {"name": "Shreyansh Jain"},
        "metadata": {
            "description": "Principal-grade software and product engineering Agent Skills, synthesized from the best open-source skill collections.",
            "version": VERSION,
        },
        "plugins": plugins,
    }


def main():
    rendered = json.dumps(build(discover()), indent=2) + "\n"
    if "--check" in sys.argv[1:]:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != rendered:
            print("marketplace.json is stale; run: python3 scripts/build_marketplace.py")
            sys.exit(1)
        print("marketplace.json is up to date")
        return
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
