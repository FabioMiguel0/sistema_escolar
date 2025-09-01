import flet as ft
from services.db import get_conn


def DocumentoView(page: ft.Page):
    nome = ft.TextField(label="Nome do Documento", width=360)
    descricao = ft.TextField(label="Descrição", width=480)
    list_view = ft.ListView(expand=True, spacing=8, padding=8)

    def ensure_table():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT
        )
        """)
        conn.commit(); conn.close()

    def load():
        ensure_table()
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT * FROM documentos ORDER BY id DESC")
        for r in cur.fetchall():
            list_view.controls.append(ft.Row([ft.Text(r["nome"], expand=True), ft.Text(r["descricao"])]))
        conn.close()
        page.update()

    def on_add(e):
        ensure_table()
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO documentos (nome, descricao) VALUES (?, ?)", (nome.value, descricao.value))
        conn.commit(); conn.close()
        nome.value = ""; descricao.value = ""
        list_view.controls.clear(); load()

    add_btn = ft.ElevatedButton("Adicionar Documento", on_click=on_add)
    container = ft.Container(content=ft.Column([ft.Text("Documentos", size=18), ft.Row([nome, add_btn]), ft.Divider(), list_view]), expand=True)
    load()
    return container


