#!/usr/bin/env python3
"""Usage: send_report.py <report_path> "<subject>" """
import json, os, smtplib, socket, ssl, sys
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlparse

CONFIG = Path("/sandbox/hand/gmail_config.json")

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
    if b" 200" not in buf.split(b"\r\n")[0]:
        raise RuntimeError(f"Proxy refused CONNECT: {buf.split(b'\r\n')[0]!r}")
    return s

class ProxySMTP_SSL(smtplib.SMTP_SSL):
    def _get_socket(self, host, port, timeout):
        return self.context.wrap_socket(proxy_socket(host, port, timeout), server_hostname=host)

def main():
    path = Path(sys.argv[1])
    subject = sys.argv[2] if len(sys.argv) > 2 else "IoT monitoring report"
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    to = cfg.get("recipients") or [cfg["email"]]
    text = path.read_text(encoding="utf-8")

    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = cfg["email"], ", ".join(to), subject
    msg.set_content(text)
    msg.add_attachment(text.encode("utf-8"), maintype="text", subtype="plain", filename=path.name)

    smtp = ProxySMTP_SSL("smtp.gmail.com", 465, timeout=30, context=ssl.create_default_context())
    try:
        smtp.login(cfg["email"], cfg["app_password"])
        smtp.send_message(msg)
        print("SENT to", ", ".join(to), flush=True)
    finally:
        try:
            smtp.sock.settimeout(5)
            smtp.quit()
        except Exception:
            pass
    os._exit(0)

if __name__ == "__main__":
    main()
