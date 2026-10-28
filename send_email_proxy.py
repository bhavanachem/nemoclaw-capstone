import json, os, smtplib, socket, ssl
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlparse

def proxy_socket(host, port, timeout=30):
    url = (os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
           or os.environ.get("ALL_PROXY"))
    if not url:
        raise RuntimeError("No proxy variable set in the sandbox")
    p = urlparse(url)
    s = socket.create_connection((p.hostname, p.port), timeout)
    s.sendall(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
    status = buf.split(b"\r\n")[0]
    if b" 200" not in status:
        raise RuntimeError(f"Proxy refused CONNECT: {status!r}")
    return s

class ProxySMTP_SSL(smtplib.SMTP_SSL):
    def _get_socket(self, host, port, timeout):
        raw = proxy_socket(host, port, timeout)
        return self.context.wrap_socket(raw, server_hostname=host)

config = json.loads(Path("/sandbox/hand/gmail_config.json").read_text(encoding="utf-8"))
msg = EmailMessage()
msg["From"] = config["email"]
msg["To"] = config["email"]
msg["Subject"] = "NemoClaw Gmail policy test (proxy)"
msg.set_content("Sent through the NemoClaw Gmail preset via the sandbox proxy.")

with ProxySMTP_SSL("smtp.gmail.com", 465, timeout=30,
                   context=ssl.create_default_context()) as smtp:
    smtp.login(config["email"], config["app_password"])
    smtp.send_message(msg)
print("SENT")
