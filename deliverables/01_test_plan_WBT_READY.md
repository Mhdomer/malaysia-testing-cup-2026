# Test Plan: Meja Marmar (Medan Selera Meja Marmar & Dapur)
**Competition:** Malaysia Testing Cup 2026 | **Platform:** World Best Tester
**Team:** NERV | **Lead Tester:** Mohamed Makhlouf
**Specification Reference:** MEJ-FRS-001 v1.0
**Standard:** ISO/IEC/IEEE 29119-3 / ISTQB CTFL Syllabus

<!-- WBT FORM PASTE GUIDE: Copy only the text inside each FIELD 1..6 block into the 6 World Best Tester Test Plan form boxes. Every block is strictly under the 8,000-character WBT limit and integrates full AI-usage documentation directly into the graded Test Plan fields. -->

<!-- FIELD 1 START: 1. Introduction & scope (Copy text below into WBT Form Field 1) -->
## 1. Introduction & scope

Meja Marmar is a digital ordering and fulfillment platform built for a multi-stall food court (Medan Selera Meja Marmar). The system spans three connected runtime interfaces:
1. Diner Web Storefront: Customer-facing web app for hall and table selection, stall browsing, menu discovery, tray configuration (Dine-in and Tapau modes), and checkout using Diner Balance or Cash at cashier pay codes.
2. Dapur Staff and Management Portal: Back-of-house operational portal supporting three staff roles: Cook (stall-scoped order fulfillment and availability controls), Cashier (cash collection, 5-sen rounding confirmation, and ticket release), and Manager (full administrative CRUD over stalls, dishes, dining halls, tables, staff accounts, and promotion windows).
3. Public Split-Flap Queue Board: Customer-facing status display tracking live tickets across Cooking and Ready states with an automatic 20-second refresh cycle.

Operational and Regional Parameters:
- Timezone: Asia/Kuala_Lumpur (UTC+8) governing stall opening hours, last-order cutoffs, and automated promotional windows.
- Currency and Financial Accounting: Malaysian Ringgit (MYR / RM). Exact sen precision is required for Diner Balance payments and refunds, paired with statutory Bank Negara Malaysia 5-sen rounding for physical cash payments.
- Localization and Standards: British English UI copy and words-only halal classification without visual logos or icons.

### Quality Objectives
The objective of this assessment is an independent, evidence-backed black-box functional, financial, state-machine, and security audit of Meja Marmar. I use a human-led, AI-orchestrated testing workflow to maximize specification coverage across all 11 modules within the 3-hour competition window while validating every single defect against live runtime responses before submission, producing a clear Go/No-Go readiness verdict.

### In-Scope Modules (All 11 MEJ-* Modules per MEJ-FRS-001 v1.0)
Testing covers the complete functional and non-functional surface across Diner, Dapur, and Public Board personas:
1. MEJ-CTR (Centre, Halls & Tables): Dining halls (Laman Self-collect: tables 1 to 80 and 117 to 120; Dewan Sejuk Table service: tables 81 to 116), out-of-service table blocking (tables 40 and 101), table capacity limit (maximum 6 open trays per table), stall trading hours, and last-order cutoff rules.
2. MEJ-STL (Stalls & Dishes): All 10 food stalls, words-only halal classification labels (no halal logos), dish pricing (RM0.50 to RM99.90 in 10-sen steps), availability toggles (Available, Sold out today, Close for today), and automatic stall Busy status at 15 or more open tickets.
3. MEJ-TRY (Draft Tray & Ordering): Single Draft tray per diner, quantity bounds (1 to 9 per line), combined Dine-in and Tapau merge cap (maximum 9 per dish), maximum 5 distinct stalls per tray, dynamic Dine-in vs Tapau switching (drag-and-drop, keyboard, click), 60-character item notes, and Send tray validation.
4. MEJ-TEH (Teh Tarik Promotion): Automated promo window activation (09:00 to 10:59, 12:00 to 13:59, 15:00 to 16:59 MYT), RM1.50 promo pricing applied to a maximum of 2 dearest eligible cups per tray, and Manager window limits (up to 4 non-overlapping windows, duration 30 minutes to 3 hours).
5. MEJ-TOT (Totals, Charges & Tax): Item subtotal calculation, Tapau container fees (RM0.30 per Tapau unit), 10% Service charge (strictly Dine-in items at Dewan Sejuk Table service only; RM0.00 for Laman Self-collect and Tapau items), and 6% Service tax calculated with statutory half-up rounding to the nearest sen.
6. MEJ-PAY (Payments, Edits & Cancellations): Diner Balance payment (exact sen deduction) vs Cash at cashier (5-sen rounded total with 4-digit numeric pay code), Edit tray (reverting Awaiting payment tray to Draft and invalidating pay code), and Cancel unpaid tray.
7. MEJ-BAL (Diner Balance Wallet): Top-ups in fixed RM10 increments up to the RM500.00 balance cap, verifying refunds can exceed RM500.00, and enforcing no cash withdrawals or peer-to-peer transfers.
8. MEJ-TKT & MEJ-BRD (Tickets & Split-Flap Board): Queue number generation (001 to 999 cyclic), ticket lifecycle progression (New -> Cooking -> Ready -> Collected / Cancelled / Refunded), and public split-flap board with 20-second refresh and pause toggle.
9. MEJ-REF (Refunds): Cook-initiated sold-out line refunds and diner-initiated cancellations of New tickets, credited to Diner Balance in exact figures without 5-sen rounding.
10. MEJ-ACC & MEJ-DAP (Auth, RBAC & Dapur Admin): Diner and staff authentication, simultaneous dual sign-in in one browser (Diner and Dapur coexisting cleanly), and server-side RBAC enforcement across Cook, Cashier, and Manager roles.
11. MEJ-SEC (Non-Functional & Security): IDOR prevention on trays and tickets, server-side RBAC and price validation, context-aware XSS encoding, kitchen shortcuts (S, C, H), Post/Redirect/Get (PRG) patterns, concurrency/double-spend safety, and responsive viewports (1024px to 1440px desktop, 375px mobile).

### Scope of AI Tool Usage
AI (Antigravity with Gemini) is used strictly for specification decomposition, parallel workspace and browser test exploration, custom Python/Node diagnostic script execution, and ISTQB report structuring inside Team NERV's assigned competition sandbox. All defect confirmation and final scoring submissions remain strictly human-verified.

### Explicitly Out-of-Scope Items
- Destructive Denial-of-Service (DDoS) testing, automated credential brute-forcing, or high-volume traffic flooding.
- Testing shared World Best Tester infrastructure outside Team NERV's assigned Meja Marmar SUT instance.
- Physical thermal receipt printer hardware and external commercial bank settlement networks.
<!-- FIELD 1 END -->

<!-- FIELD 2 START: 2. Test strategy & techniques (Copy text below into WBT Form Field 2) -->
## 2. Test strategy & techniques

To maximize coverage across all 11 MEJ-* modules within the 3-hour window, I combined ISTQB black-box test design techniques with a structured AI-orchestrated engineering workflow and adversarial runtime probing.

### 1. How I Used AI in My Testing Process (Command-Center Workflow)
Rather than using AI as a single prompt-and-paste chatbot, I configured Antigravity as a multi-agent QA workspace driven by explicit project rules (`.agents/AGENTS.md`) and pre-built diagnostic scripts:
1. Specification-to-Matrix Synthesis:
   - I fed the full 15-page `MEJ-FRS-001 v1.0` PDF into the workspace so AI agents could extract every numeric limit, permission rule, and state guard across all 11 modules into traceable Equivalence Partitions (EP), Boundary Value Analysis (BVA) tables, State Transition diagrams, and financial Decision Tables before writing test cases.
2. Parallel Specialized Agent Orchestration:
   - As Lead Coordinator, I spawned isolated subagents with distinct roles to cover wide surface area in parallel without losing context:
     - Matrix Architect Agents: Built Deliverable 1 (ISO 29119-3 Plan), Deliverable 2 (EP/BVA/State/Decision matrices), and Deliverable 3 (`TC-001` to `TC-008` test procedures).
     - Browser Exploration Scouts: Automated live browser journeys across Diner and Dapur roles in isolated browser contexts, verifying dual-session coexistence, 375px mobile overflow, 200% zoom reflow, and keyboard shortcut trapping.
     - Security & Concurrency Hunters: Executed targeted `fetch` / `Promise.all` burst tests inside authenticated sessions to probe IDOR paths, server-side RBAC, double-refund exploits, and Busy/status enforcement.
3. Scripted Diagnostic Pipeline (`scripts/`):
   - Used AI to author and run local Node.js and Python tools (`battle_runner.py`, `crawler.js`, `audit_accessibility.js`, `security_probe.py`, `fuzz_gen.py`) to inspect HTTP headers, cookie flags, CORS policies, WCAG 2.1 AA accessibility trees, and boundary string inputs automatically.
4. Strict Human-in-the-Loop Anti-Hallucination Gate:
   - LLMs frequently misread specifications or hallucinate edge-case rules. Therefore, I enforced a strict verification rule: every single defect surfaced by a subagent had to be manually cross-checked by me against the literal text of `MEJ-FRS-001 v1.0` AND backed by live HTTP status codes, JSON/HTML responses, or DevTools traces.
   - Using this audit gate, I actively filtered out 7 false-positive subagent findings (for example, incorrect claims regarding identical dish notes, hallucinated unpaid-tray limits, and misquoted opening hours) so that only 100% reproducible, spec-backed bugs entered Deliverable 4.

### 2. Specification-Based Black-Box Techniques
- Equivalence Partitioning (EP):
  - Applied across table numbers (1 to 120), dish prices (RM0.50 to RM99.90 in 10-sen steps), item quantities (1 to 9), stalls per tray (1 to 5), wallet top-ups (multiples of RM10), and field lengths (full names: 2 to 60 chars; item notes: 0 to 60 chars; board message: 0 to 60 chars; place notes: 0 to 30 chars; stall/cuisine names: 2 to 40 chars; staff username: 3 to 20 lowercase a-z chars).
- Boundary Value Analysis (BVA):
  - Targeted exact edges: tables (0, 1, 80, 81, 116, 117, 120, 121), blocked tables (40, 101), table open tray capacity (5, 6, 7th rejected), prices (RM0.40, RM0.50, RM99.90, RM100.00), merged dish qty (4+5=9 valid, 5+5=10 invalid), wallet cap (RM490 + RM10 = RM500 valid; +RM20 rejected), Teh Tarik durations (29m, 30m, 180m, 181m), and queue rollover (`999` -> `001`).
- State Transition Testing:
  - Tray Lifecycle: `(none) -> Draft -> Awaiting payment <-> Draft (Edit tray) -> Paid / Cancelled -> Complete`. Verified Paid trays cannot revert to Draft/Cancelled and Cancelled trays cannot be paid.
  - Ticket Lifecycle: `New -> Cooking -> Ready -> Collected`; `New -> Cancelled` (diner); `New / Cooking -> Refunded` (Cook sold-out). Verified terminal states (`Collected`, `Refunded`, `Cancelled`) reject further mutations and cooks remain restricted to their assigned stall.
  - Stall States: `Open`, `Busy` (>= 15 open tickets), `Sold out today`, `Close for today`.
- Decision Table Testing:
  - Permuted Dining Mode (Dine-in vs Tapau) x Hall (Laman Self-collect vs Dewan Sejuk Table service) x Teh Tarik Window (Active vs Inactive) x Payment Method (Diner Balance vs Cash at cashier) to audit RM0.30 container fees, 10% Service charge (Dewan Sejuk Dine-in only), 6% Service tax (half-up sen rounding), and 5-sen cash rounding vs exact-sen Balance/refunds.

### 3. Adversarial Security & Non-Functional Probing
- IDOR & Session Tampering: Tested horizontal isolation across `/trays/{id}`, `/cancel`, `/edit`, and ticket endpoints between distinct diner sessions, plus open redirect checks on `?next=`.
- RBAC & Server-Side Validation: Tampered with POST payloads to test Cook cross-stall isolation, Manager-only routes, hidden/disabled `Busy` status bypasses, and server-side price/state checks.
- Concurrency & Race Conditions: Executed parallel browser `Promise.all` requests against checkout, cancellation, and multi-stall refund endpoints to detect double-refund balance inflation and capacity bypasses.
- Accessibility, Shortcuts & Layout: Ran Axe-core WCAG 2.1 AA audits, tested Dapur keyboard shortcuts (`S`, `C`, `H`) inside and outside text inputs, and inspected layouts at 375px mobile and 200% zoom.

### 4. Risk-Weighted Execution Priority
- P1 (Financial & Balance Integrity): 5-sen cash vs exact-sen Balance/refund math, multi-ticket refund exploits, RM500 wallet cap, service charge/tax rules.
- P2 (Security & Access Control): IDOR on trays/tickets, Cook stall isolation, open redirects, server-side status/price validation.
- P3 (State Machine & Concurrency): Tray/ticket transitions, `Busy`/`Sold out` guards, `999` queue rollover, race conditions.
- P4 (Business Logic & Promos): Teh Tarik 2-dearest-cup promo, 5-stall tray cap, out-of-service tables 40 & 101.
- P5 (UI, A11y & Queue Board): 20s split-flap refresh, shortcut focus leaks, WCAG 2.1 AA heading/contrast checks, responsive reflow.
<!-- FIELD 2 END -->

<!-- FIELD 3 START: 3. Test environment & data (Copy text below into WBT Form Field 3) -->
## 3. Test environment & data

### 1. Client Hardware, Browsers & Diagnostic Stack
- Operating System: CachyOS Linux (Kernel 6.13+, x86_64, Wayland / Niri compositor).
- Primary Browsers: Chromium / Google Chrome (Latest) with DevTools (Network, Console, Application Storage, Device Mode) and Mozilla Firefox (Latest).
- Viewports & Scaling: Desktop baseline `1280x800`, desktop range `1024x768` to `1440x900`, mobile portrait `375x812`, plus `200%` browser zoom reflow testing.

### 2. AI Workspace & Pre-Built CLI Toolkit (`scripts/` & `.agents/`)
To avoid wasted time during the 3-hour sprint, I structured my local workspace beforehand to connect AI planning directly with automated runtime checks:
- Antigravity Multi-Agent Orchestrator: Configured workspace operational rules (`.agents/AGENTS.md`) defining timeboxed phases, ISTQB defect structure, and a zero-hallucination evidence requirement, paired with 16 offline domain skills (`.agents/skills/` covering IDOR, business logic, race conditions, XSS, parameter pollution, and API abuse).
- Automated Recon & Headless Scripts (`scripts/`):
  - `scripts/battle_runner.py`: Single-command Phase 1 runner chaining HTTP probing, header inspection, endpoint discovery, and headless DOM capture.
  - `scripts/crawler.js`: Puppeteer crawler recording live routes, console errors, failed network requests, and full-page PNG screenshots.
  - `scripts/audit_accessibility.js`: Automated Axe-core WCAG 2.1 AA compliance scanner across Diner, Dapur, and Board routes.
  - `scripts/security_probe.py`: Automated auditor for HTTP security headers (CSP, HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy), CORS reflection, and cookie flags (`HttpOnly`, `SameSite`, `Secure`).
  - `scripts/fuzz_gen.py`: Deterministic generator for BVA numeric boundaries, exact-length strings (60/61 chars), and XSS test vectors.

### 3. Platform Environmental Parameters
- Server Timezone: `Asia/Kuala_Lumpur` (UTC+8) for trading hours, cutoffs, and Teh Tarik promo windows.
- Currency: Malaysian Ringgit (`MYR` / `RM`), checked at 1-sen exact units (Balance/refunds) and 5-sen cash rounding.
- Database Isolation: Dedicated Team NERV sandbox instance on the SUT, resetting baseline accounts and isolation boundaries cleanly.

### 4. Test Data & Account Inventory (MEJ-FRS-001 Annex A)
Universal demo password across all seeded demo accounts: `marmar2026`.

Diner Accounts:
- `nuraisyah.rahman@example.com` (Nur Aisyah Rahman, Shah Alam)
- `weiling.tan@example.com` (Tan Wei Ling, Petaling Jaya)
- `arjun.selvarajah@example.com` (Arjun a/l Selvarajah, Klang)
- `farid.iskandar@example.com` (Farid Iskandar, Ampang)
- `meiyee.chong@example.com` (Chong Mei Yee, Puchong)
- `hafiz.zulkifli@example.com` (Hafiz Zulkifli, Kajang)
- `priya.murugan@example.com` (Priya Devi a/p Murugan, Brickfields)
- `boonkiat.goh@example.com` (Goh Boon Kiat, Cheras)
- `sitihajar.omar@example.com` (Siti Hajar Omar, Bangsar)

Dapur Staff Accounts:
- Managers: `rosnah` (Rosnah Abdullah), `faizal` (Faizal Hamdan)
- Cashiers: `kavitha` (Kavitha Raman), `kenghock` (Ooi Keng Hock)
- Cooks (Stalls 1 to 10): `zainal` (Stall 1), `normah` (Stall 2), `sulaiman` (Stall 3), `kheong` (Stall 4), `ahlan` (Stall 5), `swee` (Stall 6), `esah` (Stall 7), `latiff` (Stall 8), `rohana` (Stall 9), `kamaruddin` (Stall 10).

Synthesized Boundary & Adversarial Test Vectors:
- Table Numbers: `0`, `1`, `40` (out of service), `80`, `81`, `101` (out of service), `116`, `117`, `120`, `121`.
- Dish Prices: `RM0.40`, `RM0.50`, `RM0.60`, `RM12.30`, `RM99.90`, `RM100.00`.
- Top-Ups & Rounding Probes: `RM5`, `RM10`, `RM15`, `RM20`, `RM50`, `RM500.00` cap, plus cash rounding endings (`.x1` to `.x9` sen).
- Strings & Security Vectors: `60-char` exact boundary, `61-char` overflow, `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`, `O'Connor-Tan @ Omar.`, and external `?next=https://evil.example` redirect tests.
<!-- FIELD 3 END -->

<!-- FIELD 4 START: 4. Risks & assumptions (Copy text below into WBT Form Field 4) -->
## 4. Risks & assumptions

### 1. Product & Technical Quality Risks
1. Financial Rounding & Refund Calculation Errors:
   - Risk: 5-sen cash rounding leaks into Diner Balance debits, refunds, or today's cash takings totals, or multi-stall tray refunds credit the full tray total multiple times instead of per-ticket amounts.
   - Impact: Direct financial loss, balance inflation exploits, and incorrect daily accounting.
2. Wallet Balance Cap Violations:
   - Risk: Top-ups bypass the RM500.00 cap or accept non-RM10 steps, or valid refunds fail when pushing balance past RM500.00.
   - Impact: Stored-value liability and blocked customer refunds.
3. Insecure Direct Object Reference (IDOR) & Open Redirects:
   - Risk: Diners read, edit, pay for, or cancel another diner's tray or ticket by modifying numeric IDs in URL paths or POST targets, or `?next=` parameters redirect users off-site after login.
   - Impact: Privacy breach, cross-account order hijacking, and phishing exposure.
4. Server-Side State & Availability Bypass:
   - Risk: The server allows `Send tray`, `Take payment`, or ticket transitions against `Busy`, `Sold out`, or `Cancelled` entities when endpoints are invoked directly or via cached UI state.
   - Impact: Unfulfillable paid orders and broken kitchen capacity throttling.
5. Broken Multi-Role RBAC & Dual-Session Collision:
   - Risk: Cooks access other stalls' tickets, unauthorized roles reach Manager CRUD endpoints, or running Diner and Dapur sessions in one browser causes cookie clobbering.
   - Impact: Privilege escalation and corrupted test/operational sessions.
6. Concurrency & Race Conditions:
   - Risk: Parallel checkout, cancellation, or table submission requests cause double spending, duplicate refunds, or > 6 open trays per table.
   - Impact: Financial inconsistency and capacity overruns.
7. Accessibility, Focus Leaks & Mobile Overflow:
   - Risk: Global Dapur keyboard shortcuts (`S`, `C`, `H`) trigger while typing inside inputs, missing `<h1>` headings break screen readers, or tables/cards clip horizontally at `375px` mobile or `200%` zoom.
   - Impact: Accidental ticket state changes by cooks and degraded usability.

### 2. AI-Assisted Testing Risks & Mitigations
1. AI Specification Hallucination / Misremembered Rules:
   - Risk: An AI subagent invents requirements not in `MEJ-FRS-001 v1.0` (such as fake tray limits, misquoted wording rules, or wrong operating hours), creating noisy false-positive defect reports.
   - Mitigation: Every AI claim must cite the exact `MEJ-*` section and pass manual human verification against the PDF spec and live HTTP/UI evidence before logging.
2. Context Drift During Long Multi-Agent Sessions:
   - Risk: Autonomous browser scouts lose track of mutated database state (e.g., an altered stall status or balance) across concurrent tests.
   - Mitigation: Keep agents modular with fresh narrow charters, track exact test IDs/table numbers per agent, and verify clean pre-conditions before logging financial/state bugs.
3. Unscoped Automated Probing:
   - Risk: Automated crawlers or security probes accidentally touch non-SUT pages or cause unnecessary load.
   - Mitigation: Lock all scripts and subagents strictly to `https://www.worldbesttester.com/sut/mejamarmar/` (Team NERV instance), banning DDoS, password brute-force, or external host calls.

### 3. Operational & Environmental Assumptions
1. Isolated Team Sandbox: The SUT isolates Team NERV's database state cleanly from competing teams.
2. Timezone Sync: SUT server time is synchronized to `Asia/Kuala_Lumpur` (UTC+8) for stall trading hours and Teh Tarik promo windows.
3. Standard HTTP & PRG Semantics: State-changing actions follow Post/Redirect/Get (PRG) patterns and return accurate HTTP status codes (`200`, `302`, `400`, `403`, `404`, `409`).
<!-- FIELD 4 END -->

<!-- FIELD 5 START: 5. Roles & schedule (Copy text below into WBT Form Field 5) -->
## 5. Roles & schedule

### 1. Human-Led Multi-Agent Role Architecture
I structured Team NERV as a human-in-the-loop command center where I retain sole authority over strategy, spec validation, and final defect reporting while delegating high-throughput execution and synthesis across specialized AI subagents:

- Mohamed Makhlouf (Human Lead QA Coordinator & Final Verifier):
  - Defined the workspace rules, priority matrix, and verification gates.
  - Directed AI subagents across targeted exploratory charters, designed adversarial race-condition and IDOR probes, and personally audited every candidate bug against `MEJ-FRS-001 v1.0` and live runtime evidence (discarding false positives before logging).
  - Finalized severity classifications (Blocker, Critical, Major, Minor) and authored the Go/No-Go stakeholder recommendation.
- Matrix Architect Subagents (Antigravity / Gemini):
  - Parsed `MEJ-FRS-001 v1.0` to build structured EP/BVA tables, Tray/Ticket state transition guards, and multi-variable financial Decision Tables.
  - Synthesized `TC-001` through `TC-008` implementation procedures and formatted verified defects to ISTQB standards.
- Parallel Browser Exploration Scouts (Playwright / Chromium Subagents):
  - Diner Scout: Tested halls, table limits, blocked tables 40 & 101, Teh Tarik promo pricing, Tapau/Dine-in drag/click behavior, 5-sen cash rounding, and `375px` / `200%` zoom responsiveness.
  - Dapur & RBAC Scout: Validated simultaneous Diner + Dapur dual login, Cook/Cashier/Manager CRUD and RBAC isolation, queue rollover (`999`), keyboard shortcuts (`S`, `C`, `H`) inside inputs, and sold-out refund workflows.
  - Concurrency & IDOR Hunter: Tested cross-diner `/trays/{id}` access, `?next=` open redirects, multi-stall cancellation refund exploits, `Busy` status bypasses, and `Promise.all` parallel submissions.
- Automated Diagnostic Scripts (`scripts/` CLI Runner):
  - Executed `battle_runner.py`, `crawler.js`, `audit_accessibility.js`, `security_probe.py`, and `fuzz_gen.py` for repeatable HTTP header, cookie flag, CORS, WCAG 2.1 AA, and boundary string checks.

### 2. Timeboxed 3-Hour Competition Execution Schedule
- Phase 1 (00:00 to 00:20) - Recon, Spec Ingestion & Test Plan:
  - Ingested `MEJ-FRS-001 v1.0`, inspected live WBT submission schemas, ran `battle_runner.py` and header/endpoint recon, and drafted Deliverable 1 (Test Plan) including the AI orchestration methodology.
- Phase 2 (00:20 to 00:45) - AI-Assisted Test Analysis & Design:
  - Converted all 11 `MEJ-*` modules into EP, BVA, State Transition, and Decision Table matrices; compiled Deliverable 2.
- Phase 3 (00:45 to 01:05) - Test Implementation:
  - Authored deterministic end-to-end test cases (`TC-001` to `TC-008`) with exact test accounts and expected financial formulas; bundled Deliverables 2 & 3 into the WBT upload attachment.
- Phase 4 (01:05 to 02:15) - Parallel Bug Hunting & Non-Functional Audit:
  - Deployed Diner Scout, Dapur RBAC Scout, and Concurrency/IDOR Hunter in parallel alongside Axe-core accessibility scans and security probes.
  - Conducted strict human-in-the-loop verification against `MEJ-FRS-001 v1.0` and live HTTP traces, filtering out false positives and logging verified defects in Deliverable 4 plus non-functional findings in Deliverable 5.
- Phase 5 (02:15 to 02:45) - Triage Synthesis & Summary Report:
  - Aggregated verified severity metrics, financial/security impact chains, and authored Deliverable 6 (Summary Test Report with Go/No-Go verdict).
- Phase 6 (02:45 to 03:00) - Final WBT Submission Audit:
  - Verified character limits across all 6 WBT Test Plan textareas, attached the Test Design & Cases bundle, confirmed all bug reports on WBT, and checked formatting consistency.
<!-- FIELD 5 END -->

<!-- FIELD 6 START: 6. Exit criteria (Copy text below into WBT Form Field 6) -->
## 6. Exit criteria

Testing and final submission are complete only when all coverage, AI-verification, and deliverable gates pass:

### 1. Functional & Risk Coverage Criteria
1. 100% module coverage achieved across all 11 modules specified in `MEJ-FRS-001 v1.0` (`MEJ-CTR`, `MEJ-STL`, `MEJ-TRY`, `MEJ-TEH`, `MEJ-TOT`, `MEJ-PAY`, `MEJ-BAL`, `MEJ-TKT`, `MEJ-BRD`, `MEJ-REF`, `MEJ-ACC`/`MEJ-DAP`, and `MEJ-SEC`).
2. 100% of Priority 1 and Priority 2 risk areas (5-sen rounding vs exact-sen math, multi-ticket refund integrity, RM500 balance cap, IDOR isolation, RBAC enforcement, open redirects, `Busy` status validation, and race conditions) executed against the live SUT.
3. All core traceability test cases (`TC-001` through `TC-008`) executed with recorded actual outcomes.

### 2. Human-in-the-Loop AI Verification & Defect Quality Criteria
1. Zero Unverified AI Claims: Every bug hypothesized by AI agents or scripts is independently reproduced on the live SUT and audited against exact clauses in `MEJ-FRS-001 v1.0` by the human lead before submission.
2. False Positive Removal Complete: Any speculative or hallucinated AI finding that contradicts the spec or lacks runtime proof is explicitly rejected and excluded from Deliverable 4.
3. ISTQB Logging Completeness: Every submitted defect includes a clear title, traceable `MEJ-*` requirement ID, justified severity, step-by-step deterministic reproduction steps, observed vs expected results, and concrete runtime evidence (HTTP status/payloads, DevTools logs, script output, or screenshots).

### 3. Deliverable & Platform Readiness Criteria
1. Deliverable 1 (Test Plan) formatted cleanly under the 8,000-character limit per field across all 6 WBT textareas, clearly documenting both testing scope and AI usage.
2. Deliverables 2 and 3 (Test Analysis & Design Matrix + Test Implementation Cases) compiled into a single readable attachment ready for WBT upload.
3. Deliverable 4 (Verified Defect Reports), Deliverable 5 (Non-Functional Testing Report covering security headers, Axe-core WCAG 2.1 AA, keyboard focus, and responsive reflow), and Deliverable 6 (Stakeholder Summary Report with an evidence-backed Go/No-Go decision) finalized with consistent counts and metrics.
<!-- FIELD 6 END -->
