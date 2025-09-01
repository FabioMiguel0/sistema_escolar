import sqlite3
from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        disciplina TEXT NOT NULL,
        valor REAL,
        periodo TEXT,
        turma_id INTEGER,
        professor_id INTEGER
    )
    """)
    conn.commit()
    conn.close()

def create_nota(aluno_id: int, disciplina: str, valor: float, periodo: str = None, turma_id: int = None, professor_id: int = None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notas (aluno_id, disciplina, valor, periodo, turma_id, professor_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (aluno_id, disciplina, valor, periodo, turma_id, professor_id))
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return nid

# compatibilidade: add_nota (usada por views antigas)
def add_nota(aluno_id: int, disciplina: str, valor: float, periodo: str = None, turma_id: int = None, professor_id: int = None):
    return create_nota(aluno_id, disciplina, valor, periodo, turma_id, professor_id)

def get_notas_by_aluno(aluno_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, aluno_id, disciplina, valor, periodo, turma_id, professor_id FROM notas WHERE aluno_id = ? ORDER BY periodo, disciplina", (aluno_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_boletim_summary(aluno_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(periodo, '') as periodo, AVG(valor) as media
        FROM notas
        WHERE aluno_id = ?
        GROUP BY periodo
        ORDER BY periodo
    """, (aluno_id,))
    rows = cur.fetchall()
    conn.close()
    return [ {'periodo': r['periodo'], 'media': r['media']} for r in rows ]

def list_notas(aluno_id: int = None, turma_id: int = None, professor_id: int = None):
    """
    Retorna notas; aceita filtros opcionais por aluno_id, turma_id ou professor_id.
    """
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()

    q = "SELECT * FROM notas"
    params = []
    where = []
    if aluno_id is not None:
        where.append("aluno_id = ?"); params.append(aluno_id)
    if turma_id is not None:
        where.append("turma_id = ?"); params.append(turma_id)
    if professor_id is not None:
        where.append("professor_id = ?"); params.append(professor_id)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY id DESC"

    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def seed_sample():
    ensure_table()
    # inserir exemplos só se tabela vazia
    if not list_notas():
        create_nota(1, "Matemática", 15.0, "2025-1", turma_id=1, professor_id=2)
        create_nota(1, "Português", 12.0, "2025-1", turma_id=1, professor_id=3)
        create_nota(2, "Matemática", 10.0, "2025-1", turma_id=1, professor_id=2)
