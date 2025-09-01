import flet as ft
from services.disciplina_service import list_disciplinas  # se não existir, adapte

def SubjectsTaughtView(page: ft.Page, role=None, current_user_id=None):
    page.auto_scroll = True
    title = ft.Text("Disciplinas que leciono", size=18, weight="bold")
    try:
        d = list_disciplinas()
    except Exception:
        d = []
    # tenta filtrar por professor_id quando disponível
    minhas = [x for x in d if current_user_id and x.get("professor_id") == current_user_id] or d
    rows = [ft.Row([ft.Text(str(x.get("id")), width=60), ft.Text(x.get("nome") or "", expand=True)]) for x in minhas]
    return ft.Container(content=ft.Column([title, ft.Divider(), ft.Column(rows or [ft.Text("Nenhuma disciplina encontrada.")])]), expand=True, padding=12)