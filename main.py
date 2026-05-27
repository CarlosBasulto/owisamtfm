import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from  core.engine import Engine
from modules.domain.dns_resolver import DNSResolver
from modules.domain.subdomain_enum import SubdomainEnum
from modules.domain.subdomain_enum_api import SubdomainEnumAPI
from modules.osint.whois_lookup import WhoisLookup
from modules.bruteforce.http_login_bruteforce import HTTPLoginBruteforce
from modules.bruteforce.cpanel_bruteforce import CPanelBruteforce
from modules.bruteforce.ftp_bruteforce import FTPBruteforce

if __name__ == "__main__":
    data = {
        "domains": ["renegados.es"],
        "ips": []
    }

    modules = [
       DNSResolver(),
       WhoisLookup(),
       SubdomainEnum(),
       SubdomainEnumAPI(),
       CPanelBruteforce("https://217.160.0.231/login_up.php"),
       FTPBruteforce("217.160.230.87")
    ]

    engine = Engine(modules)
    result = engine.execute(data)

    print(result)