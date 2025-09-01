import flet as ft
from services.turma_service import list_turmas

def ClassesView(page: ft.Page, role=None, current_user_id=None):
    page.auto_scroll = True
    title = ft.Text("Minhas Turmas", size=18, weight="bold")
    try:
        turmas = list_turmas()
    except Exception:
        turmas = []

    # filtra turmas do professor, se current_user_id fornecido
    if current_user_id:
        minhas = [t for t in turmas if t.get("professor_id") == current_user_id]
    else:
        minhas = []

    # se não há turmas atribuídas, mostra mensagem clara (não lista todas)
    if not minhas:
        body = ft.Column([ft.Text("Nenhuma turma atribuída a este professor.")])
    else:
        rows = [ft.Row([ft.Text(str(t.get("id")), width=60), ft.Text(t.get("nome") or "", expand=True)]) for t in minhas]
        body = ft.Column(rows)

    return ft.Container(content=ft.Column([title, ft.Divider(), body]), expand=True, padding=12)