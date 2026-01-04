"""
Flexi Mart - Project 1 (PostgreSQL)

Schema reference:
- customer_id/product_id/order_id/order_item_id are GENERATED ALWAYS AS IDENTITY
- DO NOT insert these IDs from CSV
- CSV has source keys like C001 / P001 → map them to DB IDs after insert

Deliverables:
- etl_pipeline.py (this file)
- data_quality_report.txt
- etl.log
"""

import os
import re
import sys
import logging
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


# ---------------------------- Metrics ----------------------------

@dataclass
class DQMetrics:
    file_name: str
    records_read: int = 0
    duplicates_removed: int = 0
    missing_values_handled: int = 0
    records_loaded_successfully: int = 0


# ---------------------------- Logging ----------------------------

def setup_logger(log_path: str) -> logging.Logger:
    logger = logging.getLogger("fleximart_etl")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


# ---------------------------- Helpers ----------------------------

NULL_LIKE = {"", "nan", "NaN", "none", "None", "null", "NULL"}

def normalize_null(x):
    if x is None:
        return None
    s = str(x).strip()
    if s in NULL_LIKE:
        return None
    return s

def safe_read_csv(path: str, logger: logging.Logger) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    logger.info(f"Reading CSV: {path}")
    # Read everything as string to avoid phone becoming float/scientific notation
    return pd.read_csv(path, dtype=str)

def standardize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Standardize phone formats to +91-XXXXXXXXXX when possible.
    Handles floats, negatives, spaces, etc.
    """
    phone = normalize_null(phone)
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return f"+91-{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+91-{digits[2:]}"
    return phone

def standardize_category(cat: Optional[str]) -> str:
    cat = normalize_null(cat)
    if not cat:
        return "Unknown"
    return cat.lower().title()

def parse_date_to_yyyy_mm_dd(value: Optional[str]) -> Optional[str]:
    """
    Convert date to YYYY-MM-DD.
    Handles both mm/dd/yyyy and dd/mm/yyyy by heuristic + fallback.
    """
    value = normalize_null(value)
    if not value:
        return None

    s = value.strip()

    # If it's already ISO-ish
    dt = pd.to_datetime(s, errors="coerce")
    if not pd.isna(dt):
        return dt.strftime("%Y-%m-%d")

    # Heuristic for dd/mm/yyyy vs mm/dd/yyyy
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        # if second part > 12 => mm/dd/yyyy (month is first part)
        if b > 12:
            dt = pd.to_datetime(s, errors="coerce", dayfirst=False)
        # if first part > 12 => dd/mm/yyyy
        elif a > 12:
            dt = pd.to_datetime(s, errors="coerce", dayfirst=True)
        else:
            # ambiguous: try both
            dt1 = pd.to_datetime(s, errors="coerce", dayfirst=False)
            dt2 = pd.to_datetime(s, errors="coerce", dayfirst=True)
            dt = dt1 if not pd.isna(dt1) else dt2

        if not pd.isna(dt):
            return dt.strftime("%Y-%m-%d")

    return None

def get_engine(db_url: str) -> Engine:
    return create_engine(db_url, pool_pre_ping=True)

def ensure_cols(df: pd.DataFrame, required: List[str], name: str):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{name} missing required columns {missing}. Found: {list(df.columns)}")


# ---------------------------- Transform: Customers ----------------------------

def transform_customers(df: pd.DataFrame, logger: logging.Logger) -> Tuple[pd.DataFrame, int, int]:
    """
    Input columns (your file): customer_id, first_name, last_name, email, phone, city, registration_date
    - Drop missing email (NOT NULL + UNIQUE)
    - Dedupe by email
    - Standardize phone
    - Standardize registration_date
    Keep source_customer_key = raw customer_id like C001 for mapping later (not loaded to DB).
    """
    df = df.copy()
    missing_handled = 0

    ensure_cols(df, ["customer_id", "first_name", "last_name", "email"], "customers_raw.csv")

    # normalize
    for c in ["customer_id", "first_name", "last_name", "email", "phone", "city", "registration_date"]:
        df[c] = df[c].apply(normalize_null)

    # drop missing email
    before = len(df)
    df = df.dropna(subset=["email"])
    dropped = before - len(df)
    missing_handled += dropped
    if dropped:
        logger.info(f"Customers: dropped {dropped} rows due to missing email.")

    # standardize phone/date
    df["phone"] = df["phone"].apply(standardize_phone)
    df["registration_date"] = df["registration_date"].apply(parse_date_to_yyyy_mm_dd)

    # remove duplicates by email
    before = len(df)
    df = df.drop_duplicates(subset=["email"], keep="first")
    dup_removed = before - len(df)
    if dup_removed:
        logger.info(f"Customers: removed {dup_removed} duplicate rows by email.")

    # Return customer_id source key for mapping + DB insert cols
    out = df[[
        "customer_id",          # source key
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "registration_date"
    ]].copy()

    return out, dup_removed, missing_handled


# ---------------------------- Transform: Products ----------------------------

def transform_products(df: pd.DataFrame, logger: logging.Logger) -> Tuple[pd.DataFrame, int, int]:
    """
    Input columns (your file): product_id, product_name, category, price, stock_quantity
    - Standardize category
    - Fill missing stock_quantity with 0
    - Fill missing price with category median then global median (then drop if still missing)
    - Dedupe by product_id (source key)
    """
    df = df.copy()
    missing_handled = 0

    ensure_cols(df, ["product_id", "product_name", "category", "price"], "products_raw.csv")

    for c in ["product_id", "product_name", "category", "price", "stock_quantity"]:
        df[c] = df[c].apply(normalize_null)

    # drop missing product_name (NOT NULL)
    before = len(df)
    df = df.dropna(subset=["product_name"])
    dropped = before - len(df)
    missing_handled += dropped
    if dropped:
        logger.info(f"Products: dropped {dropped} rows due to missing product_name.")

    # category standardize
    df["category"] = df["category"].apply(standardize_category)

    # stock fill
    df["stock_quantity"] = pd.to_numeric(df["stock_quantity"], errors="coerce").fillna(0).astype(int)

    # price numeric
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # fill missing prices
    global_median = df["price"].median()
    df["price"] = df.groupby("category")["price"].transform(lambda s: s.fillna(s.median()))
    df["price"] = df["price"].fillna(global_median)

    before = len(df)
    df = df.dropna(subset=["price"])
    dropped = before - len(df)
    missing_handled += dropped
    if dropped:
        logger.info(f"Products: dropped {dropped} rows due to missing price after fill.")

    # remove duplicates by source product_id
    before = len(df)
    df = df.drop_duplicates(subset=["product_id"], keep="first")
    dup_removed = before - len(df)
    if dup_removed:
        logger.info(f"Products: removed {dup_removed} duplicate rows by product_id.")

    out = df[[
        "product_id",      # source key
        "product_name",
        "category",
        "price",
        "stock_quantity"
    ]].copy()

    return out, dup_removed, missing_handled


# ---------------------------- Load Customers / Products + Build Mapping ----------------------------

def load_customers_and_build_map(engine: Engine, customers: pd.DataFrame, logger: logging.Logger) -> Dict[str, int]:
    """
    Insert into customers WITHOUT customer_id (identity).
    Use email (unique) for upsert to support reruns.
    Build mapping: source_customer_key(C001) -> db_customer_id(1)
    """
    mapping: Dict[str, int] = {}

    with engine.begin() as conn:
        for _, r in customers.iterrows():
            source_key = r["customer_id"]
            payload = {
                "first_name": r["first_name"],
                "last_name": r["last_name"],
                "email": r["email"],
                "phone": r["phone"],
                "city": r["city"],
                "registration_date": r["registration_date"]
            }

            # Postgres upsert by email + return id
            customer_id = conn.execute(text("""
                INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
                VALUES (:first_name, :last_name, :email, :phone, :city, :registration_date)
                ON CONFLICT (email) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name  = EXCLUDED.last_name,
                    phone      = EXCLUDED.phone,
                    city       = EXCLUDED.city,
                    registration_date = EXCLUDED.registration_date
                RETURNING customer_id;
            """), payload).scalar()

            mapping[str(source_key)] = int(customer_id)

    logger.info(f"Loaded/merged customers: {len(mapping)}")
    return mapping


def load_products_and_build_map(engine: Engine, products: pd.DataFrame, logger: logging.Logger) -> Dict[str, int]:
    """
    Insert into products WITHOUT product_id (identity).
    No unique constraint exists, so we do:
    - Check if product already exists by (product_name, category)
    - If exists: update price/stock and reuse id
    - Else: insert and RETURNING product_id
    Build mapping: source_product_key(P001) -> db_product_id(1)
    """
    mapping: Dict[str, int] = {}

    with engine.begin() as conn:
        for _, r in products.iterrows():
            source_key = r["product_id"]
            payload = {
                "product_name": r["product_name"],
                "category": r["category"],
                "price": float(r["price"]),
                "stock_quantity": int(r["stock_quantity"])
            }

            # find existing
            existing = conn.execute(text("""
                SELECT product_id
                FROM products
                WHERE product_name = :product_name AND category = :category
                ORDER BY product_id
                LIMIT 1;
            """), {"product_name": payload["product_name"], "category": payload["category"]}).scalar()

            if existing is not None:
                conn.execute(text("""
                    UPDATE products
                    SET price = :price,
                        stock_quantity = :stock_quantity
                    WHERE product_id = :product_id;
                """), {"price": payload["price"], "stock_quantity": payload["stock_quantity"], "product_id": int(existing)})
                mapping[str(source_key)] = int(existing)
            else:
                product_id = conn.execute(text("""
                    INSERT INTO products (product_name, category, price, stock_quantity)
                    VALUES (:product_name, :category, :price, :stock_quantity)
                    RETURNING product_id;
                """), payload).scalar()
                mapping[str(source_key)] = int(product_id)

    logger.info(f"Loaded/merged products: {len(mapping)}")
    return mapping


# ---------------------------- Transform Sales -> Orders + Order Items ----------------------------

def transform_sales_to_orders(
    sales_df: pd.DataFrame,
    customer_map: Dict[str, int],
    product_map: Dict[str, int],
    logger: logging.Logger
) -> Tuple[pd.DataFrame, pd.DataFrame, int, int]:
    """
    Your sales file columns:
    transaction_id, customer_id, product_id, quantity, unit_price, transaction_date, status

    - Deduplicate transaction_id
    - Convert date to YYYY-MM-DD
    - Map customer_id (C001) -> db_customer_id (1)
    - Map product_id (P001) -> db_product_id (1)
    - Drop rows with missing/invalid mapping
    - Create orders grouped by (customer_id, order_date, status)
    - Create order_items per row
    """
    df = sales_df.copy()
    missing_handled = 0

    ensure_cols(df, ["transaction_id", "customer_id", "product_id", "quantity", "unit_price", "transaction_date"], "sales_raw.csv")

    for c in ["transaction_id", "customer_id", "product_id", "transaction_date", "status"]:
        df[c] = df[c].apply(normalize_null)

    # numeric fields
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # date
    df["order_date"] = df["transaction_date"].apply(parse_date_to_yyyy_mm_dd)

    # drop missing required for load
    before = len(df)
    df = df.dropna(subset=["customer_id", "product_id", "quantity", "unit_price", "order_date"])
    dropped = before - len(df)
    missing_handled += dropped
    if dropped:
        logger.info(f"Sales: dropped {dropped} rows due to missing ids/qty/price/date.")

    # status default
    df["status"] = df["status"].fillna("Pending")

    # remove duplicate transactions
    before = len(df)
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")
    dup_removed = before - len(df)
    if dup_removed:
        logger.info(f"Sales: removed {dup_removed} duplicate rows by transaction_id.")

    # sanity checks
    before = len(df)
    df = df[(df["quantity"] >= 1) & (df["unit_price"] >= 0)]
    dropped = before - len(df)
    missing_handled += dropped
    if dropped:
        logger.info(f"Sales: dropped {dropped} rows due to invalid quantity/unit_price.")

    # map to DB keys
    df["db_customer_id"] = df["customer_id"].map(customer_map)
    df["db_product_id"] = df["product_id"].map(product_map)

    before = len(df)
    df = df.dropna(subset=["db_customer_id", "db_product_id"])
    dropped = before - len(df)
    missing_handled += dropped
    if dropped:
        logger.info(f"Sales: dropped {dropped} rows due to missing customer/product mapping.")

    df["db_customer_id"] = df["db_customer_id"].astype(int)
    df["db_product_id"] = df["db_product_id"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)

    # order_items
    items = pd.DataFrame({
        "customer_id": df["db_customer_id"],
        "order_date": df["order_date"],
        "status": df["status"],
        "product_id": df["db_product_id"],
        "quantity": df["quantity"],
        "unit_price": df["unit_price"],
    })
    items["subtotal"] = items["quantity"] * items["unit_price"]

    # orders grouped
    orders = (
        items.groupby(["customer_id", "order_date", "status"], as_index=False)["subtotal"]
        .sum()
        .rename(columns={"subtotal": "total_amount"})
    )

    logger.info(f"Sales -> Orders to load: {len(orders)}")
    logger.info(f"Sales -> Order items to load: {len(items)}")

    return orders, items, dup_removed, missing_handled


# ---------------------------- Load Orders + Order Items ----------------------------

def load_orders_and_items(engine: Engine, orders: pd.DataFrame, items: pd.DataFrame, logger: logging.Logger) -> Tuple[int, int]:
    """
    Insert orders row-by-row with RETURNING order_id, then insert matching order_items.
    """
    if orders.empty or items.empty:
        logger.info("No orders/items to load.")
        return 0, 0

    orders_inserted = 0
    items_inserted = 0

    # group items per order key
    grouped: Dict[Tuple[int, str, str], pd.DataFrame] = {}
    for (cid, od, st), g in items.groupby(["customer_id", "order_date", "status"]):
        grouped[(int(cid), str(od), str(st))] = g.copy()

    with engine.begin() as conn:
        for _, o in orders.iterrows():
            key = (int(o["customer_id"]), str(o["order_date"]), str(o["status"]))
            g = grouped.get(key)
            if g is None or g.empty:
                continue

            order_id = conn.execute(text("""
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (:customer_id, :order_date, :total_amount, :status)
                RETURNING order_id;
            """), {
                "customer_id": key[0],
                "order_date": key[1],
                "total_amount": float(o["total_amount"]),
                "status": key[2] if key[2] else "Pending"
            }).scalar()

            orders_inserted += 1

            payload_items = []
            for _, r in g.iterrows():
                payload_items.append({
                    "order_id": int(order_id),
                    "product_id": int(r["product_id"]),
                    "quantity": int(r["quantity"]),
                    "unit_price": float(r["unit_price"]),
                    "subtotal": float(r["subtotal"]),
                })

            conn.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (:order_id, :product_id, :quantity, :unit_price, :subtotal)
            """), payload_items)

            items_inserted += len(payload_items)

    logger.info(f"Loaded {orders_inserted} orders and {items_inserted} order_items.")
    return orders_inserted, items_inserted


# ---------------------------- Report ----------------------------

def write_report(path: str, metrics: List[DQMetrics], logger: logging.Logger):
    lines = []
    lines.append("Flexi Mart - Data Quality Report")
    lines.append("=" * 40)
    lines.append("")

    for m in metrics:
        lines.append(f"File: {m.file_name}")
        lines.append(f"  Number of records processed:      {m.records_read}")
        lines.append(f"  Number of duplicates removed:     {m.duplicates_removed}")
        lines.append(f"  Number of missing values handled: {m.missing_values_handled}")
        lines.append(f"  Number loaded successfully:       {m.records_loaded_successfully}")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info(f"Data quality report written to: {path}")


# ---------------------------- Main ----------------------------

def main():
    load_dotenv()

    db_url = os.getenv("DB_URL", "").strip()
    raw_dir = os.getenv("RAW_DIR", "./data/raw").strip()
    report_path = os.getenv("REPORT_PATH", "./data_quality_report.txt").strip()
    log_path = os.getenv("LOG_PATH", "./etl.log").strip()

    logger = setup_logger(log_path)

    if not db_url:
        raise ValueError("DB_URL is missing in .env")

    engine = get_engine(db_url)

    customers_path = os.path.join(raw_dir, "customers_raw.csv")
    products_path = os.path.join(raw_dir, "products_raw.csv")
    sales_path = os.path.join(raw_dir, "sales_raw.csv")

    metrics = [DQMetrics("customers_raw.csv"), DQMetrics("products_raw.csv"), DQMetrics("sales_raw.csv")]

    try:
        # Extract
        customers_raw = safe_read_csv(customers_path, logger)
        products_raw = safe_read_csv(products_path, logger)
        sales_raw = safe_read_csv(sales_path, logger)

        metrics[0].records_read = len(customers_raw)
        metrics[1].records_read = len(products_raw)
        metrics[2].records_read = len(sales_raw)

        # Transform
        customers_t, c_dup, c_miss = transform_customers(customers_raw, logger)
        products_t, p_dup, p_miss = transform_products(products_raw, logger)

        metrics[0].duplicates_removed = c_dup
        metrics[0].missing_values_handled = c_miss
        metrics[1].duplicates_removed = p_dup
        metrics[1].missing_values_handled = p_miss

        # Load customers/products and build mapping from source keys (C001/P001) -> DB ids
        customer_map = load_customers_and_build_map(engine, customers_t, logger)
        product_map = load_products_and_build_map(engine, products_t, logger)

        metrics[0].records_loaded_successfully = len(customer_map)
        metrics[1].records_loaded_successfully = len(product_map)

        # Sales -> orders/items transform using mapping
        orders_t, items_t, s_dup, s_miss = transform_sales_to_orders(sales_raw, customer_map, product_map, logger)
        metrics[2].duplicates_removed = s_dup
        metrics[2].missing_values_handled = s_miss

        # Load orders/items
        o_loaded, i_loaded = load_orders_and_items(engine, orders_t, items_t, logger)
        # For sales file, count inserted rows as orders+items (or you can change to just items if you prefer)
        metrics[2].records_loaded_successfully = o_loaded + i_loaded

        # Report
        write_report(report_path, metrics, logger)
        logger.info("ETL Completed Successfully.")

    except Exception as e:
        logger.exception(f"ETL Failed: {e}")
        try:
            write_report(report_path, metrics, logger)
        except Exception:
            pass
        raise


if __name__ == "__main__":
    main()
