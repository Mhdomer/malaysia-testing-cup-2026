# Deliverable 6: Summary Test Report (Meja Marmar)
**Competition:** Malaysia Testing Cup 2026  
**Team:** NERV | **Lead Tester:** Mohamed Makhlouf  
**System Under Test:** Meja Marmar (`MEJ-FRS-001 v1.0`)  
**Standard:** ISO/IEC/IEEE 29119-3 Test Completion Report  
**Release Recommendation:** **DO NOT SHIP (NO-GO)**

---

## 1. Executive Summary

Team **NERV** conducted a black-box functional, financial, security, accessibility, and responsive assessment of **Meja Marmar** (`MEJ-FRS-001 v1.0`) across the Diner storefront, Dapur staff/management portal, and public Split-Flap Queue Board.

Testing uncovered **27 verified defects** (`DEF-001` through `DEF-027`), including **4 Blockers**, **12 Critical**, **10 Major**, and **1 Minor** defect. While Dapur role-based access control (RBAC), dual session isolation, XSS/reflected-HTML escaping, 12/12 `MEJ-SEC-06` confirmation dialogs, typed amount parsing, and tray/ticket concurrency locks functioned as specified, the release candidate suffers from **severe financial accounting exploits**, **broken object-level authorization (IDOR)**, **tax/container calculation errors**, **closed-stall ordering bypasses**, and a **concurrent wallet top-up race condition**. Specifically, any diner can multiply their wallet balance `2x` to `5x` via multi-stall ticket refunds (`DEF-018`), cancel and over-refund another diner's tickets (`DEF-011`, `DEF-026`), cancel `Paid` trays without triggering refunds (`DEF-005`), read or hijack other diners' trays (`DEF-001`, `DEF-012`), bypass `Busy` and `Close for today` stall protections (`DEF-019`, `DEF-020`, `DEF-027`), underpay `.xx5` 6% Service tax (`DEF-023`) and multi-unit Tapau container fees (`DEF-025`), and exceed the `RM500.00` wallet cap under concurrent top-ups (`DEF-024`).

**Stakeholder Decision:** **DO NOT SHIP (NO-GO)**. Deploying this build to production would expose the food court to immediate financial loss, unauthorized order tampering, and regulatory/accounting discrepancies.

---

## 2. Defect Severity Distribution (27 Verified Defects)

| Severity | Count | Percentage | Defect IDs |
|---|---:|---:|---|
| **Blocker** | 4 | 14.8% | `DEF-005`, `DEF-011`, `DEF-018`, `DEF-026` |
| **Critical** | 12 | 44.4% | `DEF-001`, `DEF-002`, `DEF-006`, `DEF-010`, `DEF-012`, `DEF-013`, `DEF-016`, `DEF-019`, `DEF-020`, `DEF-023`, `DEF-024`, `DEF-027` |
| **Major** | 10 | 37.0% | `DEF-003`, `DEF-004`, `DEF-007`, `DEF-008`, `DEF-009`, `DEF-014`, `DEF-015`, `DEF-017`, `DEF-021`, `DEF-025` |
| **Minor** | 1 | 3.7% | `DEF-022` |
| **Total** | **27** | **100.0%** | `DEF-001` to `DEF-027` |

---

## 3. Complete Defect Breakdown Table (`DEF-001` to `DEF-027`)

| ID | Severity | Module / Area | Verified Summary |
|---|---|---|---|
| **DEF-011** | **Blocker** | Security / Refunds | IDOR write + full-tray over-refund on single ticket cancellation (`MEJ-SEC-01`, `MEJ-REF-03`) |
| **DEF-018** | **Blocker** | Refunds / Balance | Multi-stall ticket cancellation refunds full tray total per ticket, enabling `2x` to `5x` balance multiplication (`MEJ-REF-03`, `MEJ-TKT-03`) |
| **DEF-001** | **Critical** | Security / IDOR | IDOR read on `/sut/mejamarmar/trays/{id}` exposes other diners' trays, orders, and billing (`MEJ-SEC-01`) |
| **DEF-002** | **Critical** | Payments / Rounding | Cashier 5-sen rounding rounds `6` and `7` sen up instead of down (`MEJ-PAY-02`) |
| **DEF-005** | **Critical** | Payments / State | `Paid` tray can be cancelled via `"Cancel unpaid tray"`, bypassing refund flow (`MEJ-PAY-05`) |
| **DEF-006** | **Critical** | Kitchen / Tickets | `"Sold out"` action offered and accepted on `Ready` tickets, violating ticket state machine (`MEJ-TKT-02`, `MEJ-REF-01`) |
| **DEF-010** | **Critical** | Dapur / Accounting | Today's `"Takings in cash"` sums unrounded tray totals instead of actual 5-sen rounded cash taken (`MEJ-DAP-07`) |
| **DEF-012** | **Critical** | Security / IDOR | IDOR allows any diner to hijack and cancel another diner's `Awaiting payment` tray via Edit Tray (`MEJ-SEC-01`, `MEJ-PAY-05`) |
| **DEF-013** | **Critical** | Security / Auth | Open redirect on diner sign-in via `?next=https://evil.com` query parameter (`MEJ-ACC-01`, `MEJ-SEC-06`) |
| **DEF-016** | **Critical** | Tickets / Board | Queue number after `999` increments to `1000` instead of rolling over to `001`, rendering as `"0 0 0"` on Split-Flap Board (`MEJ-TKT-01`, `MEJ-BRD-02`) |
| **DEF-019** | **Critical** | Payments / Stalls | Cashier `"Take payment"` bypasses `Busy` stall check and accepts orders on `Busy` stalls (`MEJ-STL-04`, `MEJ-PAY-02`) |
| **DEF-020** | **Critical** | Payments / Stalls | Diner `"Send tray"` balance payment bypasses `Busy` stall check (`MEJ-STL-04`, `MEJ-PAY-01`) |
| **DEF-003** | **Major** | Promotions | Teh Tarik Hour applies 2-cup RM1.50 limit per dish line instead of per tray and discounts cheaper cup (`MEJ-TEH-03`) |
| **DEF-004** | **Major** | Diner Tray | Off-by-one limit blocks adding dishes from a 5th distinct stall to a tray (`MEJ-TRY-02`) |
| **DEF-007** | **Major** | Kitchen / A11y | Kitchen Display single-key shortcuts `S`, `C`, `H` advance multiple tickets simultaneously (`MEJ-SEC-05`) |
| **DEF-008** | **Major** | Kitchen / Stalls | Stall closure refusal undercounts open tickets by excluding `Ready` tickets (`MEJ-STL-04`) |
| **DEF-009** | **Major** | Responsive UI | Diner `/` and `/tray` fixed `1000px` width overflows `375px` mobile by `625px`, pushing `Tray total` and `Go to Send tray` off-screen (`MEJ-SEC-07`) |
| **DEF-014** | **Major** | Accessibility / UI | Missing single-click `"Tapau"` and `"Dine in"` buttons on tray lines (`MEJ-SEC-05`, `MEJ-TRY-03`) |
| **DEF-015** | **Major** | Responsive UI | `/stalls` 5-column grid overflows `640px` effective viewport at 200% zoom (`1280px` window), clipping Stalls 5 and 10 (`MEJ-SEC-07`) |
| **DEF-017** | **Major** | Kitchen / Tickets | `"Sold out"` action offered and accepted on final `Cancelled` tickets, transitioning state to `Refunded` (`MEJ-TKT-02`, `MEJ-REF-01`) |
| **DEF-021** | **Major** | Kitchen / A11y | Kitchen Display `S`, `C`, `H` shortcuts fire while typing inside `"Message on the board"` text input (`MEJ-SEC-05`) |
| **DEF-022** | **Minor** | Accessibility | Missing `<h1>` landmark heading on Kitchen Display (`WCAG 1.3.1`, `WCAG 2.4.6`) |
| **DEF-023** | **Critical** | Totals / Tax | 6% Service tax rounds `.xx5` half-sen values down instead of half-up, undercharging tax by `RM0.01` (`MEJ-TOT-04`) |
| **DEF-024** | **Critical** | Concurrency / Balance | Concurrent `RM10.00` top-up `POST` requests bypass `RM500.00` wallet cap (`RM490.00 -> RM510.00`) (`MEJ-BAL-02`) |
| **DEF-025** | **Major** | Totals / Containers | Tapau container fee charges `RM0.30` per Tapau line instead of `RM0.30` per dish unit on the line (`MEJ-TOT-02`) |
| **DEF-026** | **Blocker** | Security / IDOR | Authenticated diner can access `/trays/{id}` and destructively cancel another diner's paid ticket (`POST /trays/{id}/tickets/{tid}/cancel`) (`MEJ-SEC-01`) |
| **DEF-027** | **Critical** | Stalls / Business Logic | `Send tray` succeeds and issues an active tray and pay code for a stall marked `Closed today` via `Close for today` (`MEJ-STL-04`) |

---

## 4. Module Quality Heatmap

| Module / Functional Area | Risk Rating | Defect Count | Key Failures | Verified Passes / Strengths |
|---|---|---:|---|---|
| **Security & IDOR** | **RED (Critical)** | 4 (`DEF-001`, `DEF-011`, `DEF-012`, `DEF-013`) | Unauthenticated/cross-diner tray read, edit-tray hijack, ticket cancel IDOR, sign-in open redirect, missing CSP/Permissions-Policy | XSS escaping (`MEJ-SEC-04`), PRG & concurrency idempotency (`MEJ-SEC-06`), HSTS, `X-Frame-Options`, `HttpOnly`/`Secure`/`SameSite=Lax` cookies |
| **Payments, Rounding & Refunds** | **RED (Critical)** | 6 (`DEF-002`, `DEF-005`, `DEF-010`, `DEF-018`, `DEF-019`, `DEF-020`) | `2x` to `5x` multi-stall refund exploit, BNM 5-sen rounding error (`6`/`7` sen up), `Paid` tray cancel bypassing refund, unrounded cash takings sum, `Busy` stall bypasses | Server-side qty/table POST validation (`MEJ-SEC-03`), concurrent cancel idempotency |
| **Kitchen, Tickets & Board** | **RED (High)** | 6 (`DEF-006`, `DEF-007`, `DEF-008`, `DEF-016`, `DEF-017`, `DEF-021`) | Queue `999 -> 1000` (`"0 0 0"` on Board), `"Sold out"` on `Ready`/`Cancelled` tickets, `Ready` tickets excluded from closure count, KDS shortcut multi-advance & input capture | Standard `New -> Cooking -> Ready -> Collected` happy-path flow |
| **Diner Tray & Teh Tarik** | **AMBER (Medium-High)** | 2 (`DEF-003`, `DEF-004`) | Teh Tarik 2-cup limit applied per line instead of per tray; off-by-one 4-stall cap blocks 5th stall | Keyboard `Tab`+`Space` tray drag/drop (`MEJ-TRY-03`) |
| **Responsive & Accessibility** | **AMBER (Medium-High)** | 4 (`DEF-009`, `DEF-014`, `DEF-015`, `DEF-022`) | Fixed `1000px` mobile overflow, `/stalls` 200% zoom clipping, missing single-click `Tapau`/`Dine in` buttons, missing KDS `<h1>` | Dapur portal clean reflow at `1024px` and `200%` zoom; 100% image `alt` text; form `<label>` associations |
| **Dapur RBAC & Admin** | **GREEN (Pass)** | 0 | No defects found in RBAC boundaries or session management | Cook stall isolation (`MEJ-DAP-01`, `MEJ-SEC-02`), dual Diner+Staff session isolation (`MEJ-ACC-05`), immediate deactivation revocation (`MEJ-ACC-04`) |

---

## 5. Stakeholder Release Recommendation: DO NOT SHIP (NO-GO)

### 5.1 Blocking Release Criteria Failed
The current release candidate **cannot be approved for production** due to the following release-blocking failures:
1. **Direct Financial Exploitation (`DEF-018`, `DEF-011`, `DEF-005`):** Diners can artificially inflate wallet balances `2x` to `5x` by cancelling tickets on multi-stall trays, trigger full-tray refunds on other diners' trays via IDOR, and cancel already-`Paid` trays without triggering refunds.
2. **Accounting & Regulatory Non-Compliance (`DEF-002`, `DEF-010`):** Cash billing violates Bank Negara Malaysia 5-sen rounding rules on `6` and `7` sen totals, and daily cash takings report unrounded totals that do not reconcile with actual cash collected.
3. **Cross-User Authorization Failures (`DEF-001`, `DEF-011`, `DEF-012`):** Missing ownership checks on `/trays/{id}` allow any diner to enumerate, view, hijack, and cancel other diners' active orders.
4. **Operational & Queue Integrity Failures (`DEF-016`, `DEF-019`, `DEF-020`, `DEF-006`):** Queue rollover breaks at `999` (`"0 0 0"` on the public Board), and `Busy` stall throttling is bypassed on both Diner balance and Cashier payment paths.

### 5.2 Path to Release (Recommended Exit Gates)
Before re-testing for a Go/No-Go decision, engineering must:
1. Fix all **2 Blockers** (`DEF-011`, `DEF-018`) and **10 Critical** defects (`DEF-001`, `DEF-002`, `DEF-005`, `DEF-006`, `DEF-010`, `DEF-012`, `DEF-013`, `DEF-016`, `DEF-019`, `DEF-020`).
2. Add automated regression tests covering tray ownership authorization, multi-stall partial ticket refunds, BNM 5-sen rounding across `0` to `9` sen endings, and queue `999 -> 001` rollover.
3. Remediate **Major** responsive, accessibility, and promotional logic defects (`DEF-003`, `DEF-004`, `DEF-007` to `DEF-009`, `DEF-014`, `DEF-015`, `DEF-017`, `DEF-021`) and harden Nginx headers (`server_tokens off`, `Content-Security-Policy`, `Permissions-Policy`).
