## Auth Documentation Guide

Understanding authentication in FastAPI comes down to mastering 
four core building blocks: 
* Imports & Configuration, 
* OAuth2 Token Extraction, 
* User Registration, and 
* Login/Verification.

---

1. Imports and Setup
External Libraries & Core FastAPI Components
```codesnippts
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
```
* import jwt (PyJWT): Responsible for decoding, validating, and encoding JSON Web Tokens.

* APIRouter: Groups related API endpoints (like authentication routes) into a modular mini-application so your main.py stays clean.

* Depends: FastAPI's Dependency Injection system. It automatically executes a helper function (e.g., getting a database connection or
extracting a token) and passes the result straight into your path function.

* HTTPException & status: HTTPException stops route execution immediately and sends an HTTP error response to the client. status provides readable constants like status.HTTP_401_UNAUTHORIZED instead of raw magic numbers like 401.

* OAuth2PasswordBearer: The security scheme that looks for a Bearer <token> in the HTTP Authorization request header.

* OAuth2PasswordRequestForm: Parses incoming login requests sent via URL-encoded form data (application/x-www-form-urlencoded), providing form_data.username and form_data.password.

* Session: Provides type hinting for the SQLAlchemy database session object.

---

### Project-Specific Imports

```code
from app.database import get_db
from app.models import UserModel
from app.schemas import Token, UserCreate, UserResponse
from app.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)
```

* get_db: Yields a database session instance per request and closes it when the request completes.

* UserModel: The SQLAlchemy class representing the users table in your database.

* Token, UserCreate, UserResponse: Pydantic schemas validating incoming request bodies and defining what fields get sent back in HTTP responses.

* SECRET_KEY & ALGORITHM: Secret signature key and signature algorithm (e.g., HS256) used by PyJWT.

* get_password_hash & verify_password: Hashing utilities using Bcrypt/Argon2 to safely encrypt passwords before saving them and verify plaintext inputs during login.

* create_access_token: Encodes a payload dictionary into a signed JWT string with an expiration timestamp.

---

2. Router & Security Scheme Initialization
```code
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
```

* APIRouter(...): Prefixes every endpoint in this file with /auth (making endpoints /auth/register, /auth/token, etc.) and groups them under the "Authentication" category in the Swagger documentation.

* oauth2_scheme: Initializes FastAPI's OAuth2 scheme. Setting tokenUrl="/api/v1/auth/token" tells Swagger UI where to post credentials when you click the Authorize button.

---

3. Current User Dependency (get_current_user)

This dependency acts as a security gatekeeper for protected endpoints.
```code
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
```

---

