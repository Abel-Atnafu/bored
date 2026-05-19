import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".finance_tracker.db"

_CREATE = """
CREATE TABLE IF NOT EXISTS transactions (
    id          TEXT PRIMARY KEY,
    amount      REAL NOT NULL,
    category    TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    date        TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_transactions_date     ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
"""


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(_CREATE)


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


def fetch_transactions(month: str | None, category: str | None) -> list[dict]:
    clauses, params = [], []
    if month:
        clauses.append("date LIKE ?")
        params.append(f"{month}%")
    if category:
        clauses.append("category = ?")
        params.append(category.lower())

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"SELECT * FROM transactions {where} ORDER BY date DESC, created_at DESC"

    with get_conn() as conn:
        return [row_to_dict(r) for r in conn.execute(sql, params).fetchall()]


def fetch_summary(month: str | None) -> dict:
    clauses, params = [], []
    if month:
        clauses.append("date LIKE ?")
        params.append(f"{month}%")

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"SELECT category, SUM(amount) as total FROM transactions {where} GROUP BY category"

    with get_conn() as conn:
        rows = [row_to_dict(r) for r in conn.execute(sql, params).fetchall()]

    income = sum(r["total"] for r in rows if r["total"] > 0)
    expenses = sum(abs(r["total"]) for r in rows if r["total"] < 0)
    by_category = sorted(rows, key=lambda r: abs(r["total"]), reverse=True)

    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "by_category": [{"category": r["category"], "total": round(r["total"], 2)} for r in by_category],
    }


def insert_transaction(txn: dict) -> None:
    sql = """
        INSERT INTO transactions (id, amount, category, description, date, created_at)
        VALUES (:id, :amount, :category, :description, :date, :created_at)
    """
    with get_conn() as conn:
        conn.execute(sql, txn)


def delete_transaction(txn_id: str) -> bool:
    with get_conn() as conn:
        cursor = conn.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
        return cursor.rowcount == 1
