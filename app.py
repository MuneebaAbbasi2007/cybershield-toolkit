import os
from functools import wraps
from flask import Flask, render_template, request, send_file, session, redirect, url_for
from modules.hash_gen import generate_hashes
from modules.password_check import check_password_strength
from modules.whois_lookup import get_whois_info
from modules.dns_lookup import get_dns_records
from modules.scanner import scan_target
from modules.risk_analysis import analyze_risk
from modules.pdf_generator import generate_pdf_report, generate_combined_pdf_report
from modules.database import init_db, save_scan, get_all_scans

app = Flask(__name__)
app.secret_key = "cybershield_secret_key_123"

init_db()

APP_USERNAME = os.getenv("APP_USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

all_results = []
last_result = {}

def save_result(tool_name, data, ai_analysis):
    entry = {"tool": tool_name, "data": data, "ai": ai_analysis}
    all_results.append(entry)
    last_result["tool"] = tool_name
    last_result["data"] = data
    last_result["ai"] = ai_analysis
    save_scan(tool_name, data, ai_analysis)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] == APP_USERNAME and request.form["password"] == APP_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/hash", methods=["GET", "POST"])
@login_required
def hash_tool():
    result = None
    if request.method == "POST":
        text = request.form["text"]
        result = generate_hashes(text)
    return render_template("hash.html", result=result)

@app.route("/password", methods=["GET", "POST"])
@login_required
def password_tool():
    result = None
    ai_analysis = None
    if request.method == "POST":
        password = request.form["password"]
        result = check_password_strength(password)
        ai_analysis = analyze_risk("Password Strength", result)
        save_result("Password Strength", result, ai_analysis)
    return render_template("password.html", result=result, ai_analysis=ai_analysis)

@app.route("/whois", methods=["GET", "POST"])
@login_required
def whois_tool():
    result = None
    ai_analysis = None
    if request.method == "POST":
        domain = request.form["domain"]
        result = get_whois_info(domain)
        ai_analysis = analyze_risk("WHOIS Lookup", result)
        save_result("WHOIS Lookup", result, ai_analysis)
    return render_template("whois.html", result=result, ai_analysis=ai_analysis)

@app.route("/dns", methods=["GET", "POST"])
@login_required
def dns_tool():
    result = None
    ai_analysis = None
    if request.method == "POST":
        domain = request.form["domain"]
        result = get_dns_records(domain)
        ai_analysis = analyze_risk("DNS Lookup", result)
        save_result("DNS Lookup", result, ai_analysis)
    return render_template("dns.html", result=result, ai_analysis=ai_analysis)

@app.route("/scan", methods=["GET", "POST"])
@login_required
def scan_tool():
    result = None
    ai_analysis = None
    if request.method == "POST":
        target = request.form["target"]
        result = scan_target(target)
        ai_analysis = analyze_risk("Network Scan", result)
        save_result("Network Scan", result, ai_analysis)
    return render_template("scan.html", result=result, ai_analysis=ai_analysis)

@app.route("/download-report")
@login_required
def download_report():
    if not last_result:
        return "No report available yet. Run a scan first.", 400
    pdf_buffer = generate_pdf_report(last_result["tool"], last_result["data"], last_result["ai"])
    return send_file(pdf_buffer, as_attachment=True, download_name="CyberShield_Report.pdf", mimetype="application/pdf")

@app.route("/dashboard")
@login_required
def dashboard():
    total = len(all_results)
    critical = high = medium = low = 0
    for entry in all_results:
        ai_text = str(entry.get("ai", "")).lower()
        if "critical" in ai_text:
            critical += 1
        elif "high" in ai_text:
            high += 1
        elif "medium" in ai_text:
            medium += 1
        elif "low" in ai_text:
            low += 1
    safe = low
    if total > 0:
        overall_score = round(((low * 1.0 + medium * 0.6 + high * 0.3) / total) * 100)
    else:
        overall_score = 100
    summary = {
        "total": total, "critical": critical, "high": high,
        "medium": medium, "low": low, "safe": safe, "score": overall_score
    }
    return render_template("dashboard.html", results=all_results, summary=summary)

@app.route("/download-combined-report")
@login_required
def download_combined_report():
    if not all_results:
        return "No results yet. Run at least one tool first.", 400
    total = len(all_results)
    critical = high = medium = low = 0
    for entry in all_results:
        ai_text = str(entry.get("ai", "")).lower()
        if "critical" in ai_text:
            critical += 1
        elif "high" in ai_text:
            high += 1
        elif "medium" in ai_text:
            medium += 1
        elif "low" in ai_text:
            low += 1
    score = round(((low * 1.0 + medium * 0.6 + high * 0.3) / total) * 100) if total else 100
    summary = {"total": total, "critical": critical, "high": high, "medium": medium, "low": low, "score": score}
    pdf_buffer = generate_combined_pdf_report(all_results, summary)
    return send_file(pdf_buffer, as_attachment=True, download_name="CyberShield_Full_Report.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)