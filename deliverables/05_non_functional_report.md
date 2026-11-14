# Deliverable 5: Non-Functional Testing Report (Meja Marmar)
**Competition:** Malaysia Testing Cup 2026  
**Team:** NERV | **Lead Tester:** Mohamed Makhlouf  
**System Under Test:** Meja Marmar (`MEJ-FRS-001 v1.0`)  
**Scope:** Security & Authorization (`MEJ-SEC-01` to `MEJ-SEC-06`), Accessibility & Keyboard Usability (`MEJ-SEC-05`, WCAG 2.1 AA), Responsive & Viewport Compliance (`MEJ-SEC-07`), and Infrastructure HTTP Hardening

---

## 1. Executive Non-Functional Summary

Non-functional testing of **Meja Marmar** (`MEJ-FRS-001 v1.0`) uncovered **12 verified non-functional defects** (`DEF-001`, `DEF-007`, `DEF-009`, `DEF-011`, `DEF-012`, `DEF-013`, `DEF-014`, `DEF-015`, `DEF-021`, `DEF-022`, `DEF-024`, `DEF-026`) across security, concurrency, accessibility, keyboard usability, and responsive viewport compliance, alongside **3 HTTP header hardening gaps**. While Dapur RBAC, dual Diner/Staff session isolation, deactivation revocation, XSS/reflected-HTML escaping, 12/12 `MEJ-SEC-06` confirmation dialogs, tray payment/ticket-cancel concurrency locks, and cookie security flags passed verification, **critical object-level authorization (IDOR), open redirect, and concurrent top-up race condition vulnerabilities** expose diner data, order state, and wallet balance limits.

| Category | Req. Coverage | Verified Failures | Verified Passes | Overall Status |
|---|---|---|---|---|
| **Security, Concurrency & Authorization** | `MEJ-SEC-01` to `MEJ-SEC-06` | `DEF-001`, `DEF-011`, `DEF-012`, `DEF-013`, `DEF-024`, `DEF-026` + 3 Header Gaps | Dapur RBAC (`403`), Dual Session Isolation, Deactivation Revocation, XSS/Reflected Escaping, 12/12 Confirmation Dialogs (`MEJ-SEC-06`), Tray Pay/Ticket-Cancel Concurrency, Cookie/TLS Flags | **FAIL (Critical Risk)** |
| **Accessibility & Keyboard Usability** | `MEJ-SEC-05`, WCAG 2.1 AA | `DEF-007`, `DEF-014`, `DEF-021`, `DEF-022` | `Tab`+`Space` Tray Drag/Drop, 100% Image `alt` Text (WCAG 1.1.1), Form `<label>` Associations | **FAIL (Major Risk)** |
| **Responsive & Viewport Compliance** | `MEJ-SEC-07`, WCAG 1.4.10 | `DEF-009`, `DEF-015` | Dapur Portal Reflow at `1024px` and `200%` Zoom (`640px`) | **FAIL (Major Risk)** |

---

## 2. Security & Authorization Assessment (`MEJ-SEC-01` to `MEJ-SEC-06`)

### 2.1 Verified Security Failures

| Defect ID | Severity | Requirement | Endpoint / Component | Verified Finding & Impact |
|---|---|---|---|---|
| **DEF-011** | **Blocker** | `MEJ-SEC-01`, `MEJ-REF-03` | Diner Ticket Cancel (`POST /trays/{id}/tickets/{tid}/cancel`) | **IDOR Write + Full-Tray Over-Refund:** Any authenticated diner can cancel a `New` ticket belonging to another diner's tray via direct ID manipulation. Worse, cancelling a single ticket credits the **entire tray total** rather than the ticket's line value, enabling unauthorized disruption and balance inflation. |
| **DEF-001** | **Critical** | `MEJ-SEC-01` | `GET /sut/mejamarmar/trays/{id}` | **IDOR Read (BOLA):** Sequential numeric tray IDs lack server-side ownership checks. Any authenticated diner can enumerate `/trays/{id}` to view other diners' orders, table numbers, hall selections, payment codes, and billing totals. |
| **DEF-012** | **Critical** | `MEJ-SEC-01`, `MEJ-PAY-05` | Diner Edit Tray (`POST /trays/{id}/edit` / `cancel`) | **IDOR Edit-Tray Hijack:** Any authenticated diner can hijack and cancel another diner's `Awaiting payment` tray via the Edit Tray flow by targeting the victim's tray ID, forcing unintended order cancellation and queue loss. |
| **DEF-013** | **Critical** | `MEJ-ACC-01`, `MEJ-SEC-06` | Diner Sign-In (`?next=https://evil.com`) | **Open Redirect on Sign-In:** The `next` query parameter on the sign-in endpoint accepts arbitrary external URLs without allowlist or same-origin validation, redirecting authenticated diners directly to external phishing domains (e.g., `https://evil.com`). |
| **DEF-024** | **Critical** | `MEJ-BAL-02`, `MEJ-SEC-06` | Dapur Top-Up (`POST /dapur/topups/{id}`) | **Concurrent Top-Up Race Condition:** Parallel `RM10.00` top-up `POST` requests (`Promise.all`) bypass the `RM500.00` balance cap (`RM490.00 -> RM510.00`) due to missing atomic locking / serialization. |

### 2.2 Infrastructure & HTTP Security Headers (`security_probe.py`)

Automated header reconnaissance via `python3 scripts/security_probe.py` identified the following HTTP hardening gaps alongside confirmed baseline protections:

- **Findings (Hardening Gaps):**
  1. **Server Version Disclosure:** Response includes `Server: nginx/1.26.3 (Ubuntu)`, exposing exact web server software and OS distribution to attackers.
  2. **Missing `Content-Security-Policy` (CSP):** No CSP header is returned, leaving the application without defense-in-depth script execution or framing restrictions if an injection vector is introduced.
  3. **Missing `Permissions-Policy`:** Browser feature permissions (camera, microphone, geolocation) are not explicitly restricted via `Permissions-Policy`.

- **Confirmed Baseline Headers & Cookie Flags:**
  - `Strict-Transport-Security` (HSTS) is present.
  - `X-Frame-Options: SAMEORIGIN` is enforced (clickjacking mitigation).
  - `X-Content-Type-Options: nosniff` is enforced (MIME-sniffing mitigation).
  - Session cookies enforce `HttpOnly`, `Secure`, and `SameSite=Lax`.

### 2.3 Verified Security & Auth Passes

| Control Area | Requirement | Verification Result | Observed Evidence |
|---|---|---|---|
| **Dapur RBAC Enforcement** | `MEJ-DAP-01`, `MEJ-SEC-02` | **PASS** | Cook accounts are strictly restricted to their assigned stall; Cashier accounts cannot access Manager CRUD routes; unauthorized Dapur routes return `403 Forbidden` / redirect. |
| **Dual Session Isolation** | `MEJ-ACC-05` | **PASS** | Simultaneous Diner and Dapur Staff sign-ins in the same browser maintain isolated session cookies and contexts without privilege bleed or cross-role contamination. |
| **Password Reset & Deactivation Revocation** | `MEJ-ACC-04` | **PASS** | Deactivating a staff account or resetting credentials immediately invalidates active sessions on subsequent requests. |
| **XSS Output Escaping** | `MEJ-SEC-04` | **PASS** | Payloads such as `<img src=x onerror=alert(1)>` submitted in dish notes, board messages, and profile fields are HTML-escaped and rendered strictly as literal text-as-typed without script execution. |
| **Server-Side Input & Price Validation** | `MEJ-SEC-03` | **PASS** | Tampered `POST` parameters for dish quantities (outside `1` to `9`) and out-of-service/invalid table numbers are rejected server-side. |
| **PRG Redirects & Concurrency Idempotency** | `MEJ-SEC-06` | **PASS** | State-changing `POST` requests follow Post/Redirect/Get (PRG) to prevent duplicate form resubmission on browser refresh; concurrent ticket cancellation requests are handled idempotently without double-refunding the same ticket. |

---

## 3. Accessibility & Keyboard Usability (`MEJ-SEC-05`, WCAG 2.1 AA)

### 3.1 Verified Accessibility & Keyboard Failures

| Defect ID | Severity | Requirement / WCAG | Component | Verified Finding & Impact |
|---|---|---|---|---|
| **DEF-007** | **Major** | `MEJ-SEC-05` | Kitchen Display (`/dapur/kitchen/{id}`) | **Shortcuts Advance Multiple Tickets:** Pressing `S`, `C`, or `H` advances multiple tickets simultaneously instead of advancing only the single oldest ticket in the target column, causing accidental state jumps during rush service. |
| **DEF-014** | **Major** | `MEJ-SEC-05`, `MEJ-TRY-03` | Diner My Tray (`/tray`) | **Missing Single-Click `Tapau` / `Dine in` Buttons:** Tray line items lack single-click toggle buttons for switching between `Dine in` and `Tapau`, forcing pointer users to rely solely on drag-and-drop (violating WCAG 2.5.7 Dragging Movements). |
| **DEF-021** | **Major** | `MEJ-SEC-05` | Kitchen Display (`"Message on the board"`) | **Shortcuts Fire Inside Text Input:** Global `S`, `C`, and `H` keyboard shortcut listeners do not check `document.activeElement` / input focus. Typing words containing `s`, `c`, or `h` inside `"Message on the board"` triggers ticket state transitions while typing. |
| **DEF-022** | **Minor** | WCAG 1.3.1 / 2.4.6 | Kitchen Display (`/dapur/kitchen/{id}`) | **Missing `<h1>` Landmark Heading:** The Kitchen Display page omits a top-level `<h1>` heading, breaking semantic heading hierarchy for screen reader navigation. |

### 3.2 Verified Accessibility Passes

- **Keyboard Tray Drag/Drop (`MEJ-TRY-03`):** Moving items between `Dine in` and `Tapau` containers via `Tab` and `Space` keys works reliably with clear focus indication.
- **Image Alternative Text (WCAG 1.1.1):** Automated and DOM inspection across audited Diner and Dapur views confirmed 100% of `<img>` elements include descriptive `alt` attributes.
- **Form Label Associations (WCAG 1.3.1 / 3.3.2):** Input controls across audited sign-in, tray, and Dapur forms maintain valid `<label>` associations.

---

## 4. Responsive & Viewport Compliance (`MEJ-SEC-07`, WCAG 1.4.10)

### 4.1 Verified Viewport Failures

| Defect ID | Severity | Viewport / Zoom | Component | Verified Finding & Impact |
|---|---|---|---|---|
| **DEF-009** | **Major** | `375px` Mobile | Diner `/` & `/tray` | **Fixed `1000px` Container Overflow:** Diner storefront and tray pages use a fixed `1000px` layout width, overflowing a `375px` mobile viewport by `625px` horizontally and pushing `Tray total` and the `Go to Send tray` CTA off-screen. |
| **DEF-015** | **Major** | `1280px` at `200%` Zoom (`640px` effective) | Diner `/stalls` | **5-Column Grid Overflow:** The `/stalls` 5-column grid does not wrap or reflow at `640px` effective width (`200%` zoom in a `1280px` window), clipping Stalls 5 and 10 horizontally. |

### 4.2 Verified Responsive Passes

- **Dapur Portal Reflow:** All audited Dapur staff and management pages reflow cleanly at `1024px` desktop width and at `200%` browser zoom (`640px` effective width) with zero horizontal overflow or clipped controls.

---

## 5. Non-Functional Risk & Remediation Summary

1. **Immediate Security Fixes (Pre-Release Mandatory):**
   - Enforce server-side `tray.diner_id == current_diner.id` ownership checks on all `/trays/{id}` read, edit, and ticket-cancel endpoints (`DEF-001`, `DEF-011`, `DEF-012`).
   - Restrict `?next=` sign-in redirects to relative same-origin paths only (`DEF-013`).
   - Suppress the `Server` version banner (`server_tokens off;`) and add `Content-Security-Policy` and `Permissions-Policy` headers in Nginx.
2. **Accessibility & Responsive Fixes:**
   - Guard KDS `S`/`C`/`H` keyboard listeners when focus is inside `<input>`, `<textarea>`, or `<select>` (`DEF-021`), and limit each shortcut press to the single oldest ticket (`DEF-007`).
   - Add single-click `Tapau` / `Dine in` buttons on tray lines (`DEF-014`) and an `<h1>` heading on Kitchen Display (`DEF-022`).
   - Replace fixed `1000px` containers and rigid 5-column grids with responsive CSS breakpoints (`DEF-009`, `DEF-015`).
