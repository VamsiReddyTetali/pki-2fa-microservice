#!/usr/local/bin/python3
import datetime
import sys
import os

timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

with open("/cron/last_code.txt", "a") as f:
    f.write(f"[{timestamp} UTC] Cron job started\n")

try:
    if not os.path.exists("/data/seed.txt"):
        with open("/cron/last_code.txt", "a") as f:
            f.write(f"[{timestamp} UTC] ERROR: Seed file not found at /data/seed.txt\n")
        sys.exit(1)

    with open("/data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    from app.totp_utils import generate_totp_code
    code = generate_totp_code(hex_seed)

    with open("/cron/last_code.txt", "a") as f:
        f.write(f"[{timestamp} UTC] 2FA Code: {code}\n")

except Exception as e:
    with open("/cron/last_code.txt", "a") as f:
        f.write(f"[{timestamp} UTC] ERROR: {str(e)}\n")