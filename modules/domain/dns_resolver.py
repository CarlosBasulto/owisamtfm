import socket
from core.base_module import BaseModule

class DNSResolver(BaseModule):
    def __init__(self):
        super().__init__("DNS Resolver")

    def run(self, data):
        results = []

        for domain in data.get("domains", []):
            try:
                ip = socket.gethostbyname(domain)

                results.append({
                    "domain": domain,
                    "ip": ip
                })

            except socket.gaierror:
                results.append({
                    "domain": domain,
                    "ip": None,
                    "error": "No se pudo resolver"
                })

        data["dns"] = results
        return data