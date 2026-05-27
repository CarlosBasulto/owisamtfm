import requests
import socket
import time
from core.base_module import BaseModule


class SubdomainEnumAPI(BaseModule):
    def __init__(self):
        super().__init__("Subdomain Enumeration API (crt.sh + DNS resolve)")

    def run(self, data):
        results = []

        headers = {
            "User-Agent": "Mozilla/5.0 (ReconTool)"
        }

        for domain in data.get("domains", []):
            try:
                url = f"https://crt.sh/?q=%25.{domain}&output=json"

                response = None

                # 🔁 RETRY ANTI-RATE LIMIT
                for i in range(3):
                    response = requests.get(url, headers=headers, timeout=15)

                    if response.status_code == 200:
                        break

                    time.sleep(2)

                # ❌ fallo API
                if not response or response.status_code != 200:
                    results.append({
                        "domain": domain,
                        "error": f"crt.sh API error ({response.status_code if response else 'no response'})"
                    })
                    continue

                # 🔥 JSON SAFE PARSE
                try:
                    data_json = response.json()
                except:
                    results.append({
                        "domain": domain,
                        "error": "Invalid JSON from crt.sh"
                    })
                    continue

                # ❌ validar estructura
                if not isinstance(data_json, list):
                    results.append({
                        "domain": domain,
                        "error": "Unexpected API response format"
                    })
                    continue

                subdomains = set()
                enriched = []

                # 🔎 extracción + limpieza fuerte
                for entry in data_json:
                    name = entry.get("name_value")

                    if not isinstance(name, str):
                        continue

                    # 🔥 evitar basura enorme
                    if len(name) > 300:
                        continue

                    for sub in name.split("\n"):
                        sub = sub.strip().lower()

                        # filtros de calidad
                        if not sub:
                            continue

                        if len(sub) > 200:
                            continue

                        if "." not in sub:
                            continue

                        # 🔥 evitar error IDNA
                        try:
                            sub.encode("idna")
                        except Exception:
                            continue

                        if domain in sub:
                            subdomains.add(sub)

                # 🌐 resolución DNS
                for sub in subdomains:
                    try:
                        ip = socket.gethostbyname(sub)

                        enriched.append({
                            "subdomain": sub,
                            "ip": ip
                        })

                    except socket.gaierror:
                        enriched.append({
                            "subdomain": sub,
                            "ip": None,
                            "error": "DNS resolution failed"
                        })

                    except Exception:
                        enriched.append({
                            "subdomain": sub,
                            "ip": None,
                            "error": "Resolution error"
                        })

                results.append({
                    "domain": domain,
                    "subdomains_count": len(subdomains),
                    "subdomains": enriched
                })

            except Exception as e:
                results.append({
                    "domain": domain,
                    "error": str(e)
                })

        data["subdomains_api"] = results
        return data