# Login / Registration System For Ako-puku demo


A minimal authentication system covering registration, login, profile management (Full Name, Date of Birth), and a "Forgot Password" flow. This simplified version removes extra layers and uses a single table to keep the system lean and easy to read.

**DEVELOPMENT TEAM - Group E**

- Yirong Chen
- Eric Gomez

## System Architecture

```mermaid
graph TB
    subgraph FE["Frontend"]
        Pages[Register / Login / Profile / Reset Pages]
    end

    subgraph App["Backend"]
        Auth[Auth Module<br/>register / login / logout]
        User[User Module<br/>profile + password reset]
    end

    DB[(Users Table)]

    Pages --> Auth
    Pages --> User
    Auth --> DB
    User --> DB
```

## Module Breakdown

```mermaid
graph LR
    subgraph M1["Auth Module"]
        A1[Register: validate, hash password, store]
        A2[Login: verify credentials, issue session]
        A3[Logout: clear session]
    end

    subgraph M2["User Module"]
        U1[View / edit profile<br/>Full Name + DOB]
        U2[Forgot password: generate token, send email]
        U3[Reset password: validate token, set new password]
    end
```

## Registration & Login Flow

```mermaid
sequenceDiagram
    participant U as User
    participant API as Backend
    participant DB as Database

    Note over U,DB: Registration
    U->>API: Full Name / DOB / email / password
    API->>API: Validate + hash password
    API->>DB: Insert user record
    API-->>U: Success, go to login

    Note over U,DB: Login
    U->>API: email + password
    API->>DB: Query user
    API->>API: Compare password hash
    alt Valid
        API-->>U: Login success (session)
    else Invalid
        API-->>U: Credential error
    end
```

## Forgot Password Flow

```mermaid
sequenceDiagram
    participant U as User
    participant API as Backend
    participant DB as Database
    participant Mail as Email

    U->>API: Enter registered email
    API->>API: Generate time-limited reset token
    API->>DB: Save token + expiry on user row
    API->>Mail: Send reset link
    Mail-->>U: Email received
    U->>API: Open link + set new password
    API->>DB: Validate token + expiry
    alt Valid
        API->>DB: Update password, clear token
        API-->>U: Reset success
    else Expired / invalid
        API-->>U: Reject, prompt to re-request
    end
```

## Data Model

```mermaid
erDiagram
    USERS {
        int id PK
        string email UK
        string password_hash
        string full_name
        date date_of_birth
        string reset_token
        datetime reset_expires
    }
```

## Design Principles

- **Maintainability** — Only two backend modules (Auth, User) with clear responsibilities; no redundant controller/service split.
- **Scalability** — Modules are independent, so features like two-factor auth or a separate reset-token table can be added later without restructuring.
- **Readability** — A single table and a small set of flows mean newcomers can grasp the whole system at a glance.

> Note: This is the lean version. If the project is graded on layered architecture or extensibility, the fuller multi-layer design may score better.
