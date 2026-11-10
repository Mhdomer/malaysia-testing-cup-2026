# Deliverable 1: Test Plan
**Competition:** Malaysia Testing Cup 2026  
**Team:** NERV | **Lead:** Mohamed Makhlouf  
**Standard:** ISO/IEC/IEEE 29119-3 / ISTQB CTFL

### 1. Context & Objectives
- **System Under Test (SUT):** [Pending URL reveal]
- **Objective:** Independent black-box quality, resilience, and security assessment under release-candidate constraints.

### 2. Scope
- **In-Scope:** Authentication, core transactional workflows, input validation boundaries, client performance, and security hygiene.
- **Out-of-Scope:** Destructive infrastructure volume attacks (DDoS) and internal source code static analysis.

### 3. Quality Risks & Prioritization
1. **Critical:** Transactional calculation errors, silent data loss, broken access control.
2. **Major:** Workflow navigation interruptions, unhandled server exceptions (HTTP 500).
3. **Moderate:** Responsive viewports, client input validation error messaging.

### 4. Test Strategy & Techniques
- **Black-Box:** Equivalence Partitioning (EP), Boundary Value Analysis (BVA), State Transition Testing, Decision Tables.
- **Non-Functional:** Axe-core WCAG 2.1 AA accessibility, HTTP security header compliance, DevTools network latency analysis.

### 5. Environment & Tools
- Client: CachyOS Linux (Kernel 6.13+), Chromium 156.0.
- Diagnostics: Chrome DevTools, Puppeteer automation, Python audit suite.
