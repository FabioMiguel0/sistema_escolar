from models.frequencia import Frequencia
from services.db import get_conn
import datetime

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS frequencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        data TEXT,
        presente INTEGER
    )
    """)
    conn.commit()
    conn.close()

def registrar(aluno_id, data, presente):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO frequencias (aluno_id, data, presente) VALUES (?, ?, ?)", (aluno_id, data, 1 if presente else 0))
    conn.commit()
    conn.close()

def listar(aluno_id=None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    if aluno_id:
        cur.execute("SELECT * FROM frequencias WHERE aluno_id=? ORDER BY data DESC", (aluno_id,))
    else:
        cur.execute("SELECT * FROM frequencias ORDER BY data DESC")
    rows = cur.fetchall(); conn.close()
    return [dict(r) for r in rows]

class FrequenciaService:
    def __init__(self):
        self.frequencias = []

    def registrar_frequencia(self, frequencia: Frequencia):
        self.frequencias.append(frequencia)

    def editar_frequencia(self, id_frequencia, **kwargs):
        for f in self.frequencias:
            if f.id_frequencia == id_frequencia:
                for chave, valor in kwargs.items():
                    setattr(f, chave, valor)

    def excluir_frequencia(self, id_frequencia):
        self.frequencias = [f for f in self.frequencias if f.id_frequencia != id_frequencia]

    def listar_frequencia_por_aluno(self, aluno_id):
        return [f for f in self.frequencias if f.aluno_id == aluno_id]
