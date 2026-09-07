import sqlite3
from contextlib import contextmanager

from .settings import DATABASE_PATH


@contextmanager
def connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_amount REAL NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'CONFIRMED',
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
"""
PRODUCTS = [
    (101, "Laptop Pro 14", "Computers", 120000, 20),
    (102, "27-inch Monitor", "Displays", 32000, 35),
    (103, "Wireless Keyboard", "Accessories", 4500, 80),
    (104, "USB-C Dock", "Accessories", 12500, 45),
]
def initialize_database():
    with connection() as db:
        db.executescript(SCHEMA)

        db.executemany(
            """
            INSERT OR IGNORE INTO products
            (product_id, name, category, unit_price, stock)
            VALUES (?, ?, ?, ?, ?)
            """,
            PRODUCTS,
        )

def list_products(category=None):
    with connection() as db:

        if category:
            rows = db.execute(
                """
                SELECT *
                FROM products
                WHERE lower(category) = lower(?)
                ORDER BY product_id
                """,
                (category,),
            ).fetchall()

        else:
            rows = db.execute(
                "SELECT * FROM products ORDER BY product_id"
            ).fetchall()

    return [dict(row) for row in rows]

def get_order(order_id):
    with connection() as db:
        row = db.execute(
            """
            SELECT
                o.*,
                p.name AS product_name,
                p.category
            FROM orders o
            JOIN products p
              ON p.product_id = o.product_id
            WHERE o.order_id = ?
            """,
            (order_id,),
        ).fetchone()

    return dict(row) if row else None
def sales_summary(start_date, end_date):
    with connection() as db:
        row = db.execute(
            """
            SELECT
                COUNT(*) AS order_count,
                COALESCE(SUM(quantity), 0) AS units_sold,
                COALESCE(SUM(total_amount), 0) AS revenue
            FROM orders
            WHERE order_date BETWEEN ? AND ?
              AND status = 'CONFIRMED'
            """,
            (start_date, end_date),
        ).fetchone()

    return {
        "start_date": start_date,
        "end_date": end_date,
        "order_count": row["order_count"],
        "units_sold": row["units_sold"],
        "revenue": row["revenue"],
    }

def create_order(
    customer_name: str,
    product_id: int,
    quantity: int,
):
    """
    Create a sales order and reduce product stock.
    """

    # ---------------------------------------------
    # Validate input
    # ---------------------------------------------

    if not customer_name.strip():
        raise ValueError(
            "Customer name cannot be empty"
        )

    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero"
        )

    # ---------------------------------------------
    # Check product and stock
    # ---------------------------------------------

    with connection() as db:

        product = db.execute(
            """
            SELECT
                product_id,
                name,
                category,
                unit_price,
                stock
            FROM products
            WHERE product_id = ?
            """,
            (product_id,),
        ).fetchone()

        if product is None:
            raise ValueError(
                f"Product {product_id} does not exist"
            )

        if product["stock"] < quantity:
            raise ValueError(
                f"Insufficient stock. "
                f"Requested: {quantity}, "
                f"Available: {product['stock']}"
            )

        # -----------------------------------------
        # Calculate order amount
        # -----------------------------------------

        unit_price = product["unit_price"]

        total_amount = round(
            unit_price * quantity,
            2,
        )

        order_date = date.today().isoformat()

        # -----------------------------------------
        # Insert order
        # -----------------------------------------

        cursor = db.execute(
            """
            INSERT INTO orders
            (
                customer_name,
                product_id,
                quantity,
                unit_price,
                total_amount,
                order_date,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_name.strip(),
                product_id,
                quantity,
                unit_price,
                total_amount,
                order_date,
                "CONFIRMED",
            ),
        )

        order_id = cursor.lastrowid

        # -----------------------------------------
        # Reduce stock
        # -----------------------------------------

        db.execute(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE product_id = ?
            """,
            (
                quantity,
                product_id,
            ),
        )

    # Transaction is committed when the
    # connection context manager completes.

    return get_order(order_id)