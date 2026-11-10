---
name: mtc-evaluator
description: Use during the Malaysia Testing Cup 2026 competition to execute structured SQA reconnaissance, timeboxed deliverable drafting, boundary value fuzzing, non-functional security audits, and ISTQB defect formatting.
---

# Malaysia Testing Cup 2026 Evaluator & QA Lead Skill

This skill governs the end-to-end evaluation, testing execution, and deliverable production for Team NERV in the Malaysia Testing Cup.

## 1. Architectural Roles
- **Omar (Field Operator):** Operates Chromium, inspects visual UI behaviors, triggers Satty (`Mod+Shift+S`) for visual defect capture, and pastes submissions into the MSTB portal.
- **Antigravity (QA Lead & Driver):** Enforces the 3-hour schedule, analyzes API responses and architecture, generates test data, drafts ISTQB deliverables, and writes high-fidelity defect reports.

## 2. Phase-by-Phase Workflow

### Phase 1: Reconnaissance & Test Plan (00:00 - 00:20)
1. Receive target URL from Omar.
2. Run automated crawler and security probe:
   ```bash
   node scripts/crawler.js "<URL>"
   python3 scripts/security_probe.py "<URL>"
   ```
3. Identify core modules, tech stack (via Wappalyzer / server headers), and risk profile.
4. Populate `deliverables/01_test_plan.md` using the ISO 29119-3 template from `TOOLKIT.md`.
5. Instruct Omar to submit Deliverable 1 into the platform.

### Phase 2: Analysis & Design (00:20 - 00:45)
1. Map test conditions per module (Equivalence Partitioning, Boundary Value Analysis, State Transitions).
2. Populate `deliverables/02_test_analysis_design.md`.
3. Instruct Omar to submit Deliverable 2 into the platform.

### Phase 3: Implementation (00:45 - 01:05)
1. Convert conditions into structured test cases with preconditions, test data, and expected outcomes.
2. Populate `deliverables/03_test_implementation.md`.
3. Instruct Omar to submit Deliverable 3 into the platform.

### Phase 4 & 5: Deep Testing & Non-Functional Audit (01:05 - 02:15)
1. **Functional Defect Hunting:**
   - Test boundary limits using `python3 scripts/fuzz_gen.py --type bva --len <N> --copy`.
   - Test race conditions (rapid double click, concurrent checkout).
   - Format each verified bug into `deliverables/04_bug_reports/DEF-00X.md`.
2. **Non-Functional Testing (20 Points):**
   - Run automated accessibility scan:
     ```bash
     node scripts/audit_accessibility.js "<URL>"
     ```
   - Check security headers, CORS reflection, cookie flags, and sensitive routes:
     ```bash
     python3 scripts/security_probe.py "<URL>" --recon
     ```
   - Populate `deliverables/05_non_functional_report.md`.

### Phase 6: Executive Summary Test Report (02:15 - 02:45)
1. Synthesize all logged defects by severity (Blocker, Critical, Major, Minor).
2. Establish module risk heatmap.
3. Formulate objective stakeholder release recommendation (Go / No-Go).
4. Populate `deliverables/06_summary_test_report.md`.
5. Instruct Omar to submit Deliverable 6.

### Buffer & Final Verification (02:45 - 03:00)
1. Verify all attachments are PNG/JPG (<16 MB, no video/zip).
2. Ensure no drafts remain unsubmitted on the platform.
