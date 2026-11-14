# Test Plan: Meja Marmar (Medan Selera Meja Marmar & Dapur)
**Competition:** Malaysia Testing Cup 2026  
**Team:** NERV | **Lead Tester:** Mohamed Makhlouf  
**Specification Reference:** MEJ-FRS-001 v1.0  
**Standard:** ISO/IEC/IEEE 29119-3 / ISTQB CTFL Syllabus  

---

### 1. Context & Objectives
- **Context:** Independent black-box quality and security assessment of the **Meja Marmar** food-court ordering platform (Diner storefront, Dapur staff/management portal, and public Split-Flap Queue Board) under release-candidate conditions. The system operates on `Asia/Kuala_Lumpur` (UTC+8) business hours, uses Malaysian Ringgit (MYR / RM) currency rules, and targets British English UI copy.
- **Primary Objective:** Identify high-severity functional, financial, security, usability, and concurrency defects before production release, and provide an evidence-backed Go/No-Go readiness recommendation for stakeholders.

---

### 2. Scope

#### 2.1 In-Scope Items
All 11 functional and non-functional modules defined in `MEJ-FRS-001 v1.0`, across both **Diner** (email/password) and **Dapur Staff** (Cook of one stall, Cashier, Manager) personas:

1. **MEJ-CTR (Centre, Halls & Tables):** 2 halls (Laman Self-collect: tables 1 to 80 and 117 to 120; Dewan Sejuk Table service: tables 81 to 116), out-of-service enforcement (tables 40 and 101), max 6 open trays per table, stall operating hours, and last-order cutoffs.
2. **MEJ-STL (Stalls & Dishes):** 10 stalls, words-only halal labels, dish pricing (RM0.50 to RM99.90 in 10 sen steps), `Sold out today`, `Close for today`, and automatic `Busy` status (>= 15 open tickets).
3. **MEJ-TRY (Draft Tray & Ordering):** Single Draft tray per diner at a time, quantity 1 to 9 per line, max 5 stalls per tray, Dine-in vs Tapau switching (drag, keyboard, click), 60-character item notes, and Send tray validation order.
4. **MEJ-TEH (Teh Tarik Promotion):** Active windows (9.00am to 10.59am, 12.00pm to 1.59pm, 3.00pm to 4.59pm MYT), RM1.50 promotional price for max 2 dearest eligible cups per tray, and Manager configuration limits (max 4 windows, 30 minutes to 3 hours duration).
5. **MEJ-TOT (Totals, Charges & Tax):** Item subtotals, Tapau containers (RM0.30 per Tapau line/unit as specified), 10% Service charge (Dine-in at Dewan Sejuk Table service only), and 6% Service tax (half-up rounding).
6. **MEJ-PAY (Payments, Edits & Cancellations):** Diner Balance payment vs Cash at cashier (with 5-sen rounding and 4-digit pay code), Edit tray, and Cancel unpaid tray.
7. **MEJ-BAL (Diner Balance Wallet):** Top-ups in RM10 steps up to RM500.00 maximum cap, refunds permitted to exceed RM500.00, and strict prohibition of withdrawals or peer transfers.
8. **MEJ-TKT & MEJ-BRD (Tickets & Split-Flap Board):** Queue numbers `001` to `999`, ticket lifecycle (`New -> Cooking -> Ready -> Collected / Cancelled / Refunded`), and public split-flap board with 20-second auto-refresh.
9. **MEJ-REF (Refunds):** Sold-out line refunds and diner cancellation of `New` tickets, credited in exact figures without 5-sen rounding.
10. **MEJ-ACC & MEJ-DAP (Auth, RBAC & Dapur Admin):** Authentication, simultaneous 2 sign-ins in 1 browser (Diner + Dapur), server-enforced RBAC (Cook restricted to assigned stall, Cashier payment/collection, Manager full CRUD for stalls, dishes, halls, tables, and users).
11. **MEJ-SEC (Non-Functional & Security):** Own-trays-only IDOR protection, server-side RBAC, server-side price and state validation, XSS text-as-typed output encoding, keyboard shortcuts (`S`, `C`, `H`), Post/Redirect/Get (PRG) and concurrency safety, and responsive layouts (1024px to 1440px desktop and 375px mobile).

#### 2.2 Out-of-Scope Items
- Destructive Denial-of-Service (DDoS) or infrastructure-level volume/load flooding.
- Source code white-box static analysis (black-box assessment against the deployed SUT only).
- Third-party payment gateway settlement outside the simulated Balance and Cash-at-Cashier flows.

---

### 3. Quality Risk Assessment & Prioritization

| Priority | Risk Category | Specific Failure Modes & Impact |
|---|---|---|
| **Critical** | **Financial & Rounding Integrity** | Incorrect 5-sen cash rounding vs exact balance/refund figures, 6% service tax half-up miscalculation, 10% service charge leaking onto Laman Self-collect or Tapau orders, or Tapau container fee (RM0.30) omissions. |
| **Critical** | **Balance & Wallet Integrity** | Top-up bypassing the RM500.00 cap or RM10 step constraint, negative balance exploits, or unauthorized withdrawal/transfer paths. |
| **Critical** | **Authorization & IDOR** | Diners viewing, editing, paying, or cancelling another diner's tray/ticket via URL/ID manipulation; Cook accessing or mutating another stall's tickets or Manager CRUD endpoints. |
| **Critical** | **Server-Side Price & State Bypass** | Tampering with dish prices, Teh Tarik promo prices, quantities, or ticket states in client requests; bypassing `Sold out today`, `Close for today`, or out-of-service tables (40, 101). |
| **Critical** | **Concurrency & Race Conditions** | Double-spending Balance on parallel `Pay` requests, double-refunding on parallel `Cancel` requests, exceeding 6 open trays/table under concurrent submissions, or duplicate submissions on refresh (missing PRG). |
| **Major** | **State Machine Violations** | Invalid ticket transitions (e.g., `Collected -> Cancelled`, `Ready -> New`, or Cook cancelling without stock/refund sync). |
| **Major** | **Teh Tarik & Capacity Rules** | Applying RM1.50 to > 2 cups, discounting cheapest instead of dearest cups, wrong `Asia/Kuala_Lumpur` window boundaries, or failing to flag `Busy` at >= 15 open tickets. |
| **Moderate** | **UI, Accessibility & Board Sync** | Split-flap board failing 20-second auto-refresh, broken `S`/`C`/`H` shortcuts, inaccessible Dine-in/Tapau switching, 60-char note truncation errors, or layout clipping at 375px / 1024px to 1440px. |

---

### 4. Test Approach & Strategy

#### 4.1 Phased Execution Flow
1. **Phase A: Diner Side First:** Verify authentication, hall/table selection (Laman vs Dewan Sejuk, tables 40 & 101 blocked), stall browsing, Teh Tarik window behaviour, Draft tray constraints (1 draft, qty 1 to 9, max 5 stalls, 60-char notes, Dine-in/Tapau), total calculations (containers, 10% service charge, 6% tax), and Balance/Cash payments.
2. **Phase B: Dapur Portal as Manager (plus Cook & Cashier):** Verify dual sign-in in one browser, strict RBAC boundaries across Cook (single stall), Cashier (cash confirmation with 4-digit pay code), and Manager (CRUD for stalls, dishes, halls, tables, Teh Tarik windows, and users).
3. **Phase C: Integrated End-to-End & Adversarial:** Execute cross-persona workflows: ticket progression (`New -> Cooking -> Ready -> Collected`), sold-out line refunds and `New` ticket cancellations (exact figure refunds), public split-flap board 20s updates, boundary limits (6 open trays/table, 15 open tickets `Busy` threshold, RM500 top-up cap), and security/resilience checks (address bar IDOR, PRG refresh, concurrent requests, XSS payloads).

#### 4.2 Test Design Techniques
- **Equivalence Partitioning (EP) & Boundary Value Analysis (BVA):** Applied to tables (1 to 120, 40, 101), dish prices (RM0.50 to RM99.90 in 10 sen steps), quantities (1 to 9), stalls per tray (1 to 5), open trays per table (6), notes (60 chars), top-ups (RM10 steps, RM500 cap), Teh Tarik windows (max 4, 30m to 3h), and queue numbers (`001` to `999`).
- **State Transition Testing:** Applied to Draft/Unpaid/Paid trays and Ticket states (`New`, `Cooking`, `Ready`, `Collected`, `Cancelled`, `Refunded`), plus Stall states (`Open`, `Busy`, `Closed`, `Sold out`).
- **Decision Table Testing:** Applied to Charge/Tax/Promo combinations (Hall x Dining Mode x Teh Tarik Window x Payment Method).
- **Experience-Based & Non-Functional Testing:** Error guessing, timeboxed exploratory charters, Chrome DevTools network/console inspection, Axe-core WCAG 2.1 AA audits, and OWASP API/client security probing.

---

### 5. Test Environment, Tools & How AI Was Used
- **Client Environment:** CachyOS Linux (Kernel 6.13+), Chromium / Google Chrome (Latest), Mozilla Firefox (Latest).
- **Diagnostic & Automation Toolkit (`scripts/`):**
  - `scripts/battle_runner.py` for single-command Phase 1 HTTP probing, endpoint discovery, and DOM capture.
  - `scripts/crawler.js` for DOM mapping, console error capture, and failed network request logging.
  - `scripts/audit_accessibility.js` for automated Axe-core WCAG 2.1 AA compliance checks.
  - `scripts/security_probe.py` for HTTP security headers, CORS, cookie flags, and endpoint reconnaissance.
  - `scripts/fuzz_gen.py` for boundary string, numeric, and XSS/injection vector generation.
- **Human-Led AI Orchestration (Antigravity / Gemini):**
  - **Specification Decomposition:** Parsed the 15-page `MEJ-FRS-001 v1.0` PDF across all 11 `MEJ-*` modules to derive EP, BVA, State Transition, and financial Decision Table matrices.
  - **Parallel Multi-Agent Execution:** Coordinated specialized subagents in parallel: Matrix Architect agents for ISO 29119-3 design/cases, Playwright/Chromium Browser Scouts covering Diner and Dapur RBAC flows, and Security/Concurrency Hunters running `Promise.all` bursts and IDOR/redirect probes.
  - **Human-in-the-Loop Anti-Hallucination Gate:** Every AI-surfaced hypothesis was manually audited by Mohamed Makhlouf against the literal wording of `MEJ-FRS-001 v1.0` and live runtime HTTP/DevTools traces before logging, explicitly rejecting false-positive agent claims.

---

### 6. Entry/Exit Criteria & Team NERV Roles

#### 6.1 Entry & Exit Criteria
- **Entry Criteria:** Live SUT URL, Diner and Dapur (Cook, Cashier, Manager) credentials, and `MEJ-FRS-001 v1.0` specification available.
- **Exit Criteria:** 100% of Critical risk areas and all 11 `MEJ-*` modules exercised; 100% of AI-surfaced defects verified against `MEJ-FRS-001 v1.0` and live runtime evidence (zero unverified AI claims) in Deliverable 4; Non-Functional audit completed in Deliverable 5; Stakeholder Go/No-Go Summary Report delivered in Deliverable 6.

#### 6.2 Team NERV Role Allocation
- **Human Lead QA Coordinator & Final Verifier:** Mohamed Makhlouf. Directs agent charters, enforces the anti-hallucination verification gate against `MEJ-FRS-001 v1.0`, validates financial/security exploits, and issues Go/No-Go sign-off.
- **Matrix Architect Subagents:** Synthesize ISO 29119-3 Test Plan, Test Analysis & Design Matrix (EP/BVA/State/Decision Tables), and Test Case Implementation (`TC-001` to `TC-008`).
- **Diner & Dapur Browser Scouts:** Run live browser journeys across Diner storefront flows, dual Diner+Dapur login coexistence, Cook/Cashier/Manager RBAC boundaries, and mobile/zoom layouts.
- **Concurrency, Security & Diagnostic Runner:** Executes IDOR, open redirect, `Busy` bypass, `Promise.all` double-refund checks, plus `scripts/` CLI security/a11y audits.
