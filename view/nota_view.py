import flet as ft
from services.nota_service import list_notas, add_nota
from services.aluno_service import get_all

def NotaView(page: ft.Page, role=None, aluno_id=None):
    alunos = get_all()
    aluno_options = [ft.dropdown.Option(str(a["id"]), text=a["nome"]) for a in alunos]
    aluno_dd = ft.Dropdown(label="Aluno", options=aluno_options, value=str(aluno_id) if aluno_id else (aluno_options[0].value if aluno_options else None))
    disciplina = ft.TextField(label="Disciplina", width=240)
    valor = ft.TextField(label="Nota", width=120)
    list_view = ft.ListView(expand=True, spacing=8, padding=8)

    def load():
        list_view.controls.clear()
        for n in list_notas(aluno_id=int(aluno_dd.value) if aluno_dd.value else None):
            list_view.controls.append(ft.Row([ft.Text(str(n["id"]), width=40), ft.Text(n["disciplina"], expand=True), ft.Text(str(n["valor"]))]))
        page.update()

    def on_add(e):
        if not aluno_dd.value or not disciplina.value or not valor.value: return
        add_nota(int(aluno_dd.value), disciplina.value, float(valor.value))
        disciplina.value = ""; valor.value = ""
        load()

    add_btn = ft.ElevatedButton("Adicionar Nota", on_click=on_add)
    container = ft.Container(content=ft.Column([ft.Text("Notas", size=18), ft.Row([aluno_dd, disciplina, valor, add_btn]), ft.Divider(), list_view]), expand=True)
    load()
    return container
