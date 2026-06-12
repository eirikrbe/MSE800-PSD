
from models.customer import Customer
from models.admin import Admin


class UserFactory:
    """Factory to instantiate concrete user subtypes from role and DB fields."""
    @staticmethod
    def create_user(role, full_name, email, password_hash, phone=None, user_id=None, created_at=None):
        if not role:
            raise ValueError("Role is required to create a user.")

        role = role.strip().lower()

        if role == 'customer':
            return Customer(full_name, email, password_hash, phone, user_id, created_at)
        elif role == 'admin':
            return Admin(full_name, email, password_hash, phone, user_id, created_at)
        else:
            raise ValueError(f"Invalid role {role}. Must be 'customer' or 'admin'.")
