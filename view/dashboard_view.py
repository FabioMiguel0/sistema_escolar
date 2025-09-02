import flet as ft
from services.aluno_service import count_alunos
from services.turma_service import count_turmas
from services.professor_service import count_professores


def _card(title: str, value: str, icon=ft.Icons.INSIGHTS, color=ft.Colors.BLUE_600):
    return ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(icon, color=ft.Colors.WHITE), ft.Text(title, color=ft.Colors.WHITE)], alignment="start"),
                ft.Text(value, size=20, weight="bold", color=ft.Colors.WHITE),
            ],
            tight=True,
        ),
        padding=12,
        width=220,
        height=100,
        bgcolor=color,
        border_radius=ft.border_radius.all(8),
    )


def DashboardView(page: ft.Page, role=None, username=None, go=None):
    page.auto_scroll = True
    title = ft.Text(f"Dashboard — {username or ''}", size=20, weight="bold")

    # obtém contagens se as funções existirem
    try:
        alunos_count = str(count_alunos() or 0)
    except Exception:
        alunos_count = "—"
    try:
        turmas_count = str(count_turmas() or 0)
    except Exception:
        turmas_count = "—"
    try:
        prof_count = str(count_professores() or 0)
    except Exception:
        prof_count = "—"

    cards = ft.Row(
        [
            _card("Alunos", alunos_count, icon=ft.Icons.SCHOOL, color=ft.Colors.BLUE_600),
            _card("Turmas", turmas_count, icon=ft.Icons.GROUP, color=ft.Colors.BLUE_500),
            _card("Professores", prof_count, icon=ft.Icons.PERSON, color=ft.Colors.INDIGO_500),
        ],
        alignment="start",
        spacing=12,
    )

    body = ft.Column(
        [
            title,
            ft.Divider(),
            cards,
        ],
        spacing=12,
        expand=True,
    )

    return ft.Container(content=body, expand=True, padding=12)
