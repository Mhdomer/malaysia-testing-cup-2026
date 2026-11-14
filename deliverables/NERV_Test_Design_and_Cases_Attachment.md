# Test Design & Test Cases Attachment: Meja Marmar
**Competition:** Malaysia Testing Cup 2026 (National Pre-Qualifier to World's Best Tester)
**Platform Submission:** World Best Tester Test Plan Attachment (/participant/test-plan/16)
**Team:** NERV | **Lead Tester:** Mohamed Makhlouf
**Specification Reference:** MEJ-FRS-001 v1.0
**Standards:** ISO/IEC/IEEE 29119-3 & ISTQB CTFL Black-Box Test Design

---

## Document Overview
This attachment provides the complete specification-based test design artifacts and detailed test implementation procedures supporting Deliverable 1 (Test Plan) for Team NERV:
- Part 1: Deliverable 2: Test Analysis & Design Matrix (Test Conditions, EP/BVA Tables, State Transition Models, Decision Tables, and Security Conditions)
- Part 2: Deliverable 3: Test Implementation & Procedures (Detailed Test Cases TC-001 through TC-008 with step-by-step actions, test data, and expected outcomes)
- Part 3: Smart Use of AI Tools (Engineering Multiplier, test data synthesis, automated diagnostic tooling, and human-in-the-loop verification policy)

---

## PART 1: TEST ANALYSIS & DESIGN MATRIX (DELIVERABLE 2)

# Test Analysis & Design Matrix: Meja Marmar (Medan Selera Meja Marmar & Dapur)
**Competition:** Malaysia Testing Cup 2026  
**Team:** NERV | **Lead Tester:** Mohamed Makhlouf  
**Specification Reference:** MEJ-FRS-001 v1.0  
**Standard:** ISTQB CTFL Black-Box Test Design (EP, BVA, State Transition, Decision Table)  

---

### 1. Test Conditions & Coverage Map

| Module / FRS Ref | Test Condition ID | Test Condition Description | Risk Rating | Technique Applied |
|---|---|---|---|---|
| **MEJ-CTR-03** | TCND-CTR-01 | Table number range (1 to 120), hall mapping, out-of-service enforcement (40, 101), and max 6 open trays per table | Critical | EP + BVA |
| **MEJ-TRY-01 / 02** | TCND-TRY-01 | Dish quantity limits (1 to 9), Dine-in + Tapau merge cap (<= 9), and max 5 distinct stalls per tray | Critical | EP + BVA |
| **MEJ-STL-02 / DAP-03** | TCND-PRC-01 | Dish price boundaries (RM0.50 to RM99.90 in 10-sen steps) and typed amount format parsing (Section 1) | Critical | EP + BVA |
| **MEJ-BAL-02** | TCND-BAL-01 | Diner balance top-up in RM10.00 steps, RM500.00 wallet cap, and refund cap bypass | Critical | EP + BVA |
| **MEJ-ACC / TRY / BRD / DAP** | TCND-TXT-01 | Text field length limits and character set rules across Diner, Tray, Board, and Dapur Admin | Major | EP + BVA |
| **MEJ-TEH-01 to 04** | TCND-TEH-01 | Teh Tarik Hours window duration (30m to 3h), max 4 non-overlapping windows, max 2 dearest cups at RM1.50 | Major | EP + BVA + Error Guessing |
| **MEJ-PAY-02** | TCND-PAY-01 | Cash 5-sen rounding rules across all last sen digits (0 to 9) and exact Balance payment | Critical | EP + BVA |
| **Section 16** | TCND-ST-01 | Tray lifecycle transitions (`Draft`, `Awaiting payment`, `Paid`, `Cancelled`, `Complete`) and Edit tray loop | Critical | State Transition Testing |
| **MEJ-TKT-02** | TCND-ST-02 | Ticket lifecycle transitions (`New`, `Cooking`, `Ready`, `Collected`, `Cancelled`, `Refunded`) | Critical | State Transition Testing |
| **MEJ-TOT-01 to 05** | TCND-TOT-01 | Totals, Tapau containers (RM0.30), 10% Service charge (Dewan Sejuk Dine-in only), and 6% half-up Service tax | Critical | Decision Table Testing |
| **MEJ-SEC** | TCND-SEC-01 | Own-tray IDOR, Dapur RBAC (Cook/Cashier/Manager), XSS encoding, PRG double-submit, and concurrency | Critical | Defect-Based + Error Guessing |

---

### 2. Equivalence Partitioning (EP) & Boundary Value Analysis (BVA) Table

| Field / Rule (FRS Ref) | Valid Partitions & Boundaries | Invalid Partitions & Boundaries | Expected System Behaviour |
|---|---|---|---|
| **Table Number** (`MEJ-CTR-03`) | Min: `1` (Laman, In use)<br>Hall boundary: `80` (Laman), `81` (Dewan Sejuk), `116` (Dewan Sejuk), `117` (Laman)<br>Max: `120` (Laman, In use)<br>Open trays on table: `0`, `5` | Below min: `0`, `-1`<br>Above max: `121`<br>Non-integer: `12.5`, `abc`, `""`<br>Out of service: `40`, `101`<br>Capacity reached: Table with `6` open trays | Valid in-use tables with `< 6` open trays are accepted and assigned correct hall service mode; invalid, out-of-service (`40`, `101`), or full (`6` open trays) tables are rejected with clear error. |
| **Dish Quantity** (`MEJ-TRY-01`) | Min: `1`<br>Typical: `5`<br>Max: `9`<br>Merge Dine-in + Tapau same dish: `4 + 5 = 9` | Below min: `0`, `-1`<br>Above max: `10`<br>Merge overflow: `5 + 5 = 10`<br>Non-integer: `1.5`, `abc` | Quantities `1` to `9` accepted; `0` removes line or is blocked on add; `>= 10` or Dine-in + Tapau merge exceeding `9` is rejected without corrupting tray totals. |
| **Stall Count per Tray** (`MEJ-TRY-02`) | Min: `1` stall<br>Typical: `3` stalls<br>Max: `5` stalls (including multiple dishes from same 5 stalls) | Above max: Adding dish from a `6th` distinct stall | Up to `5` distinct stalls allowed in one tray; adding a dish from a `6th` stall is blocked with an inline limit message. |
| **Dish Price** (`MEJ-STL-02` / `MEJ-DAP-03`) | Min: `RM0.50`<br>Step: `RM0.60`, `RM12.30`<br>Max: `RM99.90` | Below min: `RM0.40`, `RM0.00`, `-RM1.00`<br>Above max: `RM100.00`<br>Invalid step: `RM1.05`, `RM1.01`, `RM12.99` | Prices from `RM0.50` to `RM99.90` in `RM0.10` steps saved; out-of-range or non-10-sen step values rejected at both UI and server. |
| **Top-up Amount** (`MEJ-BAL-02`) | Step: `RM10.00`, `RM20.00`, `RM50.00`<br>Cap boundary: Balance `RM490.00` + `RM10.00` = `RM500.00` | Non-RM10 step: `RM5.00`, `RM15.00`, `RM10.50`, `RM0.00`, `-RM10.00`<br>Cap overflow: Balance `RM490.00` + `RM20.00` = `RM510.00`, Balance `RM491.00` + `RM10.00` = `RM501.00` | Only `RM10.00` multiples keeping balance `<= RM500.00` succeed; `RM500.01+` or non-RM10 steps rejected. (Note: Refunds may still push balance above `RM500.00`.) |
| **Typed Amounts** (`Section 1`) | Integers & decimals: `15`, `15.2`, `15.20`<br>Comma thousands: `1,250`, `1,250.00` | European comma decimal: `15,20`, `1.250,00`<br>Dot thousands: `1.250`<br>Indian grouping: `1,25,000`<br>Currency prefix / empty: `RM15`, `""`, `"   "` | Valid numeric formats parsed accurately to sen; malformed groupings, comma decimals, currency prefixes, and empty strings rejected with validation feedback. |
| **Full Name** (`MEJ-ACC-02`) | Min: `2` chars (`Al`)<br>Typical: `Mohamed bin Ali / O'Connor-Tan @ Omar.`<br>Max: `60` chars | Below min: `1` char (`A`), `""`<br>Above max: `61` chars<br>Disallowed chars: `Ali123`, `Ali_Tan`, `<script>`, `🔥` | `2` to `60` chars using letters plus `. ' - / @` (and spaces) accepted; digits, symbols, HTML tags, or length `< 2` / `> 60` rejected. |
| **Tray Item Note** (`MEJ-TRY-04`) | Min: `0` chars (empty)<br>Typical: `30` chars (`Kurang manis, no ice`)<br>Max: `60` chars | Above max: `61` chars<br>XSS payload: `<img src=x onerror=alert(1)>` | `0` to `60` chars accepted and displayed as plain text (HTML-encoded); `61+` chars blocked or rejected. |
| **Board Message** (`MEJ-BRD-05`) | Min: `0` chars (cleared)<br>Max: `60` chars | Above max: `61` chars<br>XSS payload: `<script>alert(1)</script>` | `0` to `60` chars saved and rendered safely as text on the public Split-Flap Queue Board; `61+` chars rejected. |
| **Place Note** (`MEJ-DAP-04`) | Min: `0` chars<br>Max: `30` chars | Above max: `31` chars | `0` to `30` chars accepted for table/place note; `31+` chars rejected. |
| **Stall Name & Cuisine** (`MEJ-DAP`) | Min: `2` chars<br>Max: `40` chars | Below min: `1` char, `""`<br>Above max: `41` chars | `2` to `40` chars accepted; `< 2` or `> 40` chars rejected. |
| **Dish Name** (`MEJ-DAP-03`) | Min: `2` chars<br>Max: `60` chars | Below min: `1` char, `""`<br>Above max: `61` chars | `2` to `60` chars accepted; `< 2` or `> 60` chars rejected. |
| **Staff Login** (`MEJ-DAP`) | Min: `3` lowercase `a-z` (`ali`)<br>Max: `20` lowercase `a-z` (`abcdefghijklmnopqrst`) | Below min: `2` chars (`al`)<br>Above max: `21` chars<br>Disallowed: `Ali` (uppercase), `ali1` (digit), `ali_cook` (underscore/symbol) | Only `3` to `20` lowercase `a-z` characters accepted; uppercase, digits, spaces, and symbols rejected. |
| **Teh Tarik Hours** (`MEJ-TEH-01` to `04`) | Window duration: `30m` (min), `2h` (typical), `3h` (max)<br>Window count: `0` to `4` non-overlapping windows<br>Promo cups: `1` or `2` dearest eligible cups at `RM1.50` (e.g., 3 cups at RM2.50, RM3.00, RM3.50 -> RM3.00 and RM3.50 discounted to RM1.50) | Duration `< 30m`: `29m`<br>Duration `> 3h`: `3h 1m` (`181m`)<br>Overlap: `10:00-11:30` & `11:00-12:30`<br>Count: `5th` window<br>Boundary time: 1s after window end | Valid windows (`30m` to `3h`, max `4`, non-overlapping) saved; overlapping, `29m`, `3h 1m`, or `5th` window rejected. At most `2` dearest eligible cups per tray priced at `RM1.50`. |
| **Cash 5-Sen Rounding** (`MEJ-PAY-02`) | Last sen digit `0` or `5`: `RM10.00` -> `RM10.00`, `RM10.05` -> `RM10.05`<br>Digit `1` or `2` (down to `0`): `RM10.01` -> `RM10.00`, `RM10.02` -> `RM10.00`<br>Digit `3` or `4` (up to `5`): `RM10.03` -> `RM10.05`, `RM10.04` -> `RM10.05`<br>Digit `6` or `7` (down to `5`): `RM10.06` -> `RM10.05`, `RM10.07` -> `RM10.05`<br>Digit `8` or `9` (up to `10`): `RM10.08` -> `RM10.10`, `RM10.09` -> `RM10.10` | Applying 5-sen rounding to Diner Balance payment or Refunds (`MEJ-REF`) | Cash total rounds to nearest `RM0.05` per Malaysian rounding rules; Diner Balance and Refunds always use exact unrounded sen amounts. |

---

### 3. State Transition Matrices

#### 3.1 Tray Lifecycle States (`Section 16`)
*Valid States:* `(none)` -> `Draft` -> `Awaiting payment` <-> `Draft` (Edit tray) -> `Paid` / `Cancelled` -> `Complete` (plus direct `Draft` -> `Paid` via Diner Balance).

| Current State | Event / Action | Next State | Expected Outcome / Guard |
|---|---|---|---|
| `(none)` | Diner adds first valid dish | `Draft` | Single `Draft` tray created for Diner; persisted across refresh. |
| `Draft` | Diner selects Diner Balance & confirms (sufficient funds) | `Paid` | Exact unrounded amount deducted; tickets created as `New`. |
| `Draft` | Diner selects Cash at cashier & confirms | `Awaiting payment` | 4-digit pay code generated; tray locked for cashier collection. |
| `Awaiting payment` | Diner clicks `Edit tray` | `Draft` | Pay code invalidated; diner can modify dishes/notes/quantities. |
| `Awaiting payment` | Cashier confirms Cash receipt (5-sen rounded) | `Paid` | Tray marked `Paid`; tickets created as `New` with queue numbers `001`-`999`. |
| `Awaiting payment` | Diner clicks `Cancel tray` | `Cancelled` | Tray closed as `Cancelled`; no tickets dispatched to stalls. |
| `Paid` | All child tickets reach terminal state (`Collected` / `Cancelled` / `Refunded`) | `Complete` | Tray transitions to `Complete` in Diner history. |
| **Invalid:** `Paid` | Diner triggers `Edit tray` or `Cancel tray` via direct POST / back button | `Paid` (Unchanged) | **Rejected (400/409):** Paid trays cannot revert to `Draft` or `Cancelled`. |
| **Invalid:** `Cancelled` | Cashier attempts to collect Cash on cancelled pay code | `Cancelled` (Unchanged) | **Rejected (400/409):** Cancelled tray cannot transition to `Paid`. |
| **Invalid:** `Draft` | Diner attempts to open a 2nd concurrent `Draft` tray | `Draft` (Unchanged) | **Rejected / Merged:** Only one `Draft` tray allowed per Diner at a time. |

#### 3.2 Ticket Lifecycle States (`MEJ-TKT-02`)
*Valid States:* `New` -> `Cooking` -> `Ready` -> `Collected`; `New` -> `Cancelled` (diner); `New` / `Cooking` -> `Refunded` (sold out).

| Current State | Actor & Event | Next State | Expected Outcome / Guard |
|---|---|---|---|
| `New` | Cook (assigned stall) marks `Start cooking` | `Cooking` | Ticket enters `Cooking`; diner cancellation now blocked. |
| `New` | Diner clicks `Cancel ticket` | `Cancelled` | Exact unrounded line refund (plus proportional tax/fees if applicable) credited to Diner Balance. |
| `New` or `Cooking` | Cook marks dish `Sold out today` / refunds line | `Refunded` | Exact unrounded refund credited to Diner Balance even if balance exceeds `RM500.00`. |
| `Cooking` | Cook marks `Ready` | `Ready` | Ticket appears on Split-Flap Queue Board (`Ready` column). |
| `Ready` | Cook or Cashier marks `Collected` | `Collected` | Ticket removed from active Queue Board; terminal state reached. |
| **Invalid:** `Cooking` / `Ready` | Diner attempts `Cancel ticket` via direct API/URL | Unchanged | **Rejected (403/409):** Diner can only cancel tickets in `New` state. |
| **Invalid:** `New` (Stall A) | Cook assigned to Stall B attempts state change on Stall A ticket | Unchanged | **Rejected (403 Forbidden):** Server-side RBAC enforces stall ownership. |
| **Invalid:** `Collected` / `Refunded` / `Cancelled` | Any actor attempts further state transition | Unchanged | **Rejected (409 Conflict):** Terminal ticket states are immutable. |

---

### 4. Decision Table: Totals, Containers, Service Charge & Tax (`MEJ-TOT-01` to `-05`)

*Rules:*
- **Tapau Container Fee (`MEJ-TOT-02`):** `RM0.30` per Tapau item/unit (applied to Tapau items only; `RM0.00` for Dine-in).
- **Service Charge (`MEJ-TOT-03`):** `10%` of **Dine-in Items subtotal ONLY**, applied **ONLY** when Hall is **Dewan Sejuk (Table service, tables 81 to 116)**. Tapau items and Laman (Self-collect) incur `RM0.00` Service Charge.
- **Service Tax (`MEJ-TOT-04`):** `6%` half-up rounded to nearest sen on `(Items Subtotal + Containers + Service Charge)`.

| Rule ID | Mode: Dine-in Items | Mode: Tapau Items | Hall: Laman (Self-collect, 1-80, 117-120) | Hall: Dewan Sejuk (Table service, 81-116) | Containers (`RM0.30`/Tapau) | Service Charge (`10%` Dine-in Items) | Service Tax (`6%` half-up) |
|---|:---:|:---:|:---:|:---:|---|---|---|
| **DT-01** | Yes | No | Yes | No | `RM0.00` | `RM0.00` | `6%` of `(Dine-in Items)` |
| **DT-02** | No | Yes | Yes | No | `RM0.30 x Tapau Qty` | `RM0.00` | `6%` of `(Tapau Items + Containers)` |
| **DT-03** | Yes | Yes | Yes | No | `RM0.30 x Tapau Qty` | `RM0.00` | `6%` of `(All Items + Containers)` |
| **DT-04** | Yes | No | No | Yes | `RM0.00` | `10%` of `(Dine-in Items)` | `6%` of `(Dine-in Items + Service Charge)` |
| **DT-05** | No | Yes | No | Yes | `RM0.30 x Tapau Qty` | `RM0.00` *(Tapau excluded)* | `6%` of `(Tapau Items + Containers)` |
| **DT-06** | Yes | Yes | No | Yes | `RM0.30 x Tapau Qty` | `10%` of `(Dine-in Items ONLY)` | `6%` of `(All Items + Containers + Service Charge)` |

*Worked Boundary Verification (DT-06, Half-Up Tax):*
If `Dine-in Items = RM10.00`, `Tapau Items = RM10.00` (1 unit, `Containers = RM0.30`) at Dewan Sejuk:
- `Service Charge = 10% x RM10.00 = RM1.00` (Tapau RM10.00 excluded).
- `Taxable Base = RM10.00 + RM10.00 + RM0.30 + RM1.00 = RM21.30`.
- `Service Tax (6%) = 21.30 x 0.06 = RM1.278` -> half-up to `RM1.28`.
- `Balance Total = RM22.58`; `Cash Total (5-sen rounded, digit 8 -> 10) = RM22.60`.

---

### 5. Experience-Based & Security Test Conditions (`MEJ-SEC`)
- **IDOR & Vertical/Horizontal RBAC:** Diner B requesting Diner A's tray/ticket ID; Cook of Stall 1 mutating Stall 2 dishes/tickets; Cashier accessing Manager CRUD; unauthenticated access to `/dapur/*`.
- **Server-Side Integrity:** Tampering with dish price, Teh Tarik promo eligibility, or table number in POST payloads; submitting a tray after stall `Close for today` or last-order cutoff.
- **Concurrency & PRG:** Double-clicking `Confirm payment` (Diner Balance) or `Collect Cash` (Cashier); browser Refresh (`F5`) after POST; simultaneous Diner + Dapur sessions in one browser.


---

## PART 2: TEST IMPLEMENTATION & PROCEDURES (DELIVERABLE 3)

# Test Implementation & Procedures: Meja Marmar (Medan Selera Meja Marmar & Dapur)
**Competition:** Malaysia Testing Cup 2026  
**Team:** NERV | **Lead Tester:** Mohamed Makhlouf  
**Specification Reference:** MEJ-FRS-001 v1.0  
**Coverage:** Core User Journeys, Boundary Constraints, State Lifecycles, Security & Accessibility  

---

### Test Cases Specification Table

| Test Case ID | Traceable Condition | Pre-conditions | Test Steps | Test Data | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| **TC-001** | `TCND-TOT-01`<br>`TCND-TEH-01`<br>`TCND-PAY-01` | 1. Signed in as Diner.<br>2. Active Teh Tarik Hour window configured.<br>3. Table `81` (Dewan Sejuk, In use) has `< 6` open trays. | 1. Select Table `81` (Dewan Sejuk).<br>2. Add 3 eligible Teh Tarik cups (2 Dine-in, 1 Tapau) and 1 Dine-in dish.<br>3. Open Tray summary and inspect line discounts, Containers, Service Charge, and Service Tax.<br>4. Compare Diner Balance total vs Cash at cashier total. | Cup 1 (Dine-in): `RM2.20`<br>Cup 2 (Dine-in): `RM3.00`<br>Cup 3 (Tapau): `RM3.50`<br>Dish 4 (Dine-in): `RM4.80`<br>Table: `81` (Dewan Sejuk) | 1. Only 2 dearest cups (`RM3.50`, `RM3.00`) discounted to `RM1.50` each (`RM2.20` unchanged).<br>2. Dine-in subtotal = `RM8.50`; Tapau subtotal = `RM1.50`; Items = `RM10.00`.<br>3. Tapau Container = `RM0.30` (1 unit).<br>4. Service Charge (10% Dine-in ONLY) = `RM0.85`.<br>5. Service Tax (6% half-up on `RM11.15` = `0.669`) = `RM0.67`.<br>6. Balance Total = `RM11.82` (exact); Cash Total = `RM11.80` (5-sen rounded down). | *Pending Execution* | Pending |
| **TC-002** | `TCND-CTR-01` | 1. Signed in as Diner on Tray / Table selection.<br>2. Table `5` already has `6` open trays (`Awaiting payment` or `Paid` non-complete). | 1. Attempt to select out-of-service Table `40` (Laman).<br>2. Attempt to select out-of-service Table `101` (Dewan Sejuk).<br>3. Enter out-of-range Table `0` and Table `121`.<br>4. Attempt to open a 7th tray on Table `5` (currently at 6 open trays). | Out-of-service: `40`, `101`<br>Out-of-range: `0`, `121`<br>Full table: `5` (6 open trays)<br>Valid control: `80` (Laman), `81` (Dewan Sejuk) | 1. Tables `40` and `101` are rejected as out of service.<br>2. Tables `0` and `121` are rejected with range error (`1` to `120`).<br>3. 7th open tray on Table `5` is blocked with capacity-reached message.<br>4. Tables `80` and `81` resolve to Laman and Dewan Sejuk respectively. | *Pending Execution* | Pending |
| **TC-003** | `TCND-TRY-01`<br>`TCND-TXT-01` | 1. Signed in as Diner with an empty `Draft` tray.<br>2. At least 6 active stalls available. | 1. Add same dish as Dine-in (`qty 5`) and Tapau (`qty 4`) with identical empty notes.<br>2. Attempt to increase Tapau qty to `5` (combined `5 + 5 = 10`).<br>3. Add 1 dish each from 4 more distinct stalls (total 5 stalls), then attempt to add a dish from a 6th stall.<br>4. Add a dish with a `60`-char note, then attempt a `61`-char note.<br>5. Add same dish Dine-in (`Note A`) and Tapau (`Note B`) and inspect merge behaviour. | Qty test: `5` + `4` (`9` valid), `5` + `5` (`10` invalid)<br>Stalls: `5` valid, `6th` invalid<br>Note 60: `60 x 'a'`<br>Note 61: `61 x 'a'`<br>Notes: `"Kurang manis"` vs `"Extra ice"` | 1. Combined qty `9` accepted; `10` blocked with max-9-per-dish error.<br>2. 5 distinct stalls accepted; 6th stall blocked with max-5-stalls error.<br>3. `60`-char note saved; `61`-char note blocked or rejected.<br>4. Different notes on Dine-in vs Tapau do not silently overwrite each other or exceed qty 9. | *Pending Execution* | Pending |
| **TC-004** | `TCND-BAL-01`<br>`TCND-PAY-01` | 1. Signed in as Diner.<br>2. Initial Diner Balance set to `RM490.00` (or topped up to `RM490.00`).<br>3. Tray total exceeds `RM490.00` (or test balance `RM10.00` against `RM15.00` tray). | 1. Attempt invalid top-up of `RM5.00` and `RM15.00` (non-RM10 steps).<br>2. Top up `RM10.00` (reaching exact `RM500.00` cap).<br>3. Attempt another `RM10.00` top-up (would become `RM510.00`).<br>4. With balance `RM10.00`, attempt to pay a `RM15.00` tray using Diner Balance.<br>5. At `RM500.00` balance, trigger a `RM5.00` ticket refund (`Sold out` / `Cancel`). | Invalid steps: `RM5.00`, `RM15.00`<br>Valid top-up: `RM10.00` (to `RM500.00`)<br>Cap overflow: `+RM10.00` at `RM500.00`<br>Insufficient: `RM10.00` bal vs `RM15.00` tray<br>Refund at cap: `RM5.00` | 1. Non-RM10 top-ups (`RM5.00`, `RM15.00`) rejected.<br>2. Top-up to `RM500.00` succeeds; subsequent `+RM10.00` blocked at `RM500.00` cap.<br>3. Insufficient balance blocks payment without deducting funds.<br>4. Refund succeeds even when resulting balance exceeds `RM500.00` (`RM505.00`). | *Pending Execution* | Pending |
| **TC-005** | `TCND-ST-02`<br>`TCND-BAL-01` | 1. Paid tray with 2 tickets (`TKT-A`, `TKT-B`) at Stall 1 in `New` state.<br>2. Diner and Stall 1 Cook sessions available. | 1. Diner cancels `TKT-A` while in `New` state and checks Diner Balance.<br>2. Cook moves `TKT-B` through `New -> Cooking`.<br>3. Diner attempts to cancel `TKT-B` while in `Cooking` state (UI and direct POST).<br>4. Cook marks `TKT-B` dish `Sold out today` / refunds line and checks Diner Balance.<br>5. On a 3rd ticket `TKT-C`, Cook progresses `New -> Cooking -> Ready -> Collected`. | `TKT-A`: `New` (diner cancel)<br>`TKT-B`: `Cooking` (diner cancel blocked, cook sold-out refund)<br>`TKT-C`: full happy path<br>Line value: exact sen (e.g. `RM4.83` incl. tax/fees) | 1. `TKT-A` transitions `New -> Cancelled` with exact unrounded refund credited.<br>2. Diner cancel on `TKT-B` (`Cooking`) is blocked (UI disabled and server returns 403/409).<br>3. Cook sold-out refund transitions `TKT-B -> Refunded` with exact unrounded sen refund (no 5-sen rounding).<br>4. `TKT-C` reaches `Collected` and disappears from active Queue Board. | *Pending Execution* | Pending |
| **TC-006** | `TCND-SEC-01` | 1. Existing Diner account, Stall 1 Cook account, Cashier account, and Manager account.<br>2. Single browser session. | 1. Sign in as Diner in Tab 1.<br>2. In Tab 2 of the same browser, sign in to `/dapur` as Stall 1 Cook and verify Tab 1 Diner session remains intact.<br>3. As Stall 1 Cook, attempt to access Stall 2's kitchen URL/ticket endpoint and Manager CRUD URLs.<br>4. Sign in as Cashier and attempt to access Manager CRUD (stall/dish/staff/Teh Tarik Hours) endpoints. | Diner: Tab 1<br>Cook (Stall 1): Tab 2<br>Target unauthorized paths: Stall 2 kitchen API, Manager CRUD routes (`/dapur/manage/*`) | 1. Dual Diner + Staff sign-in coexists cleanly in one browser without session overwrite.<br>2. Stall 1 Cook is blocked (403 Forbidden) from Stall 2's kitchen and all Manager pages.<br>3. Cashier is blocked (403 Forbidden) from Manager CRUD routes. | *Pending Execution* | Pending |
| **TC-007** | `TCND-SEC-01`<br>`TCND-ST-01`<br>`TCND-TXT-01` | 1. Diner A owns Paid Tray `#A` and `Draft` Tray `#D`.<br>2. Diner B signed in.<br>3. DevTools / proxy ready to inspect POST payloads. | 1. Diner B requests Diner A's tray URL/number (`#A`).<br>2. Diner A intercepts add-to-tray / checkout POST and tampers `price=0.10` or `state=Paid`.<br>3. Diner A submits `<script>alert(1)</script>` in the 60-char tray item note and views Tray, Kitchen ticket, and Board.<br>4. Diner A submits Diner Balance payment, presses `F5` (reload), and tests simultaneous double-submit on `Confirm payment`. | IDOR target: Diner A's tray number<br>Tampered fields: `price=0.10`, `state=Paid`<br>XSS payload: `<script>alert(1)</script>`<br>Concurrency: 2 rapid clicks / parallel POSTs | 1. Diner B sees `"Tray not found"` (no data leakage).<br>2. Server ignores client-supplied price/state and computes authoritative totals (or rejects tampered state).<br>3. XSS payload is HTML-encoded and rendered as literal text; zero script execution.<br>4. PRG pattern prevents duplicate charge on `F5`; simultaneous double-submit creates only 1 Paid tray / deduction. | *Pending Execution* | Pending |
| **TC-008** | `TCND-ST-02`<br>`TCND-SEC-01` | 1. At least 1 ticket in `Cooking` and 1 in `Ready`.<br>2. Public Split-Flap Queue Board open.<br>3. Kitchen Display open as Cook. | 1. On Public Board, wait `20s` and observe auto-refresh of `Cooking` / `Ready` tickets.<br>2. Toggle `Pause updates`, trigger a ticket state change in Kitchen, wait `25s`, then unpause.<br>3. On Kitchen Display, press keyboard shortcuts `S` (Start cooking), `C` (Ready/Complete), and `H` (Help/Hold per UI legend) on focused ticket.<br>4. Inspect Public Board, Diner Tray, and Kitchen Display at `375px` mobile width and at `1280px` with `200%` browser zoom. | Wait interval: `20s` (auto) / `25s` (paused)<br>Keys: `S`, `C`, `H`<br>Viewports: `375x812` mobile, `1280x800` at `200%` zoom | 1. Public Board auto-refreshes every `20s`; `Pause updates` freezes DOM updates until resumed.<br>2. `S`, `C`, `H` shortcuts trigger their documented actions without console errors.<br>3. Zero horizontal overflow, clipped controls, or overlapping text at `375px` and `1280px` (`200%` zoom). | *Pending Execution* | Pending |

---

## PART 3: SMART USE OF AI TOOLS (ENGINEERING MULTIPLIER)

Team NERV leveraged AI (Antigravity / Gemini) as a disciplined engineering multiplier throughout test analysis, test case design, and non-functional preparation while enforcing strict human verification:

1. **Specification Decomposition & Test Matrix Synthesis:**
   - Parsed `MEJ-FRS-001 v1.0` across all 11 `MEJ-*` modules to systematically derive Equivalence Partitions, Boundary Value Analysis (BVA) edges, Tray/Ticket State Transition guards, and the 6-rule Decision Table (`DT-01` through `DT-06`) for Tapau containers, Dewan Sejuk 10% Service Charge, and 6% half-up Service Tax.
2. **Deterministic Test Data & Fuzz Vector Generation:**
   - Used AI paired with `scripts/fuzz_gen.py` to generate exact boundary test inputs: table numbers (`0`, `1`, `40`, `80`, `81`, `101`, `116`, `117`, `120`, `121`), 10-sen price boundaries (`RM0.40` to `RM100.00`), RM500.00 wallet cap edges, `60`/`61`-character strings, special-character names (`O'Connor-Tan @ Omar.`), and contextual XSS payloads (`<script>alert(1)</script>`).
3. **Automated Non-Functional Reconnaissance Suite:**
   - Deployed AI-assisted CLI tooling (`scripts/crawler.js` for Puppeteer DOM/console/network capture, `scripts/audit_accessibility.js` for Axe-core WCAG 2.1 AA audits, and `scripts/security_probe.py` for HTTP security headers, CORS, and cookie flags) to accelerate surface mapping.
4. **Protocol & ISTQB Classification:**
   - Cross-referenced HTTP status codes, Post/Redirect/Get (PRG) patterns, and 5-sen cash rounding edge cases against RFC HTTP specifications and ISTQB CTFL severity standards.
5. **Human-in-the-Loop Verification Guarantee:**
   - AI is strictly restricted to planning, test design synthesis, and diagnostic assistance. Every executed test case (`TC-001` through `TC-008`) and every logged defect is manually reproduced, verified, and diagnosed in live Chrome/Firefox DevTools and SUT runtime output, ensuring zero unverified or hallucinated findings.

