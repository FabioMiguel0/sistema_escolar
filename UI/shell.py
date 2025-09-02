import flet as ft
from services.user_service import menu_for_role

class Shell:
    def __init__(self, page: ft.Page, username="Usuário", role="aluno", current_route=None, on_route_change=None, content_builder=None):
        self.page = page
        self.username = username
        self.role = role
        self.current_route = current_route
        self.on_route_change = on_route_change
        self.content_builder = content_builder

        # estado UI responsiva
        self._menu_open = False

        # reconstrói a UI quando a janela for redimensionada
        def _on_resize(e):
            if callable(self.on_route_change):
                # força rebuild chamando a função de rota actual
                self.on_route_change(self.current_route)
        # ligar handler (main.go irá rebuild via on_route_change)
        try:
            self.page.on_resize = _on_resize
        except Exception:
            pass

    def _on_route_click(self, route: str):
        # fecha menu em mobile ao navegar
        self._menu_open = False
        if callable(self.on_route_change):
            self.on_route_change(route)

    def _build_nav_items(self):
        items = []
        for route, label in menu_for_role(self.role):
            items.append(
                ft.Container(
                    content=ft.TextButton(label, on_click=lambda e, r=route: self._on_route_click(r)),
                    padding=ft.padding.only(top=4, bottom=4)
                )
            )
        # separador e logout
        items.append(ft.Divider())
        items.append(ft.Container(content=ft.TextButton("Sair / Logout", on_click=lambda e: self._on_route_click("logout")), padding=ft.padding.only(top=4, bottom=4)))
        return items

    def _get_window_width(self):
        # tenta várias propriedades para compatibilidade
        try:
            w = getattr(self.page, "window_width", None)
            if w:
                return w
            if hasattr(self.page, "client_size") and getattr(self.page.client_size, "width", None):
                return self.page.client_size.width
        except Exception:
            pass
        return 1000

    def build(self):
        # constrói o conteúdo principal usando content_builder
        try:
            content_control = self.content_builder() if callable(self.content_builder) else self.content_builder
        except Exception as ex:
            content_control = ft.Text(f"Erro ao construir conteúdo: {ex}")

        # largura actual do ecrã
        w = self._get_window_width()
        narrow = w < 900    # breakpoint: mobile/tablet

        # se estivermos na tela de login, não mostrar a barra lateral — centrar o conteúdo
        if self.current_route == "login":
            # calcula width responsivo para o formulário de login
            login_w = int(min(560, max(320, w * 0.8)))
            centered = ft.Column(
                [
                    ft.Container(content=content_control, width=login_w)
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True,
            )
            return ft.View("/", controls=[centered])

        # navegação (lista de botões)
        nav_items = self._build_nav_items()
        nav_column = ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.SCHOOL), ft.Text("Sistema Escolar", weight="bold")], alignment="start"),
                ft.Text(f"Olá, {self.username}", size=12),
                ft.Divider(),
            ] + nav_items,
            spacing=6,
            tight=True,
        )

        # layout para ecrãs largos: sidebar fixa + conteúdo expansível
        if not narrow:
            nav = ft.Container(content=nav_column, width=240, padding=12)
            content_view = ft.Container(expand=True, padding=16, content=content_control)
            view = ft.View(
                "/",
                controls=[
                    ft.Row(
                        [
                            nav,
                            ft.VerticalDivider(width=1, thickness=1),
                            content_view,
                        ],
                        expand=True,
                    )
                ],
            )
            return view

        # layout para ecrãs estreitos: top bar + opcional menu expansível
        # construir AppBar (simples)
        menu_btn = ft.IconButton(ft.icons.MENU, on_click=self._toggle_menu)
        title = ft.Text("Sistema Escolar", weight="bold")
        top_bar = ft.Row([menu_btn, title], alignment="start")

        # menu móvel: mostrado acima do conteúdo quando self._menu_open = True
        mobile_menu = ft.Column(nav_items, visible=self._menu_open, spacing=0, scroll="auto")

        content_view = ft.Container(expand=True, padding=12, content=content_control)
        view = ft.View(
            "/",
            controls=[
                ft.Column(
                    [
                        top_bar,
                        ft.Divider(),
                        mobile_menu,
                        content_view,
                    ],
                    spacing=8,
                    expand=True,
                )
            ],
        )
        return view

    def _toggle_menu(self, e=None):
        # alterna menu e força rebuild via on_route_change para refletir mudança
        self._menu_open = not self._menu_open
        if callable(self.on_route_change):
            self.on_route_change(self.current_route)
