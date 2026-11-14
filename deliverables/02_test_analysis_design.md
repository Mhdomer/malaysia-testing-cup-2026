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
