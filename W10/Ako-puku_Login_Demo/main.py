
# main.py

from database.database_manager import DatabaseManager
from services.auth_service import AuthService
from cli.main_menu import main_menu


def main():
    """Start the application: initialize database and run the login/signup menu."""
    db = DatabaseManager()
    auth_service = AuthService(db)

    try:
        main_menu(auth_service)
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
