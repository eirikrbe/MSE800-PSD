
# auth_service.py

import bcrypt
import secrets
from datetime import datetime, timedelta, timezone
from services.user_factory import UserFactory
from database.user_queries import (
    add_user,
    get_user_by_email,
    admin_exists,
    set_reset_token,
    update_password,
)


class AuthService:
    """Handles password hashing, registration rules, and role-based login."""

    RESET_TOKEN_TTL_MINUTES = 15

    def __init__(self, db_manager):
        """Dependency injection of database manager."""
        self.db_manager = db_manager

    def hash_password(self, password):
        raw_password = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password, salt)
        return hashed_password.decode("utf-8")

    def verify_password(self, password, stored_hash):
        raw_password = password.encode("utf-8")
        stored_hash = stored_hash.encode("utf-8")
        return bcrypt.checkpw(raw_password, stored_hash)

    def admin_exists(self):
        return admin_exists(self.db_manager)

    def user_exists(self, email):
        user = get_user_by_email(self.db_manager, email)
        return user is not None

    def get_user_by_email(self, email):
        return get_user_by_email(self.db_manager, email)

    def register_user(self, full_name, email, password, phone=None, role="customer"):
        existing = get_user_by_email(self.db_manager, email)

        if existing:
            raise ValueError("Email already registered.")

        role_cleaned = role.strip().lower()
        password_hash = self.hash_password(password)

        user_id = add_user(
            self.db_manager,
            full_name,
            email,
            phone,
            password_hash,
            role_cleaned
        )

        new_user = UserFactory.create_user(
            role_cleaned,
            full_name,
            email,
            password_hash,
            phone,
            user_id
        )

        return new_user

    def login(self, email, password):
        user_row = get_user_by_email(self.db_manager, email)

        if not user_row:
            return None

        if self.verify_password(password, user_row["password_hash"]):
            return UserFactory.create_user(
                user_row["role"],
                user_row["full_name"],
                user_row["email"],
                user_row["password_hash"],
                user_row["phone"],
                user_row["user_id"],
                user_row["created_at"]
            )

        return None

    def request_password_reset(self, email):
        """Generate a time-limited reset code for the given email.

        Raises ValueError if no account exists with that email.
        Returns the generated reset token (in a real system this would be
        emailed to the user instead of returned directly).
        """
        user_row = get_user_by_email(self.db_manager, email)

        if not user_row:
            raise ValueError("No account found with that email.")

        token = secrets.token_hex(4).upper()
        expires_at = (
            datetime.now(timezone.utc) + timedelta(minutes=self.RESET_TOKEN_TTL_MINUTES)
        ).isoformat()

        set_reset_token(self.db_manager, email, token, expires_at)

        return token

    def reset_password(self, email, token, new_password):
        """Validate a reset code and update the user's password.

        Raises ValueError if the account doesn't exist, no reset was
        requested, the code doesn't match, or the code has expired.
        On success, stores the new bcrypt hash and clears the reset code.
        """
        user_row = get_user_by_email(self.db_manager, email)

        if not user_row:
            raise ValueError("No account found with that email.")

        stored_token = user_row["reset_token"]
        expires_at = user_row["reset_expires"]

        if not stored_token or not expires_at:
            raise ValueError("No password reset was requested for this account.")

        if token.strip().upper() != stored_token:
            raise ValueError("Invalid reset code.")

        if datetime.now(timezone.utc) > datetime.fromisoformat(expires_at):
            raise ValueError("Reset code has expired. Please request a new one.")

        password_hash = self.hash_password(new_password)
        update_password(self.db_manager, email, password_hash)
