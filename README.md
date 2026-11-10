# Malaysia Testing Cup 2026 (Team NERV)
*National Pre-Qualifier to the World's Best Tester Competition*

Organized by the **Malaysian Software Testing Board (MSTB)**.

## 👤 Team Information
- **Team Name:** `NERV`
- **Candidate:** Mohamed Makhlouf (Omar)
- **Role:** Lead Quality & Security Assessment Engineer
- **Competition Date:** Saturday, 14 November 2026
- **Window:** 04:30 AM to 08:00 AM AST (09:30 AM to 01:00 PM MYT)
- **Target:** Top 10 finish to qualify for World's Best Tester Final (2 Dec 2026)

## 🗂️ Project Structure
```text
.
├── .agents/                   # Antigravity agent context, router & mtc-evaluator skill
├── deliverables/              # The 6 core ISTQB competition deliverables
│   ├── 01_test_plan.md
│   ├── 02_test_analysis_design.md
│   ├── 03_test_implementation.md
│   ├── 04_bug_reports/
│   ├── 05_non_functional_report.md
│   └── 06_summary_test_report.md
├── scripts/                   # Automated CLI diagnostic & testing suite
│   ├── crawler.js             # Puppeteer DOM scraper, error sniffer & screenshot engine
│   ├── audit_accessibility.js # Axe-core WCAG 2.1 AA engine
│   ├── security_probe.py      # HTTP security headers, CORS & JWT auditor
│   └── fuzz_gen.py            # BVA and fuzzing payload generator
├── evidence/                  # Captured defect screenshots (<16MB PNGs)
└── TOOLKIT.md                 # Complete 130-point ISTQB submission templates
```

## 🚀 Quick Start
```bash
# SUT Crawl & Initial Screenshot
node scripts/crawler.js "<SUT_URL>"

# Automated Accessibility Scan (Deliverable 5)
node scripts/audit_accessibility.js "<SUT_URL>"

# HTTP Security Headers & Sensitive Route Recon
python3 scripts/security_probe.py "<SUT_URL>" --recon

# Generate 255-char Boundary String to Clipboard
python3 scripts/fuzz_gen.py --type bva --len 255 --copy
```
