from fish_db import DB_PATH, connect_database, create_tables, seed_categories, seed_fish
from fish_factory import FishFactory


class AquariumManager:
    """Singleton that owns the DB connection and uses FishFactory."""

    _instance = None

    def __new__(cls, db_path=DB_PATH):
        if cls._instance is None:
            cls._instance = super(AquariumManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path=DB_PATH):
        if self._initialized:
            if self.connection is None:
                self.connection = connect_database(self.db_path)
            return

        self.db_path = db_path
        self.connection = connect_database(db_path)
        self.fish_factory = FishFactory()
        create_tables(self.connection)
        seed_categories(self.connection)
        seed_fish(self.connection)
        self._initialized = True

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_category_id(self, category_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM category WHERE name = ?", (category_name,))
        category = cursor.fetchone()

        if category is None:
            cursor.execute("INSERT INTO category (name) VALUES (?)", (category_name,))
            self.connection.commit()
            return cursor.lastrowid

        return category["id"]

    def get_fish_category(self, name):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT category.name AS category
            FROM fish
            JOIN category ON fish.category_id = category.id
            WHERE LOWER(fish.name) = LOWER(?)
            """,
            (name,),
        )
        row = cursor.fetchone()

        if row is None:
            raise ValueError(f"{name} is not available in this Auckland aquarium.")

        return row["category"]

    def save_fish(self, name, quantity):
        category = self.get_fish_category(name)
        fish = self.fish_factory.create_fish(name, quantity, category)
        category_id = self.get_category_id(category)
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO fish (name, quantity, category_id)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                quantity = excluded.quantity,
                category_id = excluded.category_id
            """,
            (fish.name, fish.quantity, category_id),
        )
        self.connection.commit()
        return fish

    def get_fish_inventory(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT fish.name, fish.quantity, category.name AS category
            FROM fish
            JOIN category ON fish.category_id = category.id
            ORDER BY category.name, fish.name
            """
        )
        rows = cursor.fetchall()
        return [
            self.fish_factory.create_fish(
                row["name"],
                row["quantity"],
                row["category"],
            )
            for row in rows
        ]

    def get_category_summary(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT category.name AS category, COALESCE(SUM(fish.quantity), 0) AS total
            FROM category
            LEFT JOIN fish ON fish.category_id = category.id
            GROUP BY category.id, category.name
            ORDER BY category.name
            """
        )
        return cursor.fetchall()

    def get_available_fish_names(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM fish ORDER BY name")
        return [row["name"] for row in cursor.fetchall()]
