from datetime import datetime, timedelta
from decimal import Decimal
import os
import random

import psycopg
from faker import Faker

from config.env_variable import settings

# ============================================================
# Configuration
# ============================================================


# Reproducible random data
random.seed(42)
fake = Faker()
Faker.seed(42)


# ============================================================
# Sample business data
# ============================================================

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Books",
    "Sports & Fitness",
    "Beauty",
    "Toys",
    "Grocery",
    "Furniture",
    "Accessories",
]

COUNTRIES = [
    "India",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
    "France",
    "Singapore",
    "United Arab Emirates",
    "Japan",
]

PAYMENT_METHODS = [
    "credit_card",
    "debit_card",
    "upi",
    "paypal",
    "bank_transfer",
]

ORDER_STATUSES = [
    "completed",
    "completed",
    "completed",
    "completed",
    "pending",
    "cancelled",
    "refunded",
]

PAYMENT_STATUSES = [
    "successful",
    "successful",
    "successful",
    "successful",
    "pending",
    "failed",
    "refunded",
]


# ============================================================
# Helper functions
# ============================================================

def random_date(start_date: datetime, end_date: datetime) -> datetime:
    """Return a random datetime between two dates."""

    delta = end_date - start_date

    random_seconds = random.randint(
        0,
        int(delta.total_seconds())
    )

    return start_date + timedelta(seconds=random_seconds)


def money(value) -> Decimal:
    """Convert a value to Decimal with 2 decimal places."""

    return Decimal(str(value)).quantize(Decimal("0.01"))


# ============================================================
# Main seed function
# ============================================================

def seed_database():
    print("[INFO] Connecting to PostgreSQL...")

    with psycopg.connect(settings.DATABASE_URL) as conn:

        with conn.cursor() as cur:

            # ------------------------------------------------
            # Clean existing data
            # ------------------------------------------------

            print("[INFO] Clearing existing data...")

            cur.execute(
                """
                TRUNCATE TABLE
                    payments,
                    order_items,
                    orders,
                    products,
                    customers,
                    categories
                RESTART IDENTITY CASCADE;
                """
            )

            # ------------------------------------------------
            # Categories
            # ------------------------------------------------

            print("[INFO] Creating categories...")

            category_ids = []

            for category_name in CATEGORIES:

                cur.execute(
                    """
                    INSERT INTO categories (category_name)
                    VALUES (%s)
                    RETURNING category_id;
                    """,
                    (category_name,),
                )

                category_id = cur.fetchone()[0]

                category_ids.append(category_id)

            print(f"[INFO] Created {len(category_ids)} categories")

            # ------------------------------------------------
            # Products
            # ------------------------------------------------

            print("[INFO] Creating products...")

            product_ids = []

            product_names = {
                "Electronics": [
                    "Wireless Headphones",
                    "Bluetooth Speaker",
                    "Smartphone",
                    "Laptop",
                    "Smart Watch",
                    "Wireless Mouse",
                    "Mechanical Keyboard",
                    "USB-C Hub",
                    "Power Bank",
                    "Webcam",
                ],
                "Clothing": [
                    "Cotton T-Shirt",
                    "Denim Jeans",
                    "Hoodie",
                    "Running Jacket",
                    "Formal Shirt",
                    "Chinos",
                    "Sneakers",
                    "Casual Shorts",
                    "Winter Jacket",
                    "Polo Shirt",
                ],
                "Home & Kitchen": [
                    "Coffee Maker",
                    "Air Fryer",
                    "Blender",
                    "Dinner Set",
                    "Electric Kettle",
                    "Toaster",
                    "Water Bottle",
                    "Knife Set",
                    "Storage Box",
                    "Cookware Set",
                ],
                "Books": [
                    "Python Programming",
                    "Data Science Handbook",
                    "Machine Learning Guide",
                    "Clean Code",
                    "SQL Mastery",
                    "Deep Learning",
                    "Algorithms Explained",
                    "System Design",
                    "AI Engineering",
                    "Database Design",
                ],
                "Sports & Fitness": [
                    "Yoga Mat",
                    "Dumbbell Set",
                    "Resistance Bands",
                    "Running Shoes",
                    "Fitness Tracker",
                    "Gym Bag",
                    "Skipping Rope",
                    "Tennis Racket",
                    "Football",
                    "Cycling Helmet",
                ],
                "Beauty": [
                    "Face Wash",
                    "Moisturizer",
                    "Sunscreen",
                    "Shampoo",
                    "Conditioner",
                    "Perfume",
                    "Lip Balm",
                    "Body Lotion",
                    "Hair Serum",
                    "Face Mask",
                ],
                "Toys": [
                    "Building Blocks",
                    "Remote Control Car",
                    "Puzzle Set",
                    "Board Game",
                    "Action Figure",
                    "Toy Train",
                    "Educational Kit",
                    "Doll House",
                    "Stuffed Animal",
                    "Science Kit",
                ],
                "Grocery": [
                    "Organic Coffee",
                    "Green Tea",
                    "Olive Oil",
                    "Protein Bars",
                    "Dark Chocolate",
                    "Almonds",
                    "Peanut Butter",
                    "Pasta",
                    "Honey",
                    "Breakfast Cereal",
                ],
                "Furniture": [
                    "Office Chair",
                    "Study Desk",
                    "Bookshelf",
                    "Bedside Table",
                    "Dining Chair",
                    "Coffee Table",
                    "Floor Lamp",
                    "Storage Cabinet",
                    "Sofa",
                    "TV Stand",
                ],
                "Accessories": [
                    "Leather Wallet",
                    "Backpack",
                    "Sunglasses",
                    "Travel Bag",
                    "Belt",
                    "Watch Strap",
                    "Key Holder",
                    "Phone Case",
                    "Laptop Sleeve",
                    "Card Holder",
                ],
            }

            # Create exactly 100 products:
            # 10 categories × 10 products
            for category_id, category_name in zip(
                category_ids,
                CATEGORIES,
            ):

                names = product_names[category_name]

                for product_name in names:

                    # Give some products a higher price
                    if category_name == "Electronics":
                        price = random.uniform(30, 1500)

                    elif category_name == "Furniture":
                        price = random.uniform(50, 1200)

                    else:
                        price = random.uniform(5, 300)

                    price = money(price)

                    # Cost is 45%–75% of selling price
                    cost = money(
                        price * Decimal(
                            str(random.uniform(0.45, 0.75))
                        )
                    )

                    stock_quantity = random.randint(0, 200)

                    created_at = random_date(
                        datetime.now() - timedelta(days=900),
                        datetime.now(),
                    )

                    sku = (
                        f"{category_name[:3].upper()}-"
                        f"{random.randint(10000, 99999)}"
                    )

                    cur.execute(
                        """
                        INSERT INTO products (
                            category_id,
                            product_name,
                            sku,
                            price,
                            cost,
                            stock_quantity,
                            created_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING product_id;
                        """,
                        (
                            category_id,
                            product_name,
                            sku,
                            price,
                            cost,
                            stock_quantity,
                            created_at,
                        ),
                    )

                    product_ids.append(cur.fetchone()[0])

            print(f"[INFO] Created {len(product_ids)} products")

            # ------------------------------------------------
            # Customers
            # ------------------------------------------------

            print("[INFO] Creating customers...")

            customer_ids = []

            # Keep some customers with old signup dates.
            # This helps create inactive customers.
            start_signup = datetime.now() - timedelta(days=1000)

            for _ in range(500):

                first_name = fake.first_name()
                last_name = fake.last_name()

                email = (
                    f"{first_name.lower()}."
                    f"{last_name.lower()}."
                    f"{random.randint(1000, 99999)}"
                    "@example.com"
                )

                country = random.choice(COUNTRIES)
                city = fake.city()

                signup_date = random_date(
                    start_signup,
                    datetime.now(),
                ).date()

                cur.execute(
                    """
                    INSERT INTO customers (
                        first_name,
                        last_name,
                        email,
                        country,
                        city,
                        signup_date
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING customer_id;
                    """,
                    (
                        first_name,
                        last_name,
                        email,
                        country,
                        city,
                        signup_date,
                    ),
                )

                customer_ids.append(cur.fetchone()[0])

            print(f"[INFO] Created {len(customer_ids)} customers")

            # ------------------------------------------------
            # Orders + Order Items + Payments
            # ------------------------------------------------

            print("[INFO] Creating orders...")

            order_count = 2000
            order_ids = []

            # Orders spread across the last 18 months
            order_start = datetime.now() - timedelta(days=540)
            order_end = datetime.now()

            for order_number in range(order_count):

                # Make some customers much more active than others.
                #
                # This gives the database interesting patterns for
                # questions such as:
                #
                # "Who is our best customer?"
                # "Who placed the most orders?"
                #
                if random.random() < 0.70:
                    customer_id = random.choice(customer_ids[:300])
                else:
                    customer_id = random.choice(customer_ids)

                order_date = random_date(
                    order_start,
                    order_end,
                )

                status = random.choice(ORDER_STATUSES)

                shipping_country = random.choice(COUNTRIES)

                # We'll calculate total_amount from order_items.
                total_amount = Decimal("0.00")

                cur.execute(
                    """
                    INSERT INTO orders (
                        customer_id,
                        order_date,
                        status,
                        shipping_country,
                        total_amount
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING order_id;
                    """,
                    (
                        customer_id,
                        order_date,
                        status,
                        shipping_country,
                        total_amount,
                    ),
                )

                order_id = cur.fetchone()[0]

                order_ids.append(order_id)

                # ------------------------------------------------
                # Order items
                # ------------------------------------------------

                # 1–5 items per order.
                # 2000 orders × average ~3 items = 6000+ items.
                item_count = random.randint(1, 5)

                selected_products = random.sample(
                    product_ids,
                    item_count,
                )

                for product_id in selected_products:

                    # Get current product price
                    cur.execute(
                        """
                        SELECT price
                        FROM products
                        WHERE product_id = %s;
                        """,
                        (product_id,),
                    )

                    product_price = cur.fetchone()[0]

                    quantity = random.randint(1, 5)

                    # Most products have no discount,
                    # some have realistic discounts.
                    if random.random() < 0.65:
                        discount = Decimal("0.00")
                    else:
                        discount = Decimal(
                            str(
                                random.choice(
                                    [5, 10, 15, 20, 25]
                                )
                            )
                        )

                    item_total = (
                        product_price
                        * quantity
                        * (Decimal("1.00") - discount / Decimal("100"))
                    )

                    total_amount += item_total

                    cur.execute(
                        """
                        INSERT INTO order_items (
                            order_id,
                            product_id,
                            quantity,
                            unit_price,
                            discount
                        )
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (
                            order_id,
                            product_id,
                            quantity,
                            product_price,
                            discount,
                        ),
                    )

                total_amount = money(total_amount)

                # Cancelled orders can still have a calculated
                # original order amount.
                cur.execute(
                    """
                    UPDATE orders
                    SET total_amount = %s
                    WHERE order_id = %s;
                    """,
                    (
                        total_amount,
                        order_id,
                    ),
                )

                # ------------------------------------------------
                # Payment
                # ------------------------------------------------

                payment_status = random.choice(
                    PAYMENT_STATUSES
                )

                payment_method = random.choice(
                    PAYMENT_METHODS
                )

                payment_date = order_date + timedelta(
                    minutes=random.randint(1, 1440)
                )

                # Don't allow payment after "now"
                if payment_date > datetime.now():
                    payment_date = datetime.now()

                cur.execute(
                    """
                    INSERT INTO payments (
                        order_id,
                        payment_date,
                        payment_method,
                        amount,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        order_id,
                        payment_date,
                        payment_method,
                        total_amount,
                        payment_status,
                    ),
                )

                # Print progress every 250 orders
                if (order_number + 1) % 250 == 0:
                    print(
                        f"[INFO] Created "
                        f"{order_number + 1}/{order_count} orders"
                    )

            print(f"[INFO] Created {len(order_ids)} orders")

        # Commit everything
        conn.commit()

    print()
    print("=" * 60)
    print("DATABASE SEED COMPLETE")
    print("=" * 60)


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":

    try:
        seed_database()

    except Exception as e:
        print()
        print("[ERROR] Database seeding failed:")
        print(e)
        raise