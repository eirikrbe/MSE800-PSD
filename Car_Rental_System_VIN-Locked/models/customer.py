from models.user import User


class Customer(User):
    """Thin User specialization representing a customer identity."""
    def __init__(self, full_name, email, password_hash, phone=None, user_id=None, created_at=None):
        super().__init__(
            full_name,
            email,
            password_hash,
            "customer",
            phone,
            user_id,
            created_at
        )