#!/usr/bin/env python3
"""Check that every inline <script> and <style> in a page is allowed by its CSP hash.

Usage:  python3 tools/check_csp.py [index.html]
        python3 tools/check_csp.py --fix <file>   # rewrite the CSP with the correct hashes

JSON data blocks (<script type="application/json">) are not executed and are skipped.
Exit code 1 if any block is missing from the CSP.
"""
import base64, hashlib, re, sys

def sha(text):
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode() + "'"

def blocks(html, tag):
    pat = rf"<{tag}(?P<attrs>[^>]*)>(?P<body>.*?)</{tag}>"
    for m in re.finditer(pat, html, re.S):
        attrs = m.group("attrs")
        if "src=" in attrs or "application/json" in attrs:
            continue
        yield m.group("body")

def check(path, fix=False):
    html = open(path, encoding="utf-8").read()
    m = re.search(r'(http-equiv="Content-Security-Policy" content=")([^"]+)(")', html)
    if not m:
        print(f"{path}: no CSP meta tag"); return False
    csp = m.group(2)
    ok = True
    for tag, directive in (("script", "script-src"), ("style", "style-src")):
        need = [sha(b) for b in blocks(html, tag)]
        d = re.search(rf"{directive} ([^;]+)", csp)
        have = d.group(1).split() if d else []
        missing = [h for h in need if h not in have]
        for h in need:
            print(f"{path}: {tag:6} {h[:28]}…  {'OK' if h in have else 'MISSING'}")
        if missing:
            ok = False
            if fix:
                keep = [x for x in have if not x.startswith("'sha256-")]
                new = f"{directive} " + " ".join(need + keep)
                csp = csp.replace(d.group(0), new) if d else csp
    if fix and not ok:
        html = html[:m.start(2)] + csp + html[m.end(2):]
        open(path, "w", encoding="utf-8").write(html)
        print(f"{path}: CSP rewritten with current hashes")
        return True
    return ok

if __name__ == "__main__":
    args = sys.argv[1:]
    fix = "--fix" in args
    files = [a for a in args if a != "--fix"] or ["index.html"]
    results = [check(f, fix) for f in files]
    sys.exit(0 if all(results) else 1)
