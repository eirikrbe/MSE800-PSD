
# user_queries.py

def add_user(db_manager, full_name, email, phone, password_hash, role):
    query = """
        INSERT INTO users (full_name, email, phone, password_hash, role)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor = db_manager.execute_query(
        query,
        (full_name, email, phone, password_hash, role)
    )
    return cursor.lastrowid


def get_user_by_email(db_manager, email):
    query = "SELECT * FROM users WHERE email = ?"
    return db_manager.fetch_one(query, (email,))


def get_user_by_id(db_manager, user_id):
    query = "SELECT * FROM users WHERE user_id = ?"
    return db_manager.fetch_one(query, (user_id,))

def admin_exists(db_manager):
    query = "SELECT 1 FROM users WHERE role = 'admin' LIMIT 1"
    return db_manager.fetch_one(query) is not None
