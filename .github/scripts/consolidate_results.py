import json, glob

def read_json(path):
    try:
        return json.load(open(path))
    except:
        return {}

def main():
    key_leaks = len(read_json("gitleaks-report.json").get("findings", []))
    vul_scan = len(read_json("grype-report.json").get("matches", []))
    ast_findings = len(read_json("semgrep-report.json").get("results", []))
    dast_find = len(read_json("zap_report.json").get("alerts", []))

    summary = f"""
🎯 *vuln‑bank* Scan Summary:
  • Secrets found: {key_leaks}
  • Vulnerable deps: {vul_scan}
  • SAST findings: {ast_findings}
  • DAST alerts: {dast_find}
"""
    print(summary)
    # tambahan: kirim lewat Discord webhook atau email

if __name__ == "__main__":
    main()
