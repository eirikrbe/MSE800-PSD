# Login / Registration Demo System for Ako-Puku

A minimal authentication system for **Ako-Puku** (A Web-Based Te Reo Māori Flashcard and Learner Progress System), covering account **registration**, **login**, and **forgot password** via a command-line interface. The system uses a single SQLite `users` table and a small set of well-separated modules (CLI, Services, Database, Models) to keep the codebase lean and easy to read.

**DEVELOPMENT TEAM - Group E**

- Yirong Chen
- Eric Gomez

## System Architecture

```mermaid
graph TB
    subgraph CLI["CLI Layer"]
        Menu[main_menu<br/>Login / Register / Forgot Password / Exit]
    end

    subgraph Svc["Service Layer"]
        Auth[AuthService<br/>hash & verify password<br/>register_user / login<br/>request_password_reset / reset_password]
        Factory[UserFactory<br/>builds Customer / Admin]
    end

    subgraph Models["Domain Models"]
        User[User]
        Customer[Customer]
        Admin[Admin]
    end

    subgraph DB["Database Layer"]
        Manager[DatabaseManager<br/>connect / execute / fetch]
        Queries[user_queries<br/>add_user / get_user_by_email]
    end

    Store[(SQLite<br/>users table)]

    Menu --> Auth
    Auth --> Factory
    Factory --> Customer
    Factory --> Admin
    Customer --> User
    Admin --> User
    Auth --> Queries
    Queries --> Manager
    Manager --> Store
```

## Module Breakdown

```mermaid
graph LR
    subgraph M1["cli"]
        main_menu[main_menu.py<br/>menu loop & prompts]
        input_helpers[input_helpers.py]
        display_helpers[display_helpers.py]
    end

    subgraph M2["services"]
        auth_service[auth_service.py<br/>register_user, login,<br/>hash_password, verify_password]
        user_factory[user_factory.py<br/>create_user by role]
    end

    subgraph M3["models"]
        user[user.py]
        customer[customer.py]
        admin[admin.py]
    end

    subgraph M4["database"]
        database_manager[database_manager.py<br/>SQLite connection & schema]
        user_queries[user_queries.py<br/>SQL for users table<br/>incl. reset_token / reset_expires]
    end

    main_menu --> auth_service
    auth_service --> user_factory
    user_factory --> customer
    user_factory --> admin
    customer --> user
    admin --> user
    auth_service --> user_queries
    user_queries --> database_manager
```

## Class Diagram

```mermaid
classDiagram
    class User {
        +int user_id
        +str full_name
        +str email
        +str phone
        +str password_hash
        +str role
        +str created_at
        +get_user_details()
    }

    class Customer {
        +role = "customer"
    }

    class Admin {
        +role = "admin"
    }

    class UserFactory {
        +create_user(role, full_name, email, password_hash, phone, user_id, created_at) User
    }

    class AuthService {
        -db_manager
        +int RESET_TOKEN_TTL_MINUTES
        +hash_password(password) str
        +verify_password(password, stored_hash) bool
        +register_user(full_name, email, password, phone, role) User
        +login(email, password) User
        +request_password_reset(email) str
        +reset_password(email, token, new_password)
        +user_exists(email) bool
        +admin_exists() bool
    }

    User <|-- Customer
    User <|-- Admin
    UserFactory ..> User : creates
    AuthService ..> UserFactory : uses
```

## Registration Flow

```mermaid
sequenceDiagram
    participant U as User
    participant Menu as main_menu (CLI)
    participant Auth as AuthService
    participant Bcrypt as bcrypt
    participant DB as DatabaseManager
    participant Store as SQLite users table

    U->>Menu: Select "Register"
    Menu->>U: Prompt for full name, email, password, phone
    U->>Menu: Enter details (plaintext password)
    Menu->>Auth: register_user(full_name, email, password, phone)
    Auth->>DB: get_user_by_email(email)
    alt Email already exists
        DB-->>Auth: existing user row
        Auth-->>Menu: raise ValueError("Email already registered.")
        Menu-->>U: Show error, return to menu
    else Email available
        DB-->>Auth: None
        Auth->>Bcrypt: hash_password(password)
        Bcrypt->>Bcrypt: gensalt()
        Bcrypt->>Bcrypt: hashpw(password, salt)
        Bcrypt-->>Auth: password_hash (utf-8 string)
        Note over Auth: plaintext password is discarded,<br/>only password_hash is kept
        Auth->>DB: add_user(full_name, email, phone, password_hash, role)
        DB->>Store: INSERT INTO users (..., password_hash, ...)
        DB-->>Auth: new user_id
        Auth->>Auth: UserFactory.create_user(...)
        Auth-->>Menu: Customer instance
        Menu-->>U: "Registration successful!"
    end
```

## Login Flow

```mermaid
sequenceDiagram
    participant U as User
    participant Menu as main_menu (CLI)
    participant Auth as AuthService
    participant DB as DatabaseManager
    participant Store as SQLite users table
    participant Bcrypt as bcrypt

    U->>Menu: Select "Login"
    Menu->>U: Prompt for email and password
    U->>Menu: Enter credentials (plaintext password)
    Menu->>Auth: login(email, password)
    Auth->>DB: get_user_by_email(email)
    DB->>Store: SELECT * FROM users WHERE email = ?
    alt User not found
        Store-->>DB: no row
        DB-->>Auth: None
        Auth-->>Menu: None
        Menu-->>U: "Invalid email or password"
    else User found
        Store-->>DB: user row (incl. password_hash, role)
        DB-->>Auth: user row
        Auth->>Bcrypt: verify_password(password, stored password_hash)
        Bcrypt->>Bcrypt: checkpw(password, password_hash)
        Bcrypt-->>Auth: True / False
        alt Password matches
            Auth->>Auth: UserFactory.create_user(role, ...)
            Auth-->>Menu: Customer or Admin instance
            Menu-->>U: "Welcome back, {full_name}!"
        else Password mismatch
            Auth-->>Menu: None
            Menu-->>U: "Invalid email or password"
        end
    end
```

## Forgot Password Flow

The CLI demo combines token generation and reset into a single interactive flow: the reset code would be emailed in a production system, but here it is printed to the console so the flow can be tested end-to-end without an email provider.

```mermaid
sequenceDiagram
    participant U as User
    participant Menu as main_menu (CLI)
    participant Auth as AuthService
    participant DB as DatabaseManager
    participant Store as SQLite users table
    participant Bcrypt as bcrypt

    U->>Menu: Select "Forgot Password"
    Menu->>U: Prompt for account email
    U->>Menu: Enter email
    Menu->>Auth: request_password_reset(email)
    Auth->>DB: get_user_by_email(email)
    DB->>Store: SELECT * FROM users WHERE email = ?
    alt Email not found
        Store-->>DB: no row
        DB-->>Auth: None
        Auth-->>Menu: raise ValueError("No account found with that email.")
        Menu-->>U: Show error, return to menu
    else Email found
        Store-->>DB: user row
        DB-->>Auth: user row
        Auth->>Auth: token = secrets.token_hex(4)<br/>expires_at = now + 15 min
        Auth->>DB: set_reset_token(email, token, expires_at)
        DB->>Store: UPDATE users SET reset_token, reset_expires
        Auth-->>Menu: token
        Menu-->>U: Display reset code<br/>(stand-in for emailed code)

        U->>Menu: Enter reset code + new password
        Menu->>Auth: reset_password(email, token, new_password)
        Auth->>DB: get_user_by_email(email)
        DB->>Store: SELECT * FROM users WHERE email = ?
        Store-->>DB: user row (reset_token, reset_expires)
        DB-->>Auth: user row

        alt Token missing / mismatched / expired
            Auth-->>Menu: raise ValueError(reason)
            Menu-->>U: Show error, return to menu
        else Token valid
            Auth->>Bcrypt: hash_password(new_password)
            Bcrypt-->>Auth: new password_hash
            Auth->>DB: update_password(email, new password_hash)
            DB->>Store: UPDATE users SET password_hash,<br/>reset_token = NULL, reset_expires = NULL
            Auth-->>Menu: success
            Menu-->>U: "Password reset successfully"
        end
    end
```

## Password Hashing & Storage (bcrypt)

`AuthService` never stores or compares plaintext passwords. It relies on `bcrypt` for one-way hashing (registration) and constant-style verification (login).

```mermaid
flowchart TD
    A[Plaintext password from user] --> B["hash_password(password)"]
    B --> C["bcrypt.gensalt()<br/>generates random salt"]
    C --> D["bcrypt.hashpw(password, salt)"]
    D --> E["password_hash<br/>(utf-8 string, salt embedded)"]
    E --> F[("users.password_hash<br/>column in SQLite")]

    G[Plaintext password at login] --> H["verify_password(password, stored_hash)"]
    F -.->|loaded by get_user_by_email| H
    H --> I["bcrypt.checkpw(password, stored_hash)"]
    I --> J{Match?}
    J -->|Yes| K[Login succeeds]
    J -->|No| L[Login rejected]
```

**Key points:**

- `hash_password()` is called once during `register_user()` — the plaintext password is hashed with a freshly generated salt (`bcrypt.gensalt()`) and the result (`password_hash`) is the **only** thing written to the `users` table.
- `password_hash` is a self-contained bcrypt string (algorithm version + cost factor + salt + hash), so no separate `salt` column is needed.
- `verify_password()` is called once during `login()` — it re-hashes the submitted password using the salt embedded in `stored_hash` via `bcrypt.checkpw()` and compares the result, without ever decrypting the stored hash.
- The plaintext password only ever exists in memory for the duration of `register_user()` / `login()` and is never logged or persisted.

## Data Model

```mermaid
erDiagram
    USERS {
        int user_id PK
        string full_name
        string email UK
        string phone
        string password_hash "bcrypt hash (salt + hash combined)"
        string role "customer | admin"
        string created_at
        string reset_token "nullable, set by forgot-password flow"
        string reset_expires "nullable, ISO 8601 UTC timestamp"
    }
```

## Design Principles

- **Maintainability** — Clear separation between CLI, services, models and database layers, each with a single responsibility.
- **Security** — Passwords are never stored in plaintext; `bcrypt` is used to hash and verify credentials.
- **Extensibility** — `UserFactory` and the `User`/`Customer`/`Admin` hierarchy allow new roles or fields (e.g. learner progress) to be added without reworking the auth flow.
- **Readability** — A single `users` table and three CLI actions (Login / Register / Forgot Password) keep the whole flow easy to follow at a glance.

## Future Enhancements

- Profile management (edit full name, add date of birth)
- Send the reset code by email instead of printing it to the console
- Integration with the Ako-Puku flashcard and learner progress modules

## Running the Demo

```bash
pip install -r requirements.txt
python3 main.py
```

The app creates its own `login_signup.db` SQLite file on first run.
