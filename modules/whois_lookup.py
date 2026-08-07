import whois
from datetime import datetime

def format_date(d):
    if isinstance(d, list):
        d = d[0] if d else None
    if isinstance(d, datetime):
        return d.strftime("%d %B %Y")
    return str(d)

def get_whois_info(domain):
    domain = domain.strip()
    if not domain or "." not in domain:
        return {"error": "Please enter a valid domain name (e.g. google.com)."}
    try:
        w = whois.whois(domain)
        if not w.domain_name:
            return {"error": f"No WHOIS data found for '{domain}'. Check the domain name and try again."}
        return {
            "domain_name": w.domain_name,
            "registrar": w.registrar,
            "creation_date": format_date(w.creation_date),
            "expiration_date": format_date(w.expiration_date),
            "name_servers": w.name_servers,
            "error": None
        }
    except Exception as e:
        return {"error": f"Could not retrieve WHOIS data for '{domain}'. It may not exist or the WHOIS server is unavailable."}