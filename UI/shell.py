import flet as ft
from typing import Callable

class Shell:
    def __init__(self, page: ft.Page, username: str, role: str, on_route_change: Callable, content_builder: Callable):
        self.page = page
        self.username = username
        self.role = role
        self.on_route_change = on_route_change
        self.content_builder = content_builder

    def build(self):
        # menu básico por papel (adiciona 'usuarios' apenas ao admin)
        menu = {
            "admin": ["dashboard", "usuarios", "professores", "turmas", "disciplinas", "alunos", "documentos", "comunicados", "calendario"],
            "secretaria": ["dashboard", "alunos", "turmas", "documentos", "comunicados", "calendario", "disciplinas"],
            "professor": ["dashboard", "frequencia", "notas", "comunicados"],
            "aluno": ["dashboard", "alunos", "notas", "comunicados", "calendario"],
            "responsavel": ["dashboard", "comunicados", "calendario"],
            "suporte": ["dashboard"],
        }
        allowed = menu.get(self.role, ["dashboard"])

        # cria botões de navegação
        nav_buttons = []
        for r in allowed:
            nav_buttons.append(ft.ElevatedButton(r.capitalize(), on_click=lambda e, rr=r: self._route(rr), width=160))

        logout_btn = ft.TextButton("Sair", on_click=lambda e: self._route("logout"))

        # content area: chama content_builder para obter a view/control
        content_control = self.content_builder()

        left_col = ft.Column(
            [
                ft.Text(f"{self.username}", weight="bold"),
                ft.Container(height=12),
                *nav_buttons,
                ft.Container(height=16),
                logout_btn
            ],
            tight=True,
            horizontal_alignment="center"
        )

        main_row = ft.Row(
            [
                ft.Container(content=left_col, width=180, bgcolor=ft.Colors.BLUE_50, padding=12),
                ft.Container(content=content_control, expand=True, padding=12)
            ],
            expand=True
        )

        view = ft.View("/home", controls=[main_row])
        setattr(view, "route", "home")
        return view

    def _route(self, r):
        # chama callback do main para trocar a rota
        if callable(self.on_route_change):
            self.on_route_change(r)
