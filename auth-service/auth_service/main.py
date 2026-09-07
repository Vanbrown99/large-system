from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field

from .security import create_access_token, decode_access_token, verify_password
from .store import User, UserStore

app = FastAPI(title="School ERP Authentication Service", version="1.0.0")
store = UserStore()
bearer = HTTPBearer(auto_error=False)


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["admin", "student"] = "student"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "student"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def to_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, name=user.name, email=user.email, role=user.role)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "auth"}


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest) -> UserResponse:
    try:
        user = store.add(request.name, str(request.email), request.password, request.role)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return to_response(user)


@app.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    user = store.get_by_email(str(request.email))
    if user is None or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(str(user.id), user.role))


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error
    user = store.get_by_id(payload.get("sub", ""))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/me", response_model=UserResponse)
def me(user: User = Depends(current_user)) -> UserResponse:
    return to_response(user)


@app.get("/admin/overview")
def admin_overview(user: User = Depends(current_user)) -> dict[str, str]:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return {"message": "Admin-only overview"}
