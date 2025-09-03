import os
import sys
import importlib
import flet as ft

# garante imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# imports resilientes das views / serviços (evitam falhas na importação)
try:
    from services.db import create_tables_and_seed
except Exception:
    create_tables_and_seed = lambda: None

# importa views de forma defensiva (se faltar, mostra placeholder)
def _safe_import(name, default=None):
    try:
        mod = importlib.import_module(name)
        return mod
    except Exception:
        return default

UI_mod = _safe_import("UI")
LoginView = getattr(UI_mod, "LoginView", None) if UI_mod else None
ShellClass = getattr(_safe_import("UI.shell"), "Shell")

# tenta carregar views (se não existir, usa stub)
def _get_view(name):
    try:
        m = importlib.import_module(f"view.{name}_view")
        # busca função que constrói a view (ex.: AlunoView, DashboardView ...)
        for attr in dir(m):
            if attr.lower().startswith(name):
                return getattr(m, attr)
        # fallback: primeira chamada que termine com 'View'
        for attr in dir(m):
            if attr.endswith("View"):
                return getattr(m, attr)
    except Exception:
        return None
    return None

DashboardView = _get_view("dashboard")
DocumentoView = _get_view("documento")
ComunicadoView = _get_view("comunicado")
AlunoView = _get_view("aluno")
TurmaView = _get_view("turma")
ProfessorView = _get_view("professor")
# ... outros views podem ser carregados on-demand no build_content

def main(page: ft.Page):
    page.title = "Sistema Escolar"
    page.window_width = 1100
    page.window_height = 700
    page.scroll = "auto"

    # cria tabelas/seed se existir
    try:
        create_tables_and_seed()
    except Exception:
        pass

    state = {"user": None, "user_id": None, "role": None, "route": "login"}

    def build_content():
        r = state.get("route", "dashboard")
        role = state.get("role")
        # rotas básicas — adiciona mais conforme necessário
        if r == "login":
            if LoginView:
                return LoginView(page, go=go)
            return ft.Container(content=ft.Text("Login view não encontrada"), expand=True)
        if r == "dashboard":
            if DashboardView:
                return DashboardView(page, role=role, username=state.get("user"), go=go)
            return ft.Container(content=ft.Text("Dashboard não encontrada"), expand=True)
        if r == "documentos":
            if DocumentoView:
                return DocumentoView(page, user=state.get("user"), role=state.get("role"), user_id=state.get("user_id"))
            return ft.Container(content=ft.Text("Documentos view não encontrada"), expand=True)
        if r == "alunos":
            if AlunoView:
                return AlunoView(page, role=role, current_user_id=state.get("user_id"), go=go)
            return ft.Container(content=ft.Text("Alunos view não encontrada"), expand=True)
        if r == "turmas":
            if TurmaView:
                return TurmaView(page, role=role, current_user_id=state.get("user_id"), go=go)
            return ft.Container(content=ft.Text("Turmas view não encontrada"), expand=True)
        if r == "professores":
            if ProfessorView:
                return ProfessorView(page, role=role, current_user_id=state.get("user_id"), go=go)
            return ft.Container(content=ft.Text("Professores view não encontrada"), expand=True)
        # default
        return ft.Container(content=ft.Text(f"Tela '{r}' em construção..."), expand=True)

    def go(route: str, user=None, role=None, user_id=None):
        if user is not None:
            state["user"] = user
        if role is not None:
            state["role"] = role
        if user_id is not None:
            state["user_id"] = user_id
        if route == "logout":
            state["user"] = state["role"] = state["user_id"] = None
            route = "login"
        state["route"] = route
        page.views.clear()
        shell = ShellClass(
            page=page,
            username=state.get("user") or "Usuário",
            role=state.get("role") or "aluno",
            current_route=state.get("route") or "dashboard",
            on_route_change=go,
            content_builder=lambda: build_content()
        )
        page.views.append(shell.build())
        page.update()

    # inicia na rota login ou auto-login para testes
    if os.environ.get("AUTO_LOGIN") == "1":
        go("dashboard", user="admin", role="admin", user_id=1)
    else:
        go("login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8550"))
    # em produção (PORT setada pelo Render) usar 0.0.0.0
    host = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
    url_host = "localhost" if host == "127.0.0.1" else "0.0.0.0"
    print(f"[START] listening on {host}:{port} — open http://{url_host}:{port} in your browser if accessible")
    ft.app(target=main, view=ft.WEB_BROWSER, host=host, port=port)
