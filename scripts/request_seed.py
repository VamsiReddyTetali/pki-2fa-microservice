import requests
import sys

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str):
    # Read your public key
    with open("student_public.pem", "r") as f:
        public_key = f.read()

    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        encrypted_seed = data["encrypted_seed"]
        with open("../encrypted_seed.txt", "w") as f:
            f.write(encrypted_seed)
        print("Success! Encrypted seed saved to encrypted_seed.txt")
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response'):
            print(e.response.text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/request_seed.py YOUR_STUDENT_ID https://github.com/yourusername/your-repo")
        sys.exit(1)
    request_seed(sys.argv[1], sys.argv[2])