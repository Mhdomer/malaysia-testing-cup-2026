---
name: mtc-evaluator
description: Use during the Malaysia Testing Cup 2026 competition to execute structured SQA reconnaissance, timeboxed deliverable drafting, boundary value fuzzing, non-functional security audits, and ISTQB defect formatting.
---

# Malaysia Testing Cup 2026 Evaluator & QA Lead Skill

This skill governs the end-to-end evaluation, testing execution, and deliverable production for Team NERV in the Malaysia Testing Cup.

## 1. Architectural Roles & Multi-Agent Swarm
- **Omar (Field Operator):** Operates Chromium, inspects visual UI behaviors, analyzes DevTools Network payloads, triggers Satty (`Mod+Shift+S`) for defect screenshots, and submits deliverables into the MSTB portal.
- **Antigravity (Mission Control / QA Lead):** Drives the master 3.5-hour clock, oversees the 130-point matrix, coordinates background subagents, performs final deliverable quality control, and ensures zero hallucinations.
- **Subagents (`invoke_subagent`):**
  - **`recon_scout` (Agent Alpha):** Runs `scripts/battle_runner.py`, extracts DOM inputs, Axe-core WCAG violations, and writes Deliverable 5 (Non-Functional Report).
  - **`matrix_architect` (Agent Bravo):** Ingests DOM architecture, designs EP/BVA matrices, drafts Deliverable 1 (Test Plan), Deliverable 2 (Test Design), and Deliverable 3 (Test Cases).
  - **`offensive_hunter` (Agent Charlie):** Applies `Claude-Red` attack playbooks (business logic, IDOR, JWT, race conditions), generates boundary fuzz vectors, structures Deliverable 4 Bug Reports, and isolates the Bonus 2 Golden Bug.

## 2. Phase-by-Phase Battle Workflow

### Phase 1: Reconnaissance & Multi-Agent Launch (00:00 - 00:20)
1. Omar provides target URL to Mission Control.
2. Mission Control invokes `recon_scout` and runs automated parallel recon:
   ```bash
   python3 scripts/battle_runner.py "<URL>"
   ```
3. Recon artifacts saved to `evidence/recon_summary.json`.
4. Mission Control dispatches `matrix_architect` to draft Deliverable 1 (`deliverables/01_test_plan.md`).
5. Mission Control prompts Omar to verify and submit Deliverable 1.

### Phase 2: Analysis & Design Matrix (00:20 - 00:45)
1. `matrix_architect` builds Equivalence Partitions, Boundary Values, and State Transition models.
2. Populates `deliverables/02_test_analysis_design.md`.
3. Omar submits Deliverable 2 into the platform.

### Phase 3: Test Implementation (00:45 - 01:05)
1. `matrix_architect` details formal test cases with exact inputs, preconditions, and expected outcomes.
2. Populates `deliverables/03_test_implementation.md`.
3. Omar submits Deliverable 3 into the platform.

### Phase 4 & 5: Deep Testing, Non-Functional Audit & Golden Bug Hunt (01:05 - 02:15)
1. **Parallel Execution:**
   - **Omar:** Executes manual interactive workflows in Chromium, intercepts network calls, flags weird behavior.
   - **`recon_scout`:** Finalizes `deliverables/05_non_functional_report.md` (WCAG violations, security headers, CORS, performance TTFB/LCP).
   - **`offensive_hunter`:** Tests high-severity logic boundaries using `python3 scripts/fuzz_gen.py --type bva --len <N> --copy`, checks JWT signature stripping, and probes for IDOR/race conditions.
2. Verified defects are documented in `deliverables/04_bug_reports/DEF-00X.md` with reproduction steps, payloads, and Satty screenshots.
3. Omar submits Deliverable 4 and Deliverable 5.

### Phase 6: Executive Summary Test Report (02:15 - 02:45)
1. Mission Control synthesizes defect counts, severity metrics, and risk heatmaps.
2. Formulates objective stakeholder release recommendation (Go / No-Go).
3. Populates `deliverables/06_summary_test_report.md`.
4. Omar submits Deliverable 6.

### Buffer & Final Verification (02:45 - 03:00)
1. Verify all image attachments are valid PNG/JPG format under 16 MB.
2. Verify all 6 deliverables plus Bonus sections are submitted on the MSTB portal.

