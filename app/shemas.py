from pathlib import Path
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent


class JWTAuth(BaseModel):
    private_key_path: Path = BASE_DIR / "app/certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "app/certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
