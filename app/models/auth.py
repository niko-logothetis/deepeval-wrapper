from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str
    expires_in: Optional[int] = None


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None
    scopes: Optional[list] = []


class User(BaseModel):
    """User model."""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    scopes: Optional[list] = []


class UserInDB(User):
    """User model with hashed password."""
    hashed_password: str


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class APIKeyRequest(BaseModel):
    """API key creation request."""
    name: str
    description: Optional[str] = None
    expires_in_days: Optional[int] = 30


class APIKeyResponse(BaseModel):
    """API key response."""
    key_id: str
    name: str
    api_key: str  # Only returned on creation
    created_at: str
    expires_at: Optional[str] = None
    description: Optional[str] = None
