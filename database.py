import sqlite3
import os
from datetime import datetime

import tempfile

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_LOCAL_DB  = os.path.join(_BASE_DIR, "rr_enterprise.db")
DB_PATH = _LOCAL_DB if os.access(_BASE_DIR, os.W_OK) else os.path.join(tempfile.gettempdir(), "rr_enterprise.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            category  TEXT    NOT NULL,
            price     REAL    NOT NULL,
            quantity  INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS sales (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id  INTEGER NOT NULL,
            product     TEXT    NOT NULL,
            quantity    INTEGER NOT NULL,
            unit_price  REAL    NOT NULL,
            subtotal    REAL    NOT NULL,
            gst         REAL    NOT NULL,
            total       REAL    NOT NULL,
            customer    TEXT    DEFAULT 'Walk-in Customer',
            date        TEXT    NOT NULL
        );
    """)
    conn.commit()

    # Seed default products if table is empty
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        _seed_products(cur)
        conn.commit()

    conn.close()


def _seed_products(cur):
    defaults = [
        # ── Distemper ─────────────────────────────────────────────────────────
        ("Uno Distemper 20 KG",                     "Distemper",      919,   30),
        ("Uno Distemper 10 KG",                     "Distemper",      495,   40),
        ("Uno Distemper 5 KG",                      "Distemper",      269,   50),
        ("Uno Distemper 2 KG",                      "Distemper",      112.5, 60),

        # ── Wall Putty ────────────────────────────────────────────────────────
        ("Asian Wall Putty 40 KG",                  "Wall Putty",     874,   20),
        ("Asian Wall Putty 30 KG",                  "Wall Putty",     655,   25),
        ("Asian Wall Putty 20 KG",                  "Wall Putty",     536,   30),
        ("Asian Wall Putty 5 KG",                   "Wall Putty",     143.5, 50),
        ("Asian Wall Putty 1 KG",                   "Wall Putty",      31,   80),

        # ── Neo Bharat Interior ───────────────────────────────────────────────
        ("Neo Bharat Interior 20 KG",               "Interior Paint", 900,   20),
        ("Neo Bharat Interior 10 KG",               "Interior Paint", 485,   25),
        ("Neo Bharat Interior 5 KG",                "Interior Paint", 264,   35),
        ("Neo Bharat Interior 2 KG",                "Interior Paint", 110,   50),

        # ── Neo Bharat Exterior ───────────────────────────────────────────────
        ("Neo Bharat Exterior 20 KG",               "Exterior Paint", 1200,  20),
        ("Neo Bharat Exterior 10 KG",               "Exterior Paint",  625,  25),
        ("Neo Bharat Exterior 5 KG",                "Exterior Paint",  325,  35),
        ("Neo Bharat Exterior 2 KG",                "Exterior Paint",  140,  50),

        # ── Tractor Sparc ─────────────────────────────────────────────────────
        ("Tractor Sparc Super White 20 LTR",        "Interior Paint", 1795,  15),
        ("Tractor Sparc Super White 10 LTR",        "Interior Paint",  935,  20),
        ("Tractor Sparc Super White 4 LTR",         "Interior Paint",  399,  30),
        ("Tractor Sparc Super White 1 LTR",         "Interior Paint",  106,  60),

        # ── Tractor Emulsion ──────────────────────────────────────────────────
        ("Tractor Emulsion TE3 20 LTR",             "Interior Paint", 2517,  15),
        ("Tractor Emulsion TE3 10 LTR",             "Interior Paint", 1309,  20),
        ("Tractor Emulsion TE3 4 LTR",              "Interior Paint",  556,  30),
        ("Tractor Emulsion TE3 1 LTR",              "Interior Paint",  147,  60),
        ("Tractor Emulsion TE13 1 LTR",             "Interior Paint",  176,  40),
        ("Tractor Emulsion TE15 1 LTR",             "Interior Paint",  180,  40),
        ("Tractor Emulsion TE22N 1 LTR",            "Interior Paint",  138,  40),

        # ── Tractor Shyne ─────────────────────────────────────────────────────
        ("Tractor Shyne SH1 20 LTR",                "Interior Paint", 3151,  10),
        ("Tractor Shyne SH1 10 LTR",                "Interior Paint", 1643,  15),
        ("Tractor Shyne SH1 4 LTR",                 "Interior Paint",  694,  25),
        ("Tractor Shyne SH1 1 LTR",                 "Interior Paint",  181,  50),
        ("Tractor Shyne SH13 1 LTR",                "Interior Paint",  208,  40),
        ("Tractor Shyne SH15 1 LTR",                "Interior Paint",  208,  40),

        # ── Premium Emulsion ──────────────────────────────────────────────────
        ("Premium Emulsion BW1 20 LTR",             "Interior Paint", 5155,  10),
        ("Premium Emulsion BW1 10 LTR",             "Interior Paint", 2645,  15),
        ("Premium Emulsion BW1 4 LTR",              "Interior Paint", 1078,  20),
        ("Premium Emulsion BW1 1 LTR",              "Interior Paint",  277,  50),
        ("Premium Emulsion BW11N 20 LTR",           "Interior Paint", 4896,  10),
        ("Premium Emulsion BW11N 10 LTR",           "Interior Paint", 2496,  15),
        ("Premium Emulsion BW11N 4 LTR",            "Interior Paint", 1018,  20),
        ("Premium Emulsion BW11N 1 LTR",            "Interior Paint",  261,  50),

        # ── Premium Shyne ─────────────────────────────────────────────────────
        ("Premium Shyne Appur White 20 LTR",        "Interior Paint", 5667,  10),
        ("Premium Shyne Appur White 10 LTR",        "Interior Paint", 2931,  12),
        ("Premium Shyne Appur White 4 LTR",         "Interior Paint", 1220,  20),
        ("Premium Shyne Appur White 1 LTR",         "Interior Paint",  308,  40),
        ("Premium Shyne AS11 20 LTR",               "Interior Paint", 5645,  10),
        ("Premium Shyne AS11 10 LTR",               "Interior Paint", 2922,  12),
        ("Premium Shyne AS11 4 LTR",                "Interior Paint", 1193,  20),
        ("Premium Shyne AS11 1 LTR",                "Interior Paint",  307,  40),

        # ── Royal ─────────────────────────────────────────────────────────────
        ("Royal RB1N 20 LTR",                       "Premium Paint",  9390,   8),
        ("Royal RB1N 10 LTR",                       "Premium Paint",  4740,  10),
        ("Royal RB1N 4 LTR",                        "Premium Paint",  1902,  15),
        ("Royal RB1N 1 LTR",                        "Premium Paint",   484,  30),
        ("Royal RB1N 200 ML",                       "Premium Paint",   104,  50),
        ("Royal RB10 20 LTR",                       "Premium Paint",  9233,   8),
        ("Royal RB10 10 LTR",                       "Premium Paint",  4661,  10),
        ("Royal RB10 4 LTR",                        "Premium Paint",  1881,  15),
        ("Royal RB10 1 LTR",                        "Premium Paint",   477,  30),
        ("Royal Neo Silver 1 LTR",                  "Premium Paint",   649,  20),
        ("Royal Neo Gold 1 LTR",                    "Premium Paint",   671,  20),

        # ── Royal Shyne ───────────────────────────────────────────────────────
        ("Royal Shyne SN3 20 LTR",                  "Premium Paint", 10147,   6),
        ("Royal Shyne SN3 10 LTR",                  "Premium Paint",  5119,   8),
        ("Royal Shyne SN3 4 LTR",                   "Premium Paint",  2060,  12),
        ("Royal Shyne SN3 1 LTR",                   "Premium Paint",   522,  25),
        ("Royal Shyne SN10 20 LTR",                 "Premium Paint",  9810,   6),
        ("Royal Shyne SN10 10 LTR",                 "Premium Paint",  4940,   8),
        ("Royal Shyne SN10 4 LTR",                  "Premium Paint",  1990,  12),
        ("Royal Shyne SN10 1 LTR",                  "Premium Paint",   504,  25),

        # ── Play ──────────────────────────────────────────────────────────────
        ("Play PG5 1 LTR",                          "Texture Paint",   658,  15),
        ("Play PG5 200 ML",                         "Texture Paint",   134,  25),
        ("Play PM1 / Gold / Copper 1 LTR",          "Texture Paint",  1002,  15),
        ("Play PM1 / Gold / Copper 200 ML",         "Texture Paint",   219,  25),

        # ── Floor Guard ───────────────────────────────────────────────────────
        ("Floor Guard FG1A 20 LTR",                 "Floor Paint",    6360,   5),
        ("Floor Guard FG1A 4 LTR",                  "Floor Paint",    1296,  10),
        ("Floor Guard FG1A 1 LTR",                  "Floor Paint",     330,  20),
        ("Floor Guard FG2A 4 LTR",                  "Floor Paint",    1368,  10),
        ("Floor Guard FG2A 1 LTR",                  "Floor Paint",     350,  20),
        ("Floor Guard Yellow 1 LTR",                "Floor Paint",     360,  15),
        ("Floor Guard Black 1 LTR",                 "Floor Paint",     360,  15),
        ("Floor Guard Terracotta 1 LTR",            "Floor Paint",     360,  15),
        ("Floor Guard White 1 LTR",                 "Floor Paint",     360,  15),

        # ── Tile Guard ────────────────────────────────────────────────────────
        ("Tile Guard TG1A 20 LTR",                  "Floor Paint",    4630,   5),
        ("Tile Guard TG1A 10 LTR",                  "Floor Paint",    2320,   8),
        ("Tile Guard TG1A 4 LTR",                   "Floor Paint",     951,  12),
        ("Tile Guard TG1A 1 LTR",                   "Floor Paint",     239,  25),

        # ── Ace Sparc ─────────────────────────────────────────────────────────
        ("Ace Sparc Super White 20 LTR",            "Exterior Paint", 2160,  15),
        ("Ace Sparc Super White 10 LTR",            "Exterior Paint", 1200,  20),
        ("Ace Sparc Super White 4 LTR",             "Exterior Paint",  510,  30),
        ("Ace Sparc Super White 1 LTR",             "Exterior Paint",  134,  60),

        # ── Ace Emulsion ──────────────────────────────────────────────────────
        ("Ace Emulsion AC2G 20 LTR",                "Exterior Paint", 3009,  10),
        ("Ace Emulsion AC2G 10 LTR",                "Exterior Paint", 1581,  15),
        ("Ace Emulsion AC2G 4 LTR",                 "Exterior Paint",  658,  25),
        ("Ace Emulsion AC2G 1 LTR",                 "Exterior Paint",  172,  50),
        ("Ace Emulsion AC9G 20 LTR",                "Exterior Paint", 2994,  10),
        ("Ace Emulsion AC9G 10 LTR",                "Exterior Paint", 1541,  15),
        ("Ace Emulsion AC9G 4 LTR",                 "Exterior Paint",  640,  25),
        ("Ace Emulsion AC9G 1 LTR",                 "Exterior Paint",  166,  50),
        ("Ace Emulsion AC21G 20 LTR",               "Exterior Paint", 2830,  10),
        ("Ace Emulsion AC21G 10 LTR",               "Exterior Paint", 1454,  15),
        ("Ace Emulsion AC21G 4 LTR",                "Exterior Paint",  604,  25),
        ("Ace Emulsion AC21G 1 LTR",                "Exterior Paint",  157,  50),

        # ── Ace Shyne ─────────────────────────────────────────────────────────
        ("Ace Shyne AH2 20 LTR",                    "Exterior Paint", 3329,  10),
        ("Ace Shyne AH2 10 LTR",                    "Exterior Paint", 1741,  12),
        ("Ace Shyne AH2 4 LTR",                     "Exterior Paint",  722,  20),
        ("Ace Shyne AH2 1 LTR",                     "Exterior Paint",  188,  40),
        ("Ace Shyne AH10 20 LTR",                   "Exterior Paint", 3189,  10),
        ("Ace Shyne AH10 10 LTR",                   "Exterior Paint", 1671,  12),
        ("Ace Shyne AH10 4 LTR",                    "Exterior Paint",  694,  20),
        ("Ace Shyne AH10 1 LTR",                    "Exterior Paint",  181,  40),

        # ── Apex Exterior ─────────────────────────────────────────────────────
        ("Apex AB2 20 LTR",                         "Exterior Paint", 5010,   8),
        ("Apex AB2 10 LTR",                         "Exterior Paint", 2597,  10),
        ("Apex AB2 4 LTR",                          "Exterior Paint", 1078,  15),
        ("Apex AB2 1 LTR",                          "Exterior Paint",  279,  35),
        ("Apex AB11 20 LTR",                        "Exterior Paint", 5060,   8),
        ("Apex AB11 10 LTR",                        "Exterior Paint", 2597,  10),
        ("Apex AB11 4 LTR",                         "Exterior Paint", 1078,  15),
        ("Apex AB11 1 LTR",                         "Exterior Paint",  279,  35),
        ("Apex AB17C 20 LTR",                       "Exterior Paint", 5261,   6),
        ("Apex AB17C 10 LTR",                       "Exterior Paint", 2676,   8),
        ("Apex AB17C 4 LTR",                        "Exterior Paint", 1099,  12),
        ("Apex AB17C 1 LTR",                        "Exterior Paint",  284,  30),
        ("Apex AB18C 20 LTR",                       "Exterior Paint", 5949,   5),
        ("Apex AB18C 10 LTR",                       "Exterior Paint", 3051,   8),
        ("Apex AB18C 4 LTR",                        "Exterior Paint", 1248,  12),
        ("Apex AB18C 1 LTR",                        "Exterior Paint",  321,  25),

        # ── Apex Shyne ────────────────────────────────────────────────────────
        ("Apex Shyne AY2 20 LTR",                   "Exterior Paint", 5030,   6),
        ("Apex Shyne AY2 10 LTR",                   "Exterior Paint", 2607,   8),
        ("Apex Shyne AY2 4 LTR",                    "Exterior Paint", 1082,  12),
        ("Apex Shyne AY2 1 LTR",                    "Exterior Paint",  280,  30),
        ("Apex Shyne AY17 20 LTR",                  "Exterior Paint", 5281,   6),
        ("Apex Shyne AY17 10 LTR",                  "Exterior Paint", 2686,   8),
        ("Apex Shyne AY17 4 LTR",                   "Exterior Paint", 1103,  12),
        ("Apex Shyne AY17 1 LTR",                   "Exterior Paint",  285,  30),

        # ── Ultima ────────────────────────────────────────────────────────────
        ("Ultima HQ2N 20 LTR",                      "Premium Paint",  7849,   5),
        ("Ultima HQ2N 10 LTR",                      "Premium Paint",  4020,   8),
        ("Ultima HQ2N 4 LTR",                       "Premium Paint",  1642,  10),
        ("Ultima HQ2N 1 LTR",                       "Premium Paint",   417,  25),
        ("Ultima HQ2N 200 ML",                      "Premium Paint",    94,  40),
        ("Ultima HQ16 20 LTR",                      "Premium Paint", 10395,   3),
        ("Ultima HQ16 10 LTR",                      "Premium Paint",  5328,   5),
        ("Ultima HQ16 4 LTR",                       "Premium Paint",  2180,   8),
        ("Ultima HQ16 1 LTR",                       "Premium Paint",   561,  20),

        # ── Gloss Enamel ──────────────────────────────────────────────────────
        ("Gloss Enamel EB1 20 LTR",                 "Enamel Paint",   4203,   8),
        ("Gloss Enamel EB1 10 LTR",                 "Enamel Paint",   2145,  10),
        ("Gloss Enamel EB1 4 LTR",                  "Enamel Paint",    885,  20),
        ("Gloss Enamel EB1 1 LTR",                  "Enamel Paint",    228,  40),
        ("Gloss Enamel EB1 500 ML",                 "Enamel Paint",    118,  50),
        ("Gloss Enamel EB10 20 LTR",                "Enamel Paint",   3973,   8),
        ("Gloss Enamel EB10 10 LTR",                "Enamel Paint",   2027,  10),
        ("Gloss Enamel EB10 4 LTR",                 "Enamel Paint",    838,  20),
        ("Gloss Enamel EB10 1 LTR",                 "Enamel Paint",    216,  40),
        ("Gloss Enamel EB10 500 ML",                "Enamel Paint",    112,  50),

        # ── Satin Enamel ──────────────────────────────────────────────────────
        ("Satin Enamel SE2 20 LTR",                 "Enamel Paint",   5081,   6),
        ("Satin Enamel SE2 10 LTR",                 "Enamel Paint",   2617,   8),
        ("Satin Enamel SE2 4 LTR",                  "Enamel Paint",   1063,  15),
        ("Satin Enamel SE2 1 LTR",                  "Enamel Paint",    274,  35),
        ("Satin Enamel SE10 4 LTR",                 "Enamel Paint",   1037,  15),
        ("Satin Enamel SE10 1 LTR",                 "Enamel Paint",    268,  35),

        # ── Primers ───────────────────────────────────────────────────────────
        ("Red Oxide Primer 20 LTR",                 "Primer",         3299,  10),
        ("Red Oxide Primer 10 LTR",                 "Primer",         1700,  12),
        ("Red Oxide Primer 4 LTR",                  "Primer",          701,  20),
        ("Red Oxide Primer 1 LTR",                  "Primer",          183,  40),
        ("Red Oxide Primer 500 ML",                 "Primer",           95.5, 50),
        ("Yellow Primer 20 LTR",                    "Primer",         3833,   8),
        ("Yellow Primer 4 LTR",                     "Primer",          815,  15),
        ("Yellow Primer 1 LTR",                     "Primer",          210,  35),
        ("Yellow Primer 500 ML",                    "Primer",          111.5, 40),
        ("Wood Primer 20 LTR",                      "Primer",         3586,   8),
        ("Wood Primer 10 LTR",                      "Primer",         1842,  10),
        ("Wood Primer 4 LTR",                       "Primer",          755,  15),
        ("Wood Primer 1 LTR",                       "Primer",          196,  35),
        ("Wood Primer 500 ML",                      "Primer",          102,  40),
        ("Trucare Interior Primer 20 LTR",          "Primer",         2454,  10),
        ("Trucare Interior Primer 10 LTR",          "Primer",         1286,  12),
        ("Trucare Interior Primer 4 LTR",           "Primer",          542,  20),
        ("Trucare Interior Primer 1 LTR",           "Primer",          145,  40),
        ("Trucare Exterior Primer 20 LTR",          "Primer",         2871,  10),
        ("Trucare Exterior Primer 10 LTR",          "Primer",         1475,  12),
        ("Trucare Exterior Primer 4 LTR",           "Primer",          614,  20),
        ("Trucare Exterior Primer 1 LTR",           "Primer",          159,  35),
        ("Royal Base Coat 20 LTR",                  "Primer",         3541,   6),
        ("Royal Base Coat 10 LTR",                  "Primer",         1881,   8),
        ("Royal Base Coat 4 LTR",                   "Primer",          797,  12),
        ("Royal Base Coat 1 LTR",                   "Primer",          213,  30),
        ("SPARC Interior Primer 10 LTR",            "Primer",          721,  15),
        ("SPARC Interior Primer 4 LTR",             "Primer",          319,  25),
        ("SPARC Interior Primer 1 LTR",             "Primer",           89,  50),

        # ── Damp Proof / Waterproofing ────────────────────────────────────────
        ("Damp Sheath Interior 20 LTR",             "Waterproofing",  2760,   8),
        ("Damp Sheath Interior 10 LTR",             "Waterproofing",  1505,  10),
        ("Damp Sheath Interior 4 LTR",              "Waterproofing",   642,  15),
        ("Damp Sheath Interior 1 LTR",              "Waterproofing",   181,  30),
        ("Damp Sheath Exterior 20 LTR",             "Waterproofing",  3218,   8),
        ("Damp Sheath Exterior 10 LTR",             "Waterproofing",  1660,  10),
        ("Damp Sheath Exterior 4 LTR",              "Waterproofing",   718,  15),
        ("Damp Sheath Exterior 1 LTR",              "Waterproofing",   201,  30),
        ("Smartcare Damp Proof 20 LTR",             "Waterproofing",  4790,   5),
        ("Smartcare Damp Proof 10 LTR",             "Waterproofing",  2440,   8),
        ("Smartcare Damp Proof 4 LTR",              "Waterproofing",  1010,  10),
        ("Smartcare Damp Proof 1 LTR",              "Waterproofing",   266,  20),
        ("Hydroloc 1 LTR",                          "Waterproofing",   383,  20),
        ("Hydroloc 900 ML",                         "Waterproofing",   383,  20),
        ("Crackseal 5 KG",                          "Waterproofing",  1361,  10),
        ("Crackseal 900 ML",                        "Waterproofing",   258,  20),
        ("Crackseal 360 GM",                        "Waterproofing",   119,  30),
        ("Damblock 15 KG",                          "Waterproofing",  1492,   8),
        ("Damblock 3 KG",                           "Waterproofing",   363,  15),

        # ── Pipes ─────────────────────────────────────────────────────────────
        ("CPVC Pipe 1 inch (per ft)",               "Pipes",            35, 200),
        ("PVC Pipe 2 inch (per ft)",                "Pipes",            28, 180),
        ("GI Pipe 1.5 inch (per ft)",               "Pipes",            85, 120),
        ("UPVC Column Pipe 4 inch (per ft)",        "Pipes",           115,  90),
        ("PVC Conduit Pipe 25mm (per mtr)",         "Pipes",            22, 150),

        # ── Electrical ────────────────────────────────────────────────────────
        ("Havells 2.5 sq mm Wire (per mtr)",        "Electrical",       38, 300),
        ("Finolex 1.5 sq mm Wire (per mtr)",        "Electrical",       24, 400),
        ("Anchor Roma 6A Switch",                   "Electrical",       45, 200),
        ("Legrand MCB 32A Single Pole",             "Electrical",      285,  80),
        ("Philips LED Bulb 9W",                     "Electrical",       95,  50),
        ("Distribution Board 8 Way",               "Electrical",      650,  30),
        ("Copper Earthing Wire (per mtr)",          "Electrical",       55, 100),
    ]
    cur.executemany(
        "INSERT INTO products (name, category, price, quantity) VALUES (?,?,?,?)",
        defaults
    )


# ── Product helpers ──────────────────────────────────────────────────────────

def get_all_products():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM products ORDER BY category, name"
        ).fetchall()]


def get_product_by_id(pid):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        return dict(row) if row else None


def add_product(name, category, price, quantity):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO products (name, category, price, quantity) VALUES (?,?,?,?)",
            (name, category, price, quantity)
        )
        conn.commit()


def update_stock(pid, qty):
    with get_conn() as conn:
        conn.execute("UPDATE products SET quantity=? WHERE id=?", (qty, pid))
        conn.commit()


def update_price(pid, price):
    with get_conn() as conn:
        conn.execute("UPDATE products SET price=? WHERE id=?", (price, pid))
        conn.commit()


def delete_product(pid):
    with get_conn() as conn:
        conn.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()


def search_products(query):
    q = f"%{query}%"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM products WHERE name LIKE ? OR category LIKE ? ORDER BY category, name",
            (q, q)
        ).fetchall()]


# ── Sales helpers ────────────────────────────────────────────────────────────

def record_sale(product_id, product, quantity, unit_price, subtotal, gst, total, customer):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO sales
               (product_id, product, quantity, unit_price, subtotal, gst, total, customer, date)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (product_id, product, quantity, unit_price, subtotal, gst, total, customer, date)
        )
        conn.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id = ?",
            (quantity, product_id)
        )
        conn.commit()


def get_sales(date_filter=None):
    """Return sales; optionally filter by 'YYYY-MM-DD' or 'YYYY-MM'."""
    with get_conn() as conn:
        if date_filter:
            rows = conn.execute(
                "SELECT * FROM sales WHERE date LIKE ? ORDER BY date DESC",
                (f"{date_filter}%",)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM sales ORDER BY date DESC"
            ).fetchall()
        return [dict(r) for r in rows]


def get_daily_summary():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT substr(date,1,10) AS day,
                   COUNT(*)          AS transactions,
                   SUM(total)        AS revenue
            FROM sales
            GROUP BY day
            ORDER BY day DESC
            LIMIT 30
        """).fetchall()
        return [dict(r) for r in rows]


def get_monthly_summary():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT substr(date,1,7) AS month,
                   COUNT(*)         AS transactions,
                   SUM(total)       AS revenue
            FROM sales
            GROUP BY month
            ORDER BY month DESC
        """).fetchall()
        return [dict(r) for r in rows]


def get_category_summary():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT p.category,
                   COUNT(s.id)  AS transactions,
                   SUM(s.total) AS revenue
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.category
            ORDER BY revenue DESC
        """).fetchall()
        return [dict(r) for r in rows]
