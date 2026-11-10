#!/usr/bin/env python3
import argparse
import subprocess
import sys

PAYLOADS = {
    "xss": [
        '<script>alert("MTC_XSS")</script>',
        '<img src=x onerror=alert("MTC_XSS")>',
        '"><svg onload=alert("MTC_XSS")>',
        "javascript:alert('MTC_XSS')",
        '"><iframe src="javascript:alert(`MTC_XSS`)">',
    ],
    "sql": [
        "' OR '1'='1",
        "admin' --",
        "1' ORDER BY 1--+",
        "1' UNION SELECT null, null--+",
        "' OR 1=1#",
    ],
    "unicode": [
        "🔥🎯🚀🧪",
        "النص العربي تجربة",
        "日本語テスト文字列",
        "\u202Ereversed_text_override",
        "\u200B\u200C\u200Dzero_width_chars",
    ],
    "numbers": [
        "0",
        "-1",
        "-999999999",
        "99999999999999999999",
        "2147483647",
        "2147483648",
        "-2147483648",
        "3.1415926535",
        "1e308",
        "NaN",
        "Infinity",
    ],
    "whitespace": [
        "   ",
        "\t\t\t",
        "\n\r\n",
        " leading_whitespace",
        "trailing_whitespace ",
    ],
}

def generate_bva(length: int) -> str:
    return "A" * length

def copy_to_clipboard(text: str):
    try:
        proc = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
        proc.communicate(text.encode("utf-8"))
        print("\n[✓] Copied to Wayland clipboard (wl-copy)!")
    except Exception as e:
        print(f"\n[!] Failed to copy to clipboard: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="MTC 2026 Test Data & Fuzzing Payload Generator")
    parser.add_argument(
        "--type",
        choices=["xss", "sql", "unicode", "numbers", "whitespace", "bva", "all"],
        default="all",
        help="Type of test payload to generate",
    )
    parser.add_argument("--len", type=int, default=256, help="Length for BVA string generator (default: 256)")
    parser.add_argument("--copy", action="store_true", help="Copy the first generated payload to wl-copy clipboard")
    args = parser.parse_args()

    selected_output = ""

    if args.type == "bva":
        res = generate_bva(args.len)
        print(f"--- BVA String (Length: {args.len}) ---")
        print(res)
        selected_output = res
    elif args.type == "all":
        for cat, items in PAYLOADS.items():
            print(f"=== {cat.upper()} PAYLOADS ===")
            for item in items:
                print(f"  {item}")
            print()
        bva_sample = generate_bva(args.len)
        print(f"=== BVA SAMPLE (Length: {args.len}) ===")
        print(f"  {bva_sample[:30]}... ({args.len} chars total)\n")
        selected_output = PAYLOADS["xss"][0]
    else:
        print(f"=== {args.type.upper()} PAYLOADS ===")
        for item in PAYLOADS[args.type]:
            print(f"  {item}")
        selected_output = PAYLOADS[args.type][0]

    if args.copy and selected_output:
        copy_to_clipboard(selected_output)

if __name__ == "__main__":
    main()
