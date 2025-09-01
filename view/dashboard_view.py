import flet as ft
from services.aluno_service import count_alunos
from services.turma_service import count_turmas
from services.professor_service import count_professores


def _card(title: str, value: str, icon=None):
    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(icon) if icon else ft.Icon(ft.Icons.INFO),
                        ft.Container(width=8),
                        ft.Text(title, size=12),
                    ],
                    vertical_alignment="center",
                ),
                ft.Container(height=8),
                ft.Text(value, size=28, weight="bold"),
            ],
            tight=True,
        ),
        padding=12,
        margin=8,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_50),
        width=220,
        height=120,
    )


def DashboardView(page: ft.Page, role="aluno", username=None, go=None):
    alunos_count = count_alunos()
    turmas_count = count_turmas()
    profs_count = count_professores()

    card_alunos = _card("Alunos", str(alunos_count), icon=ft.Icons.SCHOOL)
    card_turmas = _card("Turmas", str(turmas_count), icon=ft.Icons.GROUP)
    card_profs = _card("Professores", str(profs_count), icon=ft.Icons.PERSON)

    # atalhos rápidos (botões)
    def _shortcut_button(text, route):
        return ft.ElevatedButton(text, on_click=lambda e: go(route) if callable(go) else page.client_storage.set("go_to", route) or page.update())

    shortcuts = ft.Row(
        [
            _shortcut_button("Gerenciar Alunos", "alunos"),
            _shortcut_button("Gerenciar Turmas", "turmas"),
            _shortcut_button("Lançar Notas", "notas"),
            _shortcut_button("Registrar Frequência", "frequencia"),
        ],
        spacing=12,
    )

    header = ft.Column(
        [
            ft.Text("Dashboard", size=24, weight="bold"),
            ft.Text(f"Bem vindo, {username or 'Usuário'}", size=12, color=ft.Colors.GREY),
        ]
    )

    content = ft.Column(
        [
            ft.Row([card_alunos, card_turmas, card_profs]),
            ft.Container(height=12),
            shortcuts,
            ft.Container(height=12),
            ft.Divider(),
            ft.Text("Visão rápida de ações", size=14),
        ],
        expand=True,
        tight=True,
    )

    container = ft.Container(content=ft.Column([header, ft.Container(height=12), content], tight=True), expand=True, padding=12)

    # função para atualizar os valores dos cards
    def atualizar_metricas():
        try:
            # atualiza os textos dos cards
            card_alunos.controls[0].controls[2].value = str(count_alunos())
            card_turmas.controls[0].controls[2].value = str(count_turmas())
            card_profs.controls[0].controls[2].value = str(count_professores())
        except Exception:
            pass
        # força update da página quando chamado
        page.update()

    setattr(container, "atualizar_metricas", atualizar_metricas)
    return container
