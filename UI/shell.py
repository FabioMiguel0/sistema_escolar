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
        self._drawer_open = False
        try:
            def _on_resize(e):
                if callable(self.on_route_change):
                    self.on_route_change(self.current_route)
            self.page.on_resize = _on_resize
        except Exception:
            pass

    def _on_route_click(self, route: str):
        self._drawer_open = False
        if callable(self.on_route_change):
            self.on_route_change(route)

    def _build_nav_items(self):
        controls = []
        items = menu_for_role(self.role) or []
        for route, label in items:
            controls.append(ft.ListTile(title=ft.Text(label), on_click=lambda e, r=route: self._on_route_click(r)))
        controls.append(ft.Divider())
        controls.append(ft.ListTile(title=ft.Text("Sair / Logout"), on_click=lambda e: self._on_route_click("logout")))
        return controls

    def _get_width(self):
        try:
            if hasattr(self.page, "window_width") and self.page.window_width:
                return self.page.window_width
            if hasattr(self.page, "client_size") and getattr(self.page.client_size, "width", None):
                return self.page.client_size.width
        except Exception:
            pass
        return 1000

    def build(self):
        try:
            content_control = self.content_builder() if callable(self.content_builder) else self.content_builder
        except Exception as ex:
            content_control = ft.Container(content=ft.Text(f"Erro ao construir conteúdo: {ex}"), padding=12)

        w = self._get_width()
        mobile = w < 600
        tablet = 600 <= w < 900
        desktop = w >= 900

        # Tela de login — centraliza
        if self.current_route == "login":
            max_w = 560 if desktop else (460 if tablet else 340)
            centered = ft.Column([ft.Container(content=content_control, width=max_w)], alignment="center", horizontal_alignment="center", expand=True)
            return ft.View("/", controls=[centered])

        nav_items = self._build_nav_items()
        nav_header = ft.Column([ft.Row([ft.Icon(ft.Icons.SCHOOL, color=ft.colors.PRIMARY), ft.Text("Sistema Escolar", weight="bold")]), ft.Text(f"Olá, {self.username}", size=12), ft.Divider()], tight=True)

        if desktop:
            sidebar = ft.Container(content=ft.Column([nav_header] + nav_items, spacing=6), width=260, padding=12)
            content_view = ft.Container(content=content_control, expand=True, padding=20)
            view = ft.View("/", controls=[ft.Row([sidebar, ft.VerticalDivider(width=1), content_view], expand=True)])
            return view

        if tablet:
            sidebar = ft.Container(content=ft.Column([nav_header] + nav_items, spacing=6), width=200, padding=10)
            content_view = ft.Container(content=content_control, expand=True, padding=16)
            view = ft.View("/", controls=[ft.Row([sidebar, ft.VerticalDivider(width=1), content_view], expand=True)])
            return view

        # Mobile
        def _toggle(e=None):
            self._drawer_open = not self._drawer_open
            if callable(self.on_route_change):
                self.on_route_change(self.current_route)
        menu_btn = ft.IconButton(icon=ft.icons.MENU, on_click=_toggle)
        title = ft.Text("Sistema Escolar", weight="bold", size=16)
        appbar = ft.Container(content=ft.Row([menu_btn, title], alignment="start"), padding=ft.padding.symmetric(horizontal=8, vertical=6))
        drawer = ft.Container(content=ft.Column([nav_header] + nav_items, spacing=4), visible=self._drawer_open, padding=12)
        content_view = ft.Container(content=content_control, expand=True, padding=12)
        view = ft.View("/", controls=[ft.Column([appbar, ft.Divider(), drawer, content_view], expand=True)])
        return view
