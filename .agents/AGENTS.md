# AGENTS.md: Malaysia Testing Cup 2026 Workspace Router
*Operational Context, Scoring Rules & Assessment Protocol for Team NERV*

---

## 👤 1. Team & Candidate Context
- **Candidate:** Mohamed Makhlouf (Omar / Mhdomar)
- **Role:** Lead Quality & Security Assessment Engineer
- **Team Name:** `NERV`
- **Competition:** Malaysia Testing Cup 2026 (National Pre-Qualifier to World's Best Tester)
- **Organiser:** Malaysian Software Testing Board (MSTB)
- **Platform:** World Best Tester (`https://www.worldbesttester.com`)
- **Broadcast & Briefing:** StreamYard (`https://streamyard.com/watch/cRrd9TwnMrDF`)
- **Key Date:** Saturday 14 November 2026 (04:30 AM to 08:00 AM AST / 09:30 AM to 01:00 PM MYT)

---

## 🎯 2. Operational Methodology & Scoring Architecture

The competition evaluates a 130-point matrix across 6 core deliverables and 2 bonus criteria:

| Phase / Category | Deliverable | Points | Target Window (AST) | Target Window (MYT) |
|---|---|:---:|---|---|
| **Phase 1** | Deliverable 1: Test Plan (ISO 29119-3) | 20 | 05:00 - 05:20 AM | 10:00 - 10:20 AM |
| **Phase 2** | Deliverable 2: Test Analysis & Design Matrix | 20 | 05:20 - 05:45 AM | 10:20 - 10:45 AM |
| **Phase 3** | Deliverable 3: Test Implementation (Cases) | 20 | 05:45 - 06:05 AM | 10:45 - 11:05 AM |
| **Phase 4** | Deliverable 4: High-Fidelity Bug Reports | 20 | 06:05 - 07:15 AM | 11:05 - 12:15 PM |
| **Phase 5** | Deliverable 5: Non-Functional Testing (Security, Perf, A11y) | 20 | 06:05 - 07:15 AM | 11:05 - 12:15 PM |
| **Phase 6** | Deliverable 6: Summary Test Report (Stakeholder Go/No-Go) | 20 | 07:15 - 07:45 AM | 12:15 - 12:45 PM |
| **Bonus 1** | Smart Use of AI Tools (Engineering multiplier) | 5 | Continuous | Continuous |
| **Bonus 2** | Exceptional Performance (Golden Bug / architectural flaw) | 5 | Continuous | Continuous |

---

## 🛡️ 3. Hard Behavioral Constraints
1. **Strictly Zero Em Dashes:** Never use em dashes (`—`, `–`, or `--` used as a dash). Use colons, commas, periods, or clean bullet points instead.
2. **Context Canary ("Omar"):** Every assistant response must explicitly begin with "Omar" (e.g., "Omar, ...").
3. **No Shell `cd` Commands:** Antigravity runs commands directly in the specified working directory. Never suggest or run `cd` in terminal tool calls.
4. **Natural Human Git Commits:** Use short conventional commits (`feat: ...`, `fix: ...`, `test: ...`, `docs: ...`).
5. **No Hallucinated Findings:** Every logged defect must be validated against actual SUT runtime behavior, DevTools traces, or script output.

---

## 🧰 4. Available Diagnostic Tools (`scripts/`)
- `node scripts/crawler.js "<URL>"`: Maps DOM, captures console errors, logs failed requests, saves full-page screenshot.
- `node scripts/audit_accessibility.js "<URL>"`: Runs Axe-core WCAG 2.1 AA audit for Deliverable 5.
- `python3 scripts/security_probe.py "<URL>"`: Audits CSP, Clickjacking, HSTS, CORS reflection, cookie flags.
- `python3 scripts/security_probe.py "<URL>" --recon`: Discovers sensitive exposed endpoints (Swagger, .env, Actuator).
- `python3 scripts/security_probe.py --jwt "<TOKEN>"`: Decodes JWT claims and creates `alg: none` forged test vectors.
- `python3 scripts/fuzz_gen.py --type <type> --len <N> --copy`: Generates boundary inputs and pipes to `wl-copy`.
