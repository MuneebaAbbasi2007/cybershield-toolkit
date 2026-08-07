import nmap
import time

def scan_target(target):
    target = target.strip()
    if not target:
        return {"error": "Please enter a target (e.g. scanme.nmap.org or 127.0.0.1)."}
    try:
        start = time.time()
        nm = nmap.PortScanner()
        nm.scan(target, arguments='-F')
        duration = round(time.time() - start, 2)

        if not nm.all_hosts():
            return {"error": f"'{target}' did not respond. It may be down, blocking scans, or unreachable. Try 127.0.0.1 or scanme.nmap.org."}

        results = {}
        total_ports = 0
        for host in nm.all_hosts():
            results[host] = {"state": nm[host].state(), "ports": []}
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in sorted(ports):
                    port_info = nm[host][proto][port]
                    results[host]["ports"].append({
                        "port": port,
                        "state": port_info['state'],
                        "service": port_info['name']
                    })
                    total_ports += 1

        return {"hosts": results, "scan_time": duration, "port_count": total_ports}
    except Exception as e:
        return {"error": f"Scan failed: {str(e)}. Make sure the target is reachable and try again."}