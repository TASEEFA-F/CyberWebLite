import socket

def enumerate_subdomains(domain):
    wordlist = ["www", "mail", "ftp", "blog", "dev", "test", "shop", "news", "api"]
    discovered = []

    for sub in wordlist:
        full_domain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            discovered.append(f"{full_domain} → {ip}")
        except socket.gaierror:
            continue

    return discovered