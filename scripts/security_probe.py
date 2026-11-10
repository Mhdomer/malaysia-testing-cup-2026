#!/usr/bin/env python3
import argparse
import base64
import json
import sys
import urllib.parse
import urllib.request
import urllib.error

SENSITIVE_PATHS = [
    "/robots.txt",
    "/sitemap.xml",
    "/.env",
    "/.git/HEAD",
    "/config.json",
    "/api-docs",
    "/swagger.json",
    "/swagger/index.html",
    "/openapi.json",
    "/actuator/health",
    "/actuator/env",
    "/admin",
    "/admin/login",
    "/debug",
    "/version",
    "/metrics",
]

SECURITY_HEADERS = [
    ("Content-Security-Policy", "Mitigates XSS and data injection attacks"),
    ("X-Frame-Options", "Prevents Clickjacking attacks by forbidding iframe framing"),
    ("Strict-Transport-Security", "Enforces HTTPS connections (HSTS)"),
    ("X-Content-Type-Options", "Blocks MIME-type sniffing (should be 'nosniff')"),
    ("Referrer-Policy", "Controls referrer information leaked in outgoing links"),
    ("Permissions-Policy", "Restricts browser features like camera, microphone, geolocation"),
]

def check_headers_and_cors(base_url: str):
    print(f"\n=== 🛡️ HTTP SECURITY HEADERS & CORS AUDIT ===")
    print(f"Target: {base_url}")
    
    req = urllib.request.Request(
        base_url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Origin": "https://evil-attacker.example",
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            headers = dict(response.info())
            status = response.status
    except urllib.error.HTTPError as e:
        headers = dict(e.headers)
        status = e.code
    except Exception as e:
        print(f"[!] Connection failed: {e}", file=sys.stderr)
        return

    print(f"HTTP Status: {status}\n")

    # Info leaks
    for leak_hdr in ["Server", "X-Powered-By", "X-AspNet-Version", "X-Runtime"]:
        val = next((v for k, v in headers.items() if k.lower() == leak_hdr.lower()), None)
        if val:
            print(f"[!] [INFO LEAK] {leak_hdr}: {val}")

    # Missing security headers
    print("\nSecurity Headers Compliance:")
    missing_count = 0
    for hdr, desc in SECURITY_HEADERS:
        val = next((v for k, v in headers.items() if k.lower() == hdr.lower()), None)
        if val:
            print(f"  [✓] {hdr}: {val[:60]}...")
        else:
            print(f"  [✗] MISSING: {hdr} ({desc})")
            missing_count += 1

    # CORS check
    acao = next((v for k, v in headers.items() if k.lower() == "access-control-allow-origin"), None)
    acac = next((v for k, v in headers.items() if k.lower() == "access-control-allow-credentials"), None)

    print("\nCORS Policy:")
    if acao == "https://evil-attacker.example" or acao == "*":
        print(f"  [!] VULNERABLE CORS: Access-Control-Allow-Origin is '{acao}'")
        if acac and acac.lower() == "true":
            print("  [CRITICAL] CORS credentials allowed with reflected origin! (High Severity Exploit)")
    else:
        print("  [✓] CORS headers not reflecting arbitrary origin.")

    # Cookies
    set_cookies = [v for k, v in headers.items() if k.lower() == "set-cookie"]
    if set_cookies:
        print("\nCookie Security Flags:")
        for c in set_cookies:
            c_name = c.split("=")[0]
            has_secure = "secure" in c.lower()
            has_httponly = "httponly" in c.lower()
            has_samesite = "samesite" in c.lower()
            print(f"  Cookie '{c_name}': Secure={has_secure}, HttpOnly={has_httponly}, SameSite={has_samesite}")
            if not has_httponly:
                print(f"    -> [RISK] Cookie '{c_name}' lacks HttpOnly flag (Vulnerable to XSS theft)")
            if not has_secure:
                print(f"    -> [RISK] Cookie '{c_name}' lacks Secure flag (Transmitted over HTTP)")

def probe_sensitive_endpoints(base_url: str):
    parsed = urllib.parse.urlparse(base_url)
    root_url = f"{parsed.scheme}://{parsed.netloc}"
    print(f"\n=== 🔍 SENSITIVE ROUTE & ENDPOINT RECONNAISSANCE ===")
    print(f"Base: {root_url}")

    found = []
    for path in SENSITIVE_PATHS:
        url = root_url + path
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (MTC-Testing-Auditor)"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    content_len = len(resp.read(500))
                    print(f"  [!] FOUND [HTTP 200]: {path} (Data preview: {content_len} bytes)")
                    found.append((path, resp.status))
        except urllib.error.HTTPError as e:
            if e.code in [401, 403]:
                print(f"  [*] PROTECTED [HTTP {e.code}]: {path}")
            # Ignore 404
        except Exception:
            pass

    if not found:
        print("  [✓] Standard sensitive paths cleanly blocked or returning 404.")

def inspect_jwt(token: str):
    print(f"\n=== 🔑 JWT TOKEN SECURITY AUDIT ===")
    parts = token.strip().split(".")
    if len(parts) != 3:
        print("[!] Invalid JWT format (expected 3 dot-separated parts).", file=sys.stderr)
        return

    def b64_decode(data):
        padded = data + "=" * (-len(data) % 4)
        return json.loads(base64.urlsafe_b64decode(padded.encode()).decode())

    try:
        header = b64_decode(parts[0])
        payload = b64_decode(parts[1])
        print("Header:")
        print(json.dumps(header, indent=2))
        print("\nPayload:")
        print(json.dumps(payload, indent=2))

        alg = header.get("alg", "")
        if alg.lower() == "none":
            print("\n[CRITICAL] Algorithm is 'none' (Unsigned token accepted!)")
        else:
            print(f"\nAlgorithm: {alg}")
            # Generate none-alg forged token
            forged_header = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().rstrip("=")
            forged_token = f"{forged_header}.{parts[1]}."
            print(f"[+] Forged 'alg: none' token to test bypass:")
            print(f"    {forged_token}")

        if "exp" not in payload:
            print("[!] Token lacks 'exp' expiration claim (Never expires).")
    except Exception as e:
        print(f"[!] JWT parsing error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="MTC 2026 Security & Reconnaissance Auditor")
    parser.add_argument("url", nargs="?", help="Target SUT URL to audit")
    parser.add_argument("--jwt", help="Inspect and audit a JWT token string")
    parser.add_argument("--recon", action="store_true", help="Probe sensitive routes and endpoints")
    args = parser.parse_args()

    if args.jwt:
        inspect_jwt(args.jwt)
    elif args.url:
        check_headers_and_cors(args.url)
        if args.recon:
            probe_sensitive_endpoints(args.url)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
