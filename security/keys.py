from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PRIVATE_KEY = (BASE_DIR / "private.pem").read_text()
PUBLIC_KEY = (BASE_DIR / "public.pem").read_text()
