import bcrypt
from services.user_factory import UserFactory
from database.database_manager import DatabaseManager
from database.user_queries import add_user, get_user_by_email


class AuthService:
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

    def register_user(self, full_name, email, password, role, phone=None):
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

if __name__ == "__main__":

    db = DatabaseManager()
    auth_service = AuthService(db)

    # Run this only once, then comment it again because email is UNIQUE
    auth_service.register_user(
         "Test User4",
         "test4@example.com",
         "password123",
         "customer",
         "1234567890"
     )

    user = auth_service.login("test4@example.com", "password123")

    if user:
        print("Login successful!")
        print(user.get_user_details())
    else:
        print("Login failed.")

    db.disconnect()
    