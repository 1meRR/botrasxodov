import sqlite3
from datetime import datetime
from pathlib import Path

from config import DB_NAME


def get_conn():
    Path(DB_NAME).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        create table if not exists expenses(
            id integer primary key autoincrement,
            title text not null,
            amount integer not null,
            created_at text not null
        )
        """
    )
    conn.commit()
    conn.close()


def add_expense(title, amount):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "insert into expenses(title, amount, created_at) values(?, ?, ?)",
        (title, amount, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_today():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    start = datetime.utcnow().date().isoformat()
    cur.execute(
        "select title, amount, created_at from expenses where created_at like ? order by id desc",
        (f"{start}%",),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_stats(limit=10):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "select title, sum(amount) as total from expenses group by title order by total desc limit ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
