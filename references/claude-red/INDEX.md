# Claude-Red Offensive Skills Index

Complete offline reference library of 79 offensive security skills ported for Antigravity.

**Active Workspace Skills (16 Curated for MTC 2026):**

- **`offensive-business-logic`**: Installed in `.agents/skills/offensive-business-logic/SKILL.md`
- **`offensive-idor`**: Installed in `.agents/skills/offensive-idor/SKILL.md`
- **`offensive-jwt`**: Installed in `.agents/skills/offensive-jwt/SKILL.md`
- **`offensive-oauth`**: Installed in `.agents/skills/offensive-oauth/SKILL.md`
- **`offensive-api-security`**: Installed in `.agents/skills/offensive-api-security/SKILL.md`
- **`offensive-api-abuse`**: Installed in `.agents/skills/offensive-api-abuse/SKILL.md`
- **`offensive-graphql`**: Installed in `.agents/skills/offensive-graphql/SKILL.md`
- **`offensive-race-condition`**: Installed in `.agents/skills/offensive-race-condition/SKILL.md`
- **`offensive-parameter-pollution`**: Installed in `.agents/skills/offensive-parameter-pollution/SKILL.md`
- **`offensive-fast-checking`**: Installed in `.agents/skills/offensive-fast-checking/SKILL.md`
- **`offensive-reporting`**: Installed in `.agents/skills/offensive-reporting/SKILL.md`
- **`offensive-sqli`**: Installed in `.agents/skills/offensive-sqli/SKILL.md`
- **`offensive-xss`**: Installed in `.agents/skills/offensive-xss/SKILL.md`
- **`offensive-ssrf`**: Installed in `.agents/skills/offensive-ssrf/SKILL.md`
- **`offensive-file-upload`**: Installed in `.agents/skills/offensive-file-upload/SKILL.md`
- **`offensive-ai-security`**: Installed in `.agents/skills/offensive-ai-security/SKILL.md`

---

## Full Category Breakdown

### Active-Directory
- **`offensive-active-directory`**: Active Directory attack methodology for internal network red team engagements. Covers reconnaissance (BloodHound, PowerV... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/active-directory/offensive-active-directory/SKILL.md))
- **`offensive-netexec`**: >... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/active-directory/offensive-netexec/SKILL.md))

### Ai
- **`offensive-ai-security`**: AI/LLM security offensive checklist: prompt injection, jailbreaking, model extraction, training data poisoning, adversar... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/ai/offensive-ai-security/SKILL.md))

### Api
- **`offensive-api-abuse`**: Advanced API exploitation methodology focused on business logic abuse and sophisticated attack patterns that bypass trad... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/api/offensive-api-abuse/SKILL.md))
- **`offensive-api-security`**: Comprehensive API security testing methodology covering REST, gRPC, and WebSocket attack surfaces. Addresses the full OW... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/api/offensive-api-security/SKILL.md))

### Auth
- **`offensive-jwt`**: JWT attack methodology for penetration testers. Covers algorithm confusion (alg:none, RS256→HS256), weak HMAC secret bru... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/auth/offensive-jwt/SKILL.md))
- **`offensive-oauth`**: OAuth 2.0 attack checklist: authorization code interception, redirect_uri bypass, CSRF on OAuth flow, state parameter ab... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/auth/offensive-oauth/SKILL.md))

### Cicd
- **`offensive-cicd-pipeline`**: Comprehensive CI/CD pipeline exploitation methodology covering GitHub Actions injection vectors (expression injection vi... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/cicd/offensive-cicd-pipeline/SKILL.md))
- **`offensive-cicd-secrets`**: Comprehensive secrets extraction methodology targeting CI/CD environments across all major platforms. Covers environment... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/cicd/offensive-cicd-secrets/SKILL.md))

### Cloud
- **`offensive-cloud`**: Cloud security attack methodology covering AWS, Azure, and GCP. Includes credential harvesting (IMDS, ~/.aws, env vars, ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/cloud/offensive-cloud/SKILL.md))

### Container
- **`offensive-container-escape`**: Container escape and breakout techniques targeting Docker, containerd, and Podman runtimes. Covers privileged container ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/container/offensive-container-escape/SKILL.md))
- **`offensive-k8s-attacks`**: Kubernetes cluster attack techniques covering the full attack lifecycle from initial foothold in a pod to cluster-wide c... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/container/offensive-k8s-attacks/SKILL.md))

### Crypto
- **`offensive-crypto-attacks`**: Systematic methodology for identifying and exploiting cryptographic implementation weaknesses in real-world applications... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/crypto/offensive-crypto-attacks/SKILL.md))
- **`offensive-tls-attacks`**: Comprehensive methodology for auditing and exploiting TLS/SSL implementations and misconfigurations across network servi... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/crypto/offensive-tls-attacks/SKILL.md))

### Exploit-Dev
- **`offensive-basic-exploitation`**: Week 5 exploit development curriculum. Foundational exploitation techniques: controlling EIP/RIP, ROP chain construction... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/exploit-dev/offensive-basic-exploitation/SKILL.md))
- **`offensive-crash-analysis`**: Week 4 exploit development curriculum. Crash triage and analysis methodology: WinDbg/GDB analysis, ASAN/MSAN output inte... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/exploit-dev/offensive-crash-analysis/SKILL.md))
- **`offensive-exploit-dev-course`**: Full exploit development course roadmap and syllabus: weekly topics, recommended reading, lab setup, and learning path f... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/exploit-dev/offensive-exploit-dev-course/SKILL.md))
- **`offensive-exploit-development`**: Exploit development operational guide: environment setup, debugging workflow, PoC development lifecycle, writing reliabl... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/exploit-dev/offensive-exploit-development/SKILL.md))
- **`offensive-mitigations`**: Security mitigation reference and bypass catalog: ASLR, DEP/NX, RELRO, stack canaries, CFI, sandboxing, seccomp. Covers ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/exploit-dev/offensive-mitigations/SKILL.md))
- **`offensive-toctou`**: Time-of-Check / Time-of-Use (TOCTOU) race condition exploitation methodology across binary, kernel, filesystem, web, and... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/exploit-dev/offensive-toctou/SKILL.md))

### Forensics
- **`offensive-anti-forensics`**: Anti-forensics and evidence destruction techniques for red team operators conducting authorized engagements. Covers log ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/forensics/offensive-anti-forensics/SKILL.md))
- **`offensive-c2-frameworks`**: Command and Control framework deployment, configuration, and operational tradecraft for red team engagements. Covers Cob... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/forensics/offensive-c2-frameworks/SKILL.md))

### Fuzzing
- **`offensive-bug-identification`**: Systematic bug identification methodology: source code review patterns, black-box testing strategies, taint analysis, da... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/fuzzing/offensive-bug-identification/SKILL.md))
- **`offensive-fuzzing`**: Practical offensive fuzzing methodology covering target identification, fuzzer selection (AFL++, libFuzzer, Honggfuzz, B... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/fuzzing/offensive-fuzzing/SKILL.md))
- **`offensive-fuzzing-course`**: Week 2 of the exploit development curriculum. Covers fuzzing methodology: target selection, corpus generation, coverage-... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/fuzzing/offensive-fuzzing-course/SKILL.md))
- **`offensive-vuln-classes`**: Exploit development curriculum covering core vulnerability classes with real-world CVE case studies: stack/heap buffer o... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/fuzzing/offensive-vuln-classes/SKILL.md))

### Infrastructure
- **`offensive-advanced-redteam`**: Comprehensive red team operations methodology covering full engagement lifecycle from planning through reporting. Addres... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/infrastructure/offensive-advanced-redteam/SKILL.md))
- **`offensive-edr-evasion`**: EDR evasion offensive checklist: hook unhooking (user/kernel), direct syscalls, PPID spoofing, process injection variant... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/infrastructure/offensive-edr-evasion/SKILL.md))
- **`offensive-initial-access`**: Initial access techniques checklist: phishing (spear/smishing), credential stuffing, exposed service exploitation, suppl... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/infrastructure/offensive-initial-access/SKILL.md))
- **`offensive-keylogger-arch`**: Low-level keylogger architecture design: kernel driver hooks (WH_KEYBOARD_LL, SetWindowsHookEx), ETW-based input capture... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/infrastructure/offensive-keylogger-arch/SKILL.md))
- **`offensive-shellcode`**: Shellcode development reference for offensive security engagements. Use when writing custom x86/x64 shellcode, implement... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/infrastructure/offensive-shellcode/SKILL.md))
- **`offensive-windows-boundaries`**: Windows security boundary taxonomy and attack surface enumeration: kernel/user boundary, sandbox boundaries (LPAC, AppCo... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/infrastructure/offensive-windows-boundaries/SKILL.md))
- **`offensive-windows-mitigations`**: Deep-dive on Windows exploit mitigations: ASLR, DEP/NX, CFG, CET/Shadow Stack, SEHOP, Heap Guard, ACG, Arbitrary Code Gu... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/infrastructure/offensive-windows-mitigations/SKILL.md))

### Iot
- **`offensive-iot`**: IoT and embedded device security testing methodology. Covers hardware reconnaissance (UART, JTAG, SWD, SPI flash, I2C EE... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/iot/offensive-iot/SKILL.md))

### Mobile
- **`offensive-mobile`**: Mobile (Android + iOS) application penetration testing methodology. Covers static analysis (apktool/jadx for Android, cl... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/mobile/offensive-mobile/SKILL.md))

### Network
- **`offensive-network-attacks`**: Dense description covering ARP spoofing, LLMNR/NBT-NS/mDNS poisoning, DNS poisoning, MITM attacks, VLAN hopping, DHCP at... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/network/offensive-network-attacks/SKILL.md))

### Post-Exploitation
- **`offensive-data-exfiltration`**: Dense methodology covering DNS exfiltration (dnscat2, iodine, dns2tcp), HTTPS tunneling (domain fronting, CDN abuse, leg... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/post-exploitation/offensive-data-exfiltration/SKILL.md))
- **`offensive-lateral-movement`**: Comprehensive lateral movement tradecraft for authorized red team engagements covering credential-based movement (pass-t... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/post-exploitation/offensive-lateral-movement/SKILL.md))
- **`offensive-persistence`**: Comprehensive persistence tradecraft for authorized red team engagements covering Windows and Linux mechanisms. Windows ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/post-exploitation/offensive-persistence/SKILL.md))

### Privesc
- **`offensive-linux-privesc`**: Comprehensive Linux privilege escalation methodology for offensive security engagements. Covers the full attack surface ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/privesc/offensive-linux-privesc/SKILL.md))
- **`offensive-windows-privesc`**: Comprehensive Windows privilege escalation methodology for offensive security engagements. Covers the full attack surfac... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/privesc/offensive-windows-privesc/SKILL.md))

### Recon
- **`offensive-osint`**: Comprehensive OSINT methodology skill for offensive security, red team intelligence gathering, and bug bounty reconnaiss... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/recon/offensive-osint/SKILL.md))
- **`offensive-osint-methodology`**: Structured OSINT methodology framework: target definition, source selection, collection workflows, data correlation, tim... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/recon/offensive-osint-methodology/SKILL.md))

### Social-Engineering
- **`offensive-phishing`**: Phishing campaign execution methodology for authorized red team engagements. Covers end-to-end campaign lifecycle: infra... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/social-engineering/offensive-phishing/SKILL.md))
- **`offensive-social-engineering`**: Social engineering attack techniques beyond email phishing for authorized red team and physical penetration testing enga... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/social-engineering/offensive-social-engineering/SKILL.md))

### Supply-Chain
- **`offensive-dependency-confusion`**: Deep-dive offensive methodology for dependency confusion and namespace attacks across all major package ecosystems. Cove... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/supply-chain/offensive-dependency-confusion/SKILL.md))
- **`offensive-supply-chain`**: Comprehensive offensive methodology for software supply chain attacks covering the full kill chain from reconnaissance t... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/supply-chain/offensive-supply-chain/SKILL.md))

### Utility
- **`offensive-fast-checking`**: Speed-optimized offensive checklist for rapid assessment: quick-win vulnerability patterns, fast recon shortcuts, automa... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/utility/offensive-fast-checking/SKILL.md))
- **`offensive-reporting`**: Penetration test and red team report writing methodology. Covers executive summary structuring (risk-led narrative for n... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/utility/offensive-reporting/SKILL.md))

### Web
- **`offensive-business-logic`**: Business logic vulnerability testing for web/mobile/API engagements. Covers workflow bypass, state machine violations, m... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-business-logic/SKILL.md))
- **`offensive-deserialization`**: Insecure deserialization exploitation across Java, PHP, .NET, Python, Node.js, and Ruby. Covers gadget chain constructio... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-deserialization/SKILL.md))
- **`offensive-file-upload`**: File upload vulnerability checklist: MIME type bypass, extension bypass, magic byte manipulation, path traversal in file... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-file-upload/SKILL.md))
- **`offensive-graphql`**: Offensive methodology for attacking GraphQL APIs during penetration tests and bug bounty engagements. Covers the full at... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-graphql/SKILL.md))
- **`offensive-idor`**: IDOR (Insecure Direct Object Reference) testing checklist: object ID enumeration, horizontal/vertical privilege escalati... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-idor/SKILL.md))
- **`offensive-open-redirect`**: Open redirect vulnerability checklist: parameter identification, bypass techniques (URL encoding, double slashes, CRLF i... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-open-redirect/SKILL.md))
- **`offensive-parameter-pollution`**: HTTP parameter pollution (HPP) checklist: duplicate parameter injection, backend vs frontend parsing differences, WAF by... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-parameter-pollution/SKILL.md))
- **`offensive-race-condition`**: Race condition (TOCTOU) testing checklist: identifying timing windows, Burp Suite Turbo Intruder, Last-Byte sync techniq... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-race-condition/SKILL.md))
- **`offensive-rce`**: Remote Code Execution testing checklist: OS command injection, SSTI-to-RCE, deserialization RCE, file upload RCE, XXE wi... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-rce/SKILL.md))
- **`offensive-request-smuggling`**: HTTP request smuggling checklist: CL.TE, TE.CL, TE.TE variants, detection with timing and differential responses, WAF by... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-request-smuggling/SKILL.md))
- **`offensive-sqli`**: SQL injection testing skill for offensive security assessments and bug bounty hunting. Covers error-based, UNION-based, ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-sqli/SKILL.md))
- **`offensive-ssrf`**: Server-Side Request Forgery testing checklist: SSRF discovery, blind SSRF with out-of-band, cloud metadata endpoints (AW... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-ssrf/SKILL.md))
- **`offensive-ssti`**: Dense description covering Server-Side Template Injection across Jinja2, Twig, Freemarker, Velocity, Pebble, Smarty, Mak... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-ssti/SKILL.md))
- **`offensive-waf-bypass`**: WAF bypass techniques checklist: encoding bypass (URL/HTML/Unicode/double encoding), case variation, comment injection, ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-waf-bypass/SKILL.md))
- **`offensive-xss`**: Cross-Site Scripting testing checklist: stored/reflected/DOM/blind XSS discovery, polyglot payloads, CSP bypass, XSS fil... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-xss/SKILL.md))
- **`offensive-xxe`**: XML External Entity injection testing checklist: classic XXE, blind XXE (out-of-band), XXE via file upload (SVG/docx), X... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/web/offensive-xxe/SKILL.md))

### Wireless
- **`offensive-bluetooth-ble`**: Bluetooth Low Energy (BLE) attack methodology: GATT enumeration, characteristic read/write without auth, pairing downgra... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-bluetooth-ble/SKILL.md))
- **`offensive-bluetooth-classic`**: Bluetooth Classic (BR/EDR) attack methodology: device discovery, service enumeration via SDP, LMP/L2CAP layer attacks, l... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-bluetooth-classic/SKILL.md))
- **`offensive-deauth-disassoc`**: Deauthentication and disassociation attacks against 802.11 networks: targeted single-client deauth for handshake capture... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-deauth-disassoc/SKILL.md))
- **`offensive-evil-twin`**: Evil Twin / KARMA / Mana access point methodology: rogue AP construction with hostapd-mana / wifiphisher / airgeddon, KA... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-evil-twin/SKILL.md))
- **`offensive-krack-fragattacks`**: KRACK (CVE-2017-13077..082) and FragAttacks (CVE-2020-24586..588 + 26139-26147): key reinstallation, fragmentation, and ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-krack-fragattacks/SKILL.md))
- **`offensive-lorawan-sub-ghz`**: LoRaWAN and sub-GHz (433 / 868 / 915 MHz) attack methodology: LoRaWAN ABP/OTAA join attack, network/session key reuse, f... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-lorawan-sub-ghz/SKILL.md))
- **`offensive-wifi`**: Wireless / 802.11 attack methodology for red team engagements and wireless security assessments. Covers monitor-mode set... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-wifi/SKILL.md))
- **`offensive-wifi-recon`**: Wi-Fi reconnaissance methodology: adapter selection, monitor mode and packet injection setup, regulatory domain handling... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-wifi-recon/SKILL.md))
- **`offensive-wpa-enterprise`**: WPA/WPA2/WPA3-Enterprise (802.1X / EAP) attack methodology: EAP method identification (PEAP-MSCHAPv2, EAP-TTLS, EAP-TLS,... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-wpa-enterprise/SKILL.md))
- **`offensive-wpa2-psk`**: WPA/WPA2-PSK attack methodology: four-way handshake capture via targeted deauthentication, PMKID attacks (no client requ... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-wpa2-psk/SKILL.md))
- **`offensive-wpa3-sae`**: WPA3 / SAE (Simultaneous Authentication of Equals) attack methodology: transition-mode (mixed WPA2/WPA3) downgrade, Drag... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-wpa3-sae/SKILL.md))
- **`offensive-wps`**: WPS (Wi-Fi Protected Setup) PIN attack methodology: Pixie Dust offline attack against vulnerable chipsets (Ralink, Realt... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-wps/SKILL.md))
- **`offensive-z-wave`**: Z-Wave attack methodology: sniffing with Z-Force / EZ-Wave / RTL-SDR + ZniffMobile, S0 (legacy) network-key derivation f... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-z-wave/SKILL.md))
- **`offensive-zigbee-thread-matter`**: Zigbee, Thread, and Matter mesh-protocol attack methodology: IEEE 802.15.4 sniffing with TI CC2531 / CC2540 / Sonoff Zig... ([view](file:////mnt/data/Projects/malaysia-testing-cup-2026/references/claude-red/Skills/wireless/offensive-zigbee-thread-matter/SKILL.md))
