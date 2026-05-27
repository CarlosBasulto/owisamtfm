import socket
from core.base_module import BaseModule

class SubdomainEnum(BaseModule):
    def __init__(self, wordlist=None):
        super().__init__("Subdomain Enumerator")
        self.wordlist = wordlist or [
    # básicos
    "www", "mail", "ftp", "api", "dev", "test", "staging",

    # entornos de desarrollo
    "dev1", "dev2", "qa", "uat", "sandbox", "demo", "preprod", "prod",

    # administración
    "admin", "administrator", "panel", "cpanel", "webmail", "secure", "login",

    # servicios internos
    "ns1", "ns2", "dns", "vpn", "intranet", "portal", "internal",

    # cloud / infraestructura
    "cloud", "aws", "azure", "gcp", "storage", "cdn", "s3", "files",

    # aplicaciones comunes
    "app", "apps", "mobile", "web", "api1", "api2", "backend", "frontend",

    # monitoring / devops
    "monitor", "grafana", "jenkins", "ci", "cd", "prometheus", "logs",

    # extras comunes en empresas
    "beta", "old", "new", "legacy", "backup", "secure2", "auth"
]
    
    def run(self, data):
        results = []

        domains = data.get("domains", [])

        for domain in domains:
            found = []

            for sub in self.wordlist:
                subdomain = f"{sub}.{domain}"

                try:
                    ip = socket.gethostbyname(subdomain)

                    found.append({
                        "subdomain": subdomain,
                        "ip": ip
                    })

                except socket.gaierror:
                    # no existe ese subdominio
                    pass

            results.append({
                "domain": domain,
                "subdomains": found
            })

        data["subdomains"] = results
        return data