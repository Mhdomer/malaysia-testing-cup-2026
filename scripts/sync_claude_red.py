#!/usr/bin/env python3
"""
Sync and port Claude-Red offensive security skills into Antigravity workspace skills.
Enforces:
1. Valid YAML frontmatter (name, description)
2. Zero em dashes (replaces '—' and '–' with colons, commas, or standard hyphens)
3. Curated deployment to .agents/skills/ for MTC 2026
"""

import os
import glob
import re
import json
import shutil
from pathlib import Path

WORKSPACE_ROOT = Path("/mnt/data/Projects/malaysia-testing-cup-2026")
CLAUDE_RED_DIR = WORKSPACE_ROOT / "references" / "claude-red"
SKILLS_SRC_DIR = CLAUDE_RED_DIR / "Skills"
MANIFEST_PATH = CLAUDE_RED_DIR / "claude-skills.json"
TARGET_AGENTS_SKILLS = WORKSPACE_ROOT / ".agents" / "skills"

# High-priority skills for Malaysia Testing Cup 2026 & Web/API DevSecOps
CURATED_SKILLS = [
    "offensive-business-logic",
    "offensive-idor",
    "offensive-jwt",
    "offensive-oauth",
    "offensive-api-security",
    "offensive-api-abuse",
    "offensive-graphql",
    "offensive-race-condition",
    "offensive-parameter-pollution",
    "offensive-fast-checking",
    "offensive-reporting",
    "offensive-sqli",
    "offensive-xss",
    "offensive-ssrf",
    "offensive-file-upload",
    "offensive-ai-security"
]

def sanitize_text(text: str) -> str:
    """Removes em dashes and en dashes to enforce project zero em dash rule."""
    text = text.replace(" — ", ": ")
    text = text.replace("—", ": ")
    text = text.replace(" – ", " - ")
    text = text.replace("–", "- ")
    return text

def parse_skill_file(file_path: Path, manifest_desc: dict) -> tuple[str, str, str]:
    """Extracts name, description, and body from SKILL.md."""
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    skill_name = file_path.parent.name
    
    # Check if already has YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2].lstrip()
            # Extract name and description from existing frontmatter
            m_name = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
            m_desc = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
            name = m_name.group(1).strip().strip('"\'') if m_name else skill_name
            desc = m_desc.group(1).strip().strip('"\'') if m_desc else manifest_desc.get(name, "")
            return name, sanitize_text(desc), sanitize_text(body)

    # Format without YAML: parse ## Metadata or ## Description
    desc = manifest_desc.get(skill_name, "")
    if not desc:
        m_desc = re.search(r"## Description\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
        if m_desc:
            desc = " ".join(line.strip() for line in m_desc.group(1).splitlines() if line.strip())

    if not desc:
        desc = f"Offensive security testing checklist and methodology for {skill_name}."

    # Body without legacy metadata headers
    m_body = re.search(r"(## Full Methodology.*)", content, re.DOTALL)
    if m_body:
        body = m_body.group(1)
    else:
        # Strip the top title and metadata if possible
        lines = content.splitlines()
        body_lines = []
        skip = True
        for line in lines:
            if line.startswith("## Full Methodology") or line.startswith("---"):
                skip = False
                continue
            if not skip:
                body_lines.append(line)
        body = "\n".join(body_lines) if body_lines else content

    return skill_name, sanitize_text(desc), sanitize_text(body)

def main():
    if not CLAUDE_RED_DIR.exists():
        print(f"Error: {CLAUDE_RED_DIR} does not exist.")
        return

    manifest_desc = {}
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            manifest_desc = {s["name"]: s.get("description", "") for s in manifest.get("skills", [])}

    all_skill_files = list(SKILLS_SRC_DIR.glob("**/SKILL.md"))
    print(f"Found {len(all_skill_files)} total skills in Claude-Red.")

    index_entries = []

    # 1. Process all skills in references/claude-red/Skills (ensure YAML frontmatter & zero em dashes)
    for sfile in all_skill_files:
        category = sfile.parent.parent.name
        name, desc, body = parse_skill_file(sfile, manifest_desc)
        
        # Build normalized content
        normalized_content = f"""---
name: {name}
description: "{desc.replace('\"', '\\\"')}"
---

{body}
"""
        sfile.write_text(normalized_content, encoding="utf-8")
        index_entries.append({
            "name": name,
            "category": category,
            "path": str(sfile.relative_to(WORKSPACE_ROOT)),
            "description": desc
        })

    # 2. Deploy curated skills to .agents/skills/
    TARGET_AGENTS_SKILLS.mkdir(parents=True, exist_ok=True)
    curated_deployed = 0

    for sname in CURATED_SKILLS:
        matches = list(SKILLS_SRC_DIR.glob(f"**/{sname}/SKILL.md"))
        if not matches:
            print(f"Warning: Curated skill not found: {sname}")
            continue
        
        src_file = matches[0]
        dest_dir = TARGET_AGENTS_SKILLS / sname
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "SKILL.md"
        
        shutil.copy2(src_file, dest_file)
        curated_deployed += 1
        print(f"Deployed curated skill to .agents/skills/{sname}/SKILL.md")

    # 3. Write comprehensive master index in references/claude-red/INDEX.md
    index_file = CLAUDE_RED_DIR / "INDEX.md"
    index_md = [
        "# Claude-Red Offensive Skills Index",
        "",
        "Complete offline reference library of 79 offensive security skills ported for Antigravity.",
        "",
        f"**Active Workspace Skills ({curated_deployed} Curated for MTC 2026):**",
        ""
    ]
    for sname in CURATED_SKILLS:
        index_md.append(f"- **`{sname}`**: Installed in `.agents/skills/{sname}/SKILL.md`")

    index_md.extend([
        "",
        "---",
        "",
        "## Full Category Breakdown",
        ""
    ])

    categories = sorted(list(set(e["category"] for e in index_entries)))
    for cat in categories:
        index_md.append(f"### {cat.title()}")
        cat_skills = [e for e in index_entries if e["category"] == cat]
        for s in cat_skills:
            index_md.append(f"- **`{s['name']}`**: {s['description'][:120]}... ([view](file:///{WORKSPACE_ROOT}/{s['path']}))")
        index_md.append("")

    index_file.write_text("\n".join(index_md), encoding="utf-8")
    print(f"\nSuccessfully generated master index at {index_file}")
    print(f"Total curated skills deployed: {curated_deployed}")

if __name__ == "__main__":
    main()
