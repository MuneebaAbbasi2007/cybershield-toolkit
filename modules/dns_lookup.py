import dns.resolver

def get_dns_records(domain):
    domain = domain.strip()
    if not domain or "." not in domain:
        return {"error": ["Please enter a valid domain name (e.g. google.com)."]}

    records = {}
    record_types = ["A", "MX", "NS", "TXT"]
    found_any = False

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(rdata) for rdata in answers]
            found_any = True
        except dns.resolver.NXDOMAIN:
            return {"error": [f"Domain '{domain}' does not exist."]}
        except dns.resolver.NoAnswer:
            records[rtype] = ["Not Available"]
        except Exception:
            records[rtype] = ["Not Available"]

    return records