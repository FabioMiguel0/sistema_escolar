from services.db import get_conn

def ensure_table():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    conn.commit(); conn.close()

def create(nome):
    ensure_table(); conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO disciplinas (nome) VALUES (?)", (nome,))
    conn.commit(); conn.close()

def list_disciplinas():
    ensure_table(); conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM disciplinas ORDER BY nome")
    rows = cur.fetchall(); conn.close()
    return [dict(r) for r in rows]

def add_disciplina(nome:str):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO disciplinas (nome) VALUES (?)", (nome.strip(),))
    conn.commit(); conn.close()

def update_disciplina(disciplina_id:int, nome:str):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE disciplinas SET nome=? WHERE id=?", (nome.strip(), disciplina_id))
    conn.commit(); conn.close()

def delete_disciplina(disciplina_id:int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM matriculas WHERE disciplina_id=?", (disciplina_id,))
    cur.execute("DELETE FROM notas WHERE disciplina_id=?", (disciplina_id,))
    cur.execute("DELETE FROM disciplinas WHERE id=?", (disciplina_id,))
    conn.commit(); conn.close()
