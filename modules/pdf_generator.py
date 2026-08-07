from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import io

styles = getSampleStyleSheet()

def format_result(tool_name, data):
    """Convert raw dict results into readable paragraph text."""
    lines = []
    if not isinstance(data, dict):
        return str(data)

    if "error" in data and data["error"]:
        return f"Error: {data['error']}"

    if tool_name == "Network Scan":
        lines.append(f"Open Ports: {data.get('port_count', 'N/A')}")
        lines.append(f"Scan Time: {data.get('scan_time', 'N/A')} sec")
        for host, hdata in data.get("hosts", {}).items():
            lines.append(f"Target: {host} (Status: {hdata.get('state')})")
            for p in hdata.get("ports", []):
                lines.append(f"  Port {p['port']} - {p['service']} ({p['state']})")

    elif tool_name == "WHOIS Lookup":
        lines.append(f"Domain: {data.get('domain_name')}")
        lines.append(f"Registrar: {data.get('registrar')}")
        lines.append(f"Created: {data.get('creation_date')}")
        lines.append(f"Expires: {data.get('expiration_date')}")
        lines.append(f"Name Servers: {', '.join(data.get('name_servers') or [])}")

    elif tool_name == "DNS Lookup":
        for rtype, values in data.items():
            lines.append(f"{rtype}: {', '.join(values)}")

    elif tool_name == "Password Strength":
        lines.append(f"Strength: {data.get('strength')} ({data.get('score')}/4)")
        if data.get("warning"):
            lines.append(f"Warning: {data['warning']}")

    else:
        lines.append(str(data))

    return "<br/>".join(lines)


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.drawString(40, 20, "CyberShield Toolkit v1.0")
    canvas.drawRightString(555, 20, f"Page {doc.page}")
    canvas.restoreState()


def generate_pdf_report(tool_name, result_data, ai_analysis):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    elements.append(Paragraph("CyberShield Toolkit - Security Assessment Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Tool: {tool_name}", styles['Heading2']))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Findings:", styles['Heading2']))
    elements.append(Paragraph(format_result(tool_name, result_data), styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("AI Risk Analysis:", styles['Heading2']))
    elements.append(Paragraph(str(ai_analysis).replace('\n', '<br/>'), styles['Normal']))

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    buffer.seek(0)
    return buffer


def generate_combined_pdf_report(all_results, summary=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    elements.append(Paragraph("CyberShield Toolkit - Full Security Assessment Report", styles['Title']))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    if summary:
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        table_data = [
            ["Overall Security Score", f"{summary['score']}%"],
            ["Modules Executed", str(summary['total'])],
            ["Critical / High Risks", str(summary['critical'] + summary['high'])],
            ["Medium Risks", str(summary['medium'])],
            ["Low / Safe Risks", str(summary['low'])],
        ]
        t = Table(table_data, colWidths=[250, 150])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

    counter = {}
    for entry in all_results:
        tool = entry["tool"]
        counter[tool] = counter.get(tool, 0) + 1
        label = f"{tool} #{counter[tool]}" if counter[tool] > 1 else tool

        elements.append(Paragraph(label, styles['Heading2']))
        elements.append(Paragraph("Findings:", styles['Heading3']))
        elements.append(Paragraph(format_result(tool, entry["data"]), styles['Normal']))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("AI Risk Analysis:", styles['Heading3']))
        elements.append(Paragraph(str(entry["ai"]).replace('\n', '<br/>'), styles['Normal']))
        elements.append(Spacer(1, 20))

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    buffer.seek(0)
    return buffer