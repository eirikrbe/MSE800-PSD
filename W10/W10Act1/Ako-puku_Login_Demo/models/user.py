

class User:
    """Domain model holding authenticated user data and normalized role metadata."""
    def __init__(self, full_name, email, password_hash, role, phone=None, user_id=None, created_at=None):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.password_hash = password_hash
        self.role = role.lower()
        self.created_at = created_at


    def get_user_details(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "created_at": self.created_at
        }
