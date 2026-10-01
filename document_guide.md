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

* APIRouter: Groups related API endpoints (like authentication routes) into a modular mini-application so the main.py stays clean.

* Depends: FastAPI's Dependency Injection system. It automatically executes a helper function (e.g., getting a database connection or
extracting a token) and passes the result straight into the path function.

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

* UserModel: The SQLAlchemy class representing the users table in the database.

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

* token: str = Depends(oauth2_scheme): Intercepts the request, inspects the Authorization: Bearer <token> header, strips away "Bearer ", and passes the raw JWT string into token. If no header is found, FastAPI immediately responds with a 401 Unauthorized error.

* db: Session = Depends(get_db): Injects an active SQLAlchemy database session.

---

```code
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
```

* Reusable Exception: Pre-configures a standard 401 error. Including headers={"WWW-Authenticate": "Bearer"} is part of the HTTP OAuth2 specification standards.

---

```code
try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
```

* jwt.decode(...): Validates that the token was signed with the SECRET_KEY, uses ALGORITHM, and has not expired.

* payload.get("sub"): Extracts the subject ("sub") claim containing the username. If the decoding fails or "sub" is missing, a credentials_exception is thrown.

---

```code
user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception
    return user
```
* Database Lookup: Fetches the matching UserModel row from the database using the decoded username. Returning user means downstream route handlers receive the fully populated SQLAlchemy model object.

---

4. User Registration Endpoint (/register)

```code
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
```

* response_model=UserResponse: Filters the returned model through Pydantic, ensuring sensitive fields like hashed_password are never exposed to the client.

* status_code=status.HTTP_201_CREATED: Sets the standard REST status code (201 Created) for successful resource creation.

---

```code
if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
```

* Uniqueness Checks: Queries SQLite/PostgreSQL to prevent duplicate emails or usernames before attempting insertion.

---

```code
hashed_pwd = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        username=user.username,
        hashed_password=hashed_pwd,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

* Password Hashing: Converts plain text (e.g., "mysecurepassword") into a salted hash (e.g., "$2b$12$e8...").

* Persistence: Adds the new user instance to the session, commits the transaction to disk, refreshes db_user to retrieve its generated auto-incrementing id, and returns it.

---

5. Login Endpoint (/token)

```code
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
```

* OAuth2PasswordRequestForm: Captures credentials submitted as form data (form_data.username and form_data.password).

---

```code
user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

* Validation: Fetches the user record by username and uses verify_password() to compare the plain text password against user.hashed_password. Returns 401 Unauthorized if either check fails.

---

```code
access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

* Token Issuance: Encodes {"sub": "johndoe"} into a JWT and returns a dictionary matching the Token schema structure:

```code
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

---

6. Current User Profile Endpoint (/me)

```code
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
```

* How It Works: Injects get_current_user. If a valid token is supplied in the request header, get_current_user extracts the user object and passes it to current_user. The function simply returns that object, which UserResponse serializes back to JSON.

---
