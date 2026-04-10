import csv

from database import get_conn, init_db

def import_products_from_csv(file_path):
    conn = get_conn()
    cur = conn.cursor()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            name = row['name']
            category = row['category']
            price = float(row['price'])
            quantity = int(row['quantity'])

            existing = cur.execute(
                "SELECT id FROM products WHERE name=?", (name,)
            ).fetchone()

            if existing:
                cur.execute(
                    "UPDATE products SET price=?, quantity=? WHERE name=?",
                    (price, quantity, name)
                )
            else:
                cur.execute(
                    "INSERT INTO products (name, category, price, quantity) VALUES (?,?,?,?)",
                    (name, category, price, quantity)
                )

    conn.commit()
    conn.close()
    print("✅ CSV Imported Successfully!")
if __name__ == "__main__":
    print("Starting import...")

    init_db()  # create database

    import_products_from_csv("products.csv")  # import data

    print("Done!")