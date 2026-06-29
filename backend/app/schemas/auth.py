from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class UserMeResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    farm_id: str
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: int
    user: UserMeResponse | None = None


class LogoutResponse(BaseModel):
    status: str
