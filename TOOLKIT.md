---
title: MTC 2026 Execution Toolkit & ISTQB Submission Templates
competition: Malaysia Testing Cup 2026
team: NERV
target_score: 130/130
tags:
  - competition
  - software-testing
  - istqb
  - templates
---

# 🛠️ MTC 2026 Execution Toolkit & Submission Templates

> [!important] 🎯 Purpose of this Toolkit
> In the Malaysia Testing Cup, filing raw bugs only accounts for **20 out of 130 points**. The remaining 110 points evaluate engineering rigor: Test Planning (20), Analysis & Design (20), Implementation (20), Summary Reporting (20), Non-Functional Testing (20), and AI/Exceptional Bonuses (10).
> 
> Use these pre-built, ISTQB-aligned Markdown templates during the live 3-hour window. Copy, customize with the System Under Test (SUT) specifics, and submit directly through the platform.

---

## ⏱️ 3-Hour Battle Timebox Strategy

| Window | Duration | Objective | Target Deliverable |
|---|---|---|---|
| **00:00 - 00:20** | 20 min | Reconnaissance & Test Planning | Submit **Deliverable 1: Test Plan** |
| **00:20 - 00:45** | 25 min | Test Analysis & Design | Submit **Deliverable 2: Test Analysis & Design** |
| **00:45 - 01:05** | 20 min | Test Implementation | Submit **Deliverable 3: Test Implementation (Cases)** |
| **01:05 - 02:15** | 70 min | Active Bug Hunting & Non-Functional Audit | Submit **Deliverable 4 (Defect Reports)** & **Deliverable 5 (Non-Functional)** |
| **02:15 - 02:45** | 30 min | Synthesis & Stakeholder Reporting | Submit **Deliverable 6: Summary Test Report** |
| **02:45 - 03:00** | 15 min | Buffer & Final Polish | Verify all attachments (<16MB, no zip/video), check links, review AI prompt logs |

---

## 📋 Deliverable 1: Test Plan Template (20 Points)

```markdown
# Test Plan: [SUT Application Name]
**Competition:** Malaysia Testing Cup 2026  
**Team:** NERV | **Tester:** Mohamed Makhlouf  
**Standard:** ISO/IEC/IEEE 29119-3 / ISTQB CTFL Syllabus

### 1. Context & Objectives
- **Context:** Independent black-box quality assessment of the [SUT Application Name] web application under release-candidate conditions.
- **Primary Objective:** Identify high-severity functional, security, usability, and performance defects before production release, assessing product readiness.

### 2. Scope
- **In-Scope Items:**
  - Authentication, Session Management, and Role-Based Access Control (RBAC).
  - Core Business Workflows: [Feature A], [Feature B], and [Feature C].
  - Data Validation: Form boundaries, state persistence, data integrity across browser refreshes.
  - Non-Functional Attributes: Client-side performance, responsive viewports (Desktop & Mobile), basic client-side security hygiene.
- **Out-of-Scope Items:**
  - Destructive DDoS or infrastructure-level volume testing.
  - Source code internal white-box static analysis (inaccessible black-box environment).

### 3. Quality Risk Assessment & Prioritization
1. **Critical Risk (High Impact / High Likelihood):** Financial/transactional calculation errors, silent data loss, authentication bypass, unhandled fatal exceptions (HTTP 500).
2. **Major Risk (High Impact / Medium Likelihood):** Navigation flow breakage, broken checkout/submission workflows, state desynchronization between tabs.
3. **Moderate Risk (Medium Impact / High Likelihood):** Input validation bypass, responsive UI clipping, missing form error feedback.

### 4. Test Strategy & Techniques
- **Specification-Based (Black-Box):**
  - Equivalence Partitioning (EP) & Boundary Value Analysis (BVA) for numeric and string fields.
  - State Transition Testing for multistep workflows and order statuses.
  - Decision Table Testing for complex business rule permutations.
- **Experience-Based:** Error Guessing, Exploratory Testing with charter timeboxing.
- **Non-Functional Testing:** Browser DevTools performance audits, OWASP Top 10 client-side probing, accessibility keyboard navigability.

### 5. Test Environment & Tools
- **Client Environment:** CachyOS Linux (Kernel 6.13+), Chromium / Google Chrome (Latest), Mozilla Firefox (Latest).
- **Diagnostics Tools:** Chrome DevTools (Network, Console, Performance, Lighthouse, Memory profiler).
- **AI Augmentation:** Antigravity / Gemini for rapid test data synthesis and defect classification.

### 6. Entry and Exit Criteria
- **Entry Criteria:** Accessible SUT URL and valid testing credentials provided by MSTB.
- **Exit Criteria:** 100% of critical paths explored; all discovered defects documented with reproducible steps and evidence; Test Summary Report submitted.
```

---

## 📐 Deliverable 2: Test Analysis & Design Template (20 Points)

```markdown
# Test Analysis & Design Matrix: [SUT Application Name]
**Team:** NERV | **Standard:** ISTQB Black-Box Test Design

### 1. Test Conditions & Coverage Map

| Module / Feature | Test Condition ID | Test Condition Description | Risk Rating | Technique Applied |
|---|---|---|---|---|
| Auth / Session | TCND-AUTH-01 | Session expiration and invalid credential handling | Critical | State Transition |
| Input Forms | TCND-VAL-01 | Field length, special characters, and null inputs | Major | BVA + Equivalence Partitioning |
| Workflow Engine | TCND-FLOW-01 | End-to-end user path with valid and invalid permutations | Critical | Decision Table Testing |
| State Management | TCND-STATE-01 | Concurrent tabs, back button navigation, page refreshes | Major | Error Guessing |
| Security Perimeter | TCND-SEC-01 | Client-side input sanitization (XSS, SQLi strings) | Critical | Defect-Based Testing |

### 2. Boundary Value Analysis (BVA) & Partitioning Specifications
- **Field [Field Name] (Allowed: 1 to 100 characters):**
  - *Invalid Partition (< 1):* Empty string `""` -> Expected: Field-level validation error.
  - *Boundary Min (1):* Single character `"A"` -> Expected: Accepted.
  - *Boundary Typical:* 50 alphanumeric characters -> Expected: Accepted.
  - *Boundary Max (100):* Exact 100 characters -> Expected: Accepted.
  - *Invalid Partition (> 100):* 101 characters -> Expected: Blocked or validation error.
  - *Special Chars / Edge Cases:* Emoji `🔥`, Unicode `日本語`, Whitespace-only `"   "`.

### 3. State Transition Model
- State 0 (Unauthenticated) -> State 1 (Active User) -> State 2 (Transaction In-Progress) -> State 3 (Completed).
- *Invalid Transitions Tested:* Direct URL access to State 2 without passing State 1; Double submission on transition State 2 -> 3.
```

---

## 🧪 Deliverable 3: Test Implementation Template (20 Points)

```markdown
# Test Implementation & Procedures: [SUT Application Name]
**Team:** NERV | **Coverage:** Core User Journeys & Critical Paths

### Test Cases Specification Table

| Test Case ID | Traceable Condition | Pre-conditions | Test Steps | Test Data | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| TC-001 | TCND-AUTH-01 | SUT home loaded | 1. Navigate to /login<br>2. Submit empty credentials<br>3. Submit valid user + wrong pass | User: `test_user`<br>Pass: `WrongPass123!` | Visual inline error; no 500 error; password field masked | Inline error shown | PASS |
| TC-002 | TCND-VAL-01 | Valid logged-in session | 1. Open edit profile<br>2. Enter 256 chars in Name field<br>3. Click Save | String: 256 x 'A' | Form alerts user of limit; backend rejects cleanly | Buffer overflow / UI breaks | FAIL (Bug #1) |
| TC-003 | TCND-FLOW-01 | Cart with 1 item | 1. Proceed to checkout<br>2. Rapidly double-click "Place Order"<br>3. Inspect network tab | Valid payment payload | Exactly one order created; button disabled on first click | Duplicate orders created | FAIL (Bug #2) |
| TC-004 | TCND-SEC-01 | Search page | 1. Enter payload in search bar<br>2. Submit search query | `<script>alert(1)</script>` | Query sanitized / HTML-encoded in DOM output | Reflected raw in DOM | FAIL (Bug #3) |
```

---

## 🐞 Deliverable 4: High-Fidelity Bug Report Template (20 Points)

```markdown
### Bug Report: [BUG-00X] [Module Name] Imperative Summary Statement

- **Severity:** [Blocker | Critical | Major | Minor | Trivial] *(ISTQB Definition)*
- **Priority:** [High | Medium | Low]
- **Defect Type:** [Functional | Security | Usability | Performance | Data Integrity]
- **SUT Module:** [e.g. Authentication / Checkout / User Settings]
- **Environment:**
  - OS: Linux CachyOS / Windows 11
  - Browser: Chromium 130.0 / Firefox 132.0 (x86_64)
  - Viewport: 1920x1080 (Desktop) / 390x844 (Emulated Mobile)

#### 1. Short Description
A brief 1-2 sentence executive summary explaining what breaks and the business impact.

#### 2. Pre-conditions & Test Data
- Test Account: `[Username / Role]`
- Application State: `[e.g. Empty cart / Pre-populated profile]`

#### 3. Steps to Reproduce
1. Navigate to `https://[SUT-URL]/[path]`
2. Click on `[Element Name / Button]`
3. Enter `[Exact Test Input]` into `[Field Name]`
4. Click `[Submit / Action Button]`
5. Observe the behavior and inspect DevTools Console / Network tab.

#### 4. Expected Result
State clearly what the application *should* do according to standard business logic, UX principles, or requirements.

#### 5. Actual Result
State exactly what happened (e.g. "Application displays a generic white screen; HTTP 500 Internal Server Error returned by `/api/v1/resource`; Console throws `Uncaught TypeError: Cannot read property 'id' of undefined`").

#### 6. Technical Evidence & Diagnostics
- **HTTP Status Code:** `500 Internal Server Error` (or `400 / 403 / silent failure`)
- **Console Log:**
  ```text
  Uncaught TypeError: e.items.map is not a function at checkout.js:142
  ```
- **Network Payload:**
  - Request: `POST /api/v1/submit` Payload: `{"quantity": -1}`
  - Response: `{"error": "Unhandled Database Exception"}`
- **Attachments:** `[Screenshot_BUG-001.png]` (Attached via platform, <16MB)

#### 7. Business & User Impact
Explain why this matters to the business (e.g. causes revenue leakage, blocks user onboarding, exposes sensitive customer tokens).
```

---

## ⚡ Deliverable 5: Non-Functional Testing Report (20 Points)

```markdown
# Non-Functional Testing Report: [SUT Application Name]
**Team:** NERV | **Scope:** Performance, Client-Side Security, Usability & Accessibility

### 1. Performance & Network Diagnostics
- **Page Load Metrics (Lighthouse / DevTools Network):**
  - Time to First Byte (TTFB): `[X] ms`
  - Largest Contentful Paint (LCP): `[X] s` (Threshold: < 2.5s)
  - Total Blocking Time (TBT): `[X] ms`
  - Cumulative Layout Shift (CLS): `[X]` (Threshold: < 0.1)
- **Network Payload Optimization:**
  - Total transferred size: `[X] MB` across `[Y]` requests.
  - Flaws identified: Uncompressed assets (missing gzip/brotli), unminified JavaScript bundles, excessive redundant polling requests.
- **Client Memory & Resource Consumption:**
  - Memory heap snapshot delta before vs after 10 workflow iterations.
  - Observation: Identified memory leak on DOM re-renders (`[Component Name]`).

### 2. Client-Side Security Hygiene Audit
- **Input Sanitization & Injection Defense:**
  - Tested search and input fields with standard polyglots: `<img src=x onerror=alert(1)>`, `' OR 1=1 --`.
  - Findings: [Cleanly sanitized / Reflected in DOM without encoding].
- **Storage & Secret Leakage:**
  - LocalStorage / SessionStorage inspection: Checked for raw JWT tokens, API keys, or unmasked user PII.
  - Cookie attributes: Checked `Secure`, `HttpOnly`, and `SameSite` flags.
- **Client-Side Authorization Bypass:**
  - Inspected whether hidden UI elements (e.g. Admin controls) can be activated by removing `disabled` or `display: none` in DevTools Elements panel.

### 3. Usability & Accessibility (WCAG 2.1 AA)
- **Keyboard Navigation:** Can the entire core workflow be completed using `Tab`, `Enter`, `Space`, and `Esc` without a mouse?
- **Form Feedback:** Are error messages tied to their corresponding inputs with `aria-describedby`?
- **Responsive Viewport Reflow:**
  - Desktop (1920x1080): Standard baseline.
  - Tablet (768x1024): Horizontal scrollbars or clipped tables?
  - Mobile (375x667): Hamburger menu function, touch targets > 48x48px, overlapping text?
```

---

## 📊 Deliverable 6: Summary Test Report (20 Points)

```markdown
# Summary Test Report: [SUT Application Name]
**Competition:** Malaysia Testing Cup 2026 | **Team:** NERV  
**Release Recommendation:** [REJECT / DO NOT SHIP | CONDITIONAL RELEASE | READY]

### 1. Executive Summary
During the 3-hour intensive testing window, Team NERV conducted comprehensive functional and non-functional evaluation of [SUT Application Name]. A total of `[X]` test cases were executed across `[Y]` core modules. Testing uncovered `[Z]` valid defects, including `[A]` Blocker/Critical vulnerabilities that directly prevent successful user transactions and compromise data integrity.

### 2. Defect Breakdown & Quality Metrics

| Severity | Count | % of Total | Resolution Status |
|---|---|---|---|
| **Blocker** | [X] | [X]% | Requires immediate hotfix before launch |
| **Critical** | [X] | [X]% | Must be resolved before next sprint |
| **Major** | [X] | [X]% | High priority functional fix |
| **Minor** | [X] | [X]% | UI/UX polish |
| **Total** | **[Total]** | **100%** | |

### 3. Module Quality Heatmap
- **Module A (Auth):** Stable (0 Blocker, 1 Minor).
- **Module B (Core Workflow):** High Risk (2 Blockers, 3 Critical).
- **Module C (Reporting/Exports):** Moderate Risk (1 Major).

### 4. Residual Risks & Stakeholder Impact
1. **Transaction Integrity:** Risk of duplicate billing or orphaned database records under concurrent user clicks.
2. **Data Privacy:** Risk of PII leakage via unauthenticated API endpoint parameters.
3. **Cross-Platform Compatibility:** Mobile web viewports fail to render submission modals, preventing smartphone conversions.

### 5. Final Recommendation
- **Verdict: DO NOT SHIP (NO-GO)** until all Blocker and Critical defects documented in Deliverable 4 are remediated and regression-tested.
```

---

## 🤖 Deliverable 7 & 8: Smart AI Use & Exceptional Performance (10 Bonus Points)

- **Smart AI Use (5 Points):**
  - Document *how* AI was leveraged as an engineering multiplier:
    - Generated equivalence partitions and edge-case boundary data.
    - Synthesized regex patterns for fuzzing input fields.
    - Cross-referenced observed API behaviors against RFC HTTP specifications.
  - Explicit statement: Every defect was manually reproduced, verified, and diagnosed in live DevTools before submission; zero hallucinated bugs.
- **Exceptional Performance (5 Points):**
  - Isolate the "Golden Bug": An architectural flaw, subtle race condition, or security loophole that typical testers miss (e.g. negative quantity injection causing inverse billing, race condition in inventory decrement, state corruption via browser back-forward cache).

---

## 🧰 Automated CLI Testing Suite (`Competitions/scripts/`)

These surgical, high-speed CLI tools are pre-configured to run against any SUT URL during the live window:

| Script | Purpose | Command Syntax |
|---|---|---|
| **SUT Crawler & Console Sniffer** | Captures DOM forms, buttons, inputs, unhandled JS errors, failed HTTP 4xx/5xx requests, and full-page screenshot. | `node Competitions/scripts/crawler.js "<URL>"` |
| **WCAG 2.1 AA Accessibility Engine** | Full Axe-core audit listing broken WCAG rules, exact HTML selectors, impact level, and fixes for Deliverable 5 (20 pts). | `node Competitions/scripts/audit_accessibility.js "<URL>"` |
| **HTTP Security & CORS Prober** | Audits CSP, Clickjacking, HSTS, MIME headers, CORS wildcard reflection, and cookie `HttpOnly`/`Secure` flags. | `python3 Competitions/scripts/security_probe.py "<URL>"` |
| **Sensitive Route Recon** | Probes non-destructively for exposed Swagger/OpenAPI docs, `.env`, `.git`, Actuator endpoints, and `/admin` routes. | `python3 Competitions/scripts/security_probe.py "<URL>" --recon` |
| **JWT Token Inspector & Forger** | Decodes JWT claims, checks for missing expiration, and generates a forged `alg: none` bypass token. | `python3 Competitions/scripts/security_probe.py --jwt "<TOKEN>"` |
| **Fuzz & Test Data Generator** | Instant BVA strings, XSS payloads, SQLi, Unicode edge cases, with auto-copy to Wayland clipboard (`wl-copy`). | `python3 Competitions/scripts/fuzz_gen.py --type <type> --len <N> --copy` |

