
from models.customer import Customer
from models.admin import Admin


class UserFactory:
    @staticmethod
    def create_user(role, full_name, email, password_hash, phone=None, user_id=None, created_at=None):
        """Factory method returning a domain user instance based on `role`.

        Design notes:
        - Centralizes concrete type selection (`Customer` vs `Admin`) to keep
          service code decoupled from model constructors (Factory pattern).
        - Validates `role` and raises `ValueError` for unknown roles.
        - Preserves DB identifiers (`user_id`) and timestamps (`created_at`).
        """
        if not role:
            raise ValueError("Role is required to create a user.")
        
        role = role.strip().lower()
        
        if role == 'customer':
            return Customer(full_name, email, password_hash, phone, user_id, created_at)
        elif role == 'admin':
            return Admin(full_name, email, password_hash, phone, user_id, created_at)
        else:
            raise ValueError(f"Invalid role {role}. Must be 'customer' or 'admin'.")

    