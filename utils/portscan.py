import nmap

def scan_ports(target):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=target, arguments='-sS -Pn -T4 -F')
    except Exception as e:
        return [f"Scan failed: {e}"]

    results = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in sorted(ports):
                state = nm[host][proto][port]["state"]
                results.append(f"{host}:{port}/{proto} - {state}")
    return results