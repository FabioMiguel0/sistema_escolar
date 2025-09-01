from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def create(nome):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO turmas (nome) VALUES (?)", (nome,))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def list_turmas():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM turmas ORDER BY nome")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete(id_):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM turmas WHERE id=?", (id_,))
    conn.commit()
    conn.close()

def count_turmas():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) as c FROM turmas")
    r = cur.fetchone()
    conn.close()
    return r["c"] if r else 0
