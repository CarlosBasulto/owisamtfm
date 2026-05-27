#import whois
from core.base_module import BaseModule


class WhoisLookup(BaseModule):
    def __init__(self):
        super().__init__("WHOIS Lookup (OSINT)")

    def run(self, data):
        results = []

        for domain in data.get("domains", []):
            try:
                w = whois.whois(domain)

                results.append({
                    "domain": domain,
                    "registrar": w.registrar,
                    "creation_date": str(w.creation_date),
                    "expiration_date": str(w.expiration_date),
                    "updated_date": str(w.updated_date),
                    "name_servers": w.name_servers,
                    "status": w.status,
                    "emails": w.emails
                })

            except Exception as e:
                results.append({
                    "domain": domain,
                    "error": str(e)
                })

        data["whois"] = results
        return data