import pyotp
import base64
import time

def hex_to_base32(hex_seed: str) -> str:
    return base64.b32encode(bytes.fromhex(hex_seed)).decode()

def generate_totp_code(hex_seed: str) -> str:
    totp = pyotp.TOTP(hex_to_base32(hex_seed))
    return totp.now()

def verify_totp_code(hex_seed: str, code: str) -> bool:
    totp = pyotp.TOTP(hex_to_base32(hex_seed))
    return totp.verify(code, valid_window=1)

def get_remaining_seconds() -> int:
    return 30 - int(time.time() % 30)