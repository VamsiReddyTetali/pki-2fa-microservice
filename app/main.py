from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
import os
from app.crypto_utils import decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code, get_remaining_seconds

app = FastAPI()

SEED_PATH = "/data/seed.txt"

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(data: dict = Body(...)):
    encrypted_seed_b64 = data.get("encrypted_seed")
    if not encrypted_seed_b64:
        raise HTTPException(status_code=400, detail={"error": "Missing encrypted_seed"})

    try:
        with open("student_private.pem", "rb") as f:
            private_pem = f.read()
        from cryptography.hazmat.primitives import serialization
        private_key = serialization.load_pem_private_key(private_pem, password=None)

        hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

        os.makedirs("/data", exist_ok=True)
        with open(SEED_PATH, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Decryption failed"})

@app.get("/generate-2fa")
async def generate_2fa():
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    with open(SEED_PATH) as f:
        hex_seed = f.read().strip()
    code = generate_totp_code(hex_seed)
    valid_for = get_remaining_seconds()
    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
async def verify_2fa(data: dict = Body(...)):
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    with open(SEED_PATH) as f:
        hex_seed = f.read().strip()
    valid = verify_totp_code(hex_seed, str(code))
    return {"valid": valid}