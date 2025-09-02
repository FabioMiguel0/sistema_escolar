import os
import sys
import flet as ft

# garante imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db import create_tables_and_seed
import importlib
try:
    seed = importlib.import_module("services.seed")
except ModuleNotFoundError:
    seed = None

from UI import LoginView
from UI.shell import Shell
from services.user_service import menu_for_role
from view.dashboard_view import DashboardView
from view.aluno_view import AlunoView
from view.professor_view import ProfessorView
from view.comunicado_view import ComunicadoView
from view.turma_view import TurmaView
from view.disciplina_view import DisciplinaView
from view.frequencia_view import FrequenciaView
from view.nota_view import NotaView
from view.documento_view import DocumentoView
from view.calendario_view import CalendarioView
from view.users_view import UsersView
from view.student.performance_view import PerformanceView
from view.student.report_card_view import ReportCardView
from view.student.grades_view import GradesView
from view.student.profile_view import ProfileView  # <<< novo import
from view.teacher.classes_view import ClassesView
from view.teacher.schedule_view import ScheduleView
from view.teacher.subjects_taught_view import SubjectsTaughtView


def main(page: ft.Page):
    print("[MAIN] flet main() started")   # <-- adicione isto
    page.title = "Sistema Escolar"
    page.window_width = 1100
    page.window_height = 700
    page.scroll = "auto"

    create_tables_and_seed()

    state = {"user": None, "user_id": None, "role": None, "route": "dashboard"}

    permissions = {
        "admin": {"dashboard", "usuarios", "professores", "disciplinas", "turmas", "alunos", "documentos", "comunicados", "calendario", "frequencia", "notas"},
        "secretaria": {"dashboard", "alunos", "turmas", "documentos", "comunicados", "calendario", "disciplinas"},
        "professor": {"dashboard", "frequencia", "notas", "comunicados", "minhas_turmas", "horario", "minhas_disciplinas", "documentos"},
        "aluno": {"perfil", "desempenho", "boletim", "horario"},
        "responsavel": {"dashboard", "comunicados", "calendario"},
        "suporte": {"dashboard"},
    }

    shell = None

    def build_shell(page, state, build_content):
        nonlocal shell
        shell = Shell(
            page=page,
            username=state.get("user") or "Usuário",
            role=state.get("role") or "aluno",
            current_route=state.get("route") or "dashboard",
            on_route_change=go,
            content_builder=lambda: build_content()
        )
        return shell.build()

    def build_content():
        r = state.get("route", "dashboard")
        role = state.get("role")
        print(f"[BUILD_CONTENT] route={r} role={role}")
        try:
            if r == "login":
                return LoginView(page, go=go)
            if r == "home":
                r = "dashboard"
                state["route"] = r
                role = state.get("role")
            if r == "dashboard":
                return DashboardView(page, role=role, username=state.get("user"), go=go)
            if r == "notas" and role == "aluno":
                return ProfileView(page, aluno_id=state.get("user_id"))
            if r == "perfil":
                return ProfileView(page, aluno_id=state.get("user_id"))
            if r == "usuarios":
                return UsersView(page, current_user=state.get("user"))
            if r == "alunos":
                return AlunoView(page, role=role, current_user_id=state.get("user_id"))
            if r == "turmas":
                return TurmaView(page, role=role)
            if r == "professores":
                return ProfessorView(page, role=role, current_user_id=state.get("user_id"))
            if r == "disciplinas":
                return DisciplinaView(page)
            if r == "notas":
                return NotaView(page, role=role, aluno_id=state.get("user_id"))
            if r == "desempenho":
                return PerformanceView(page, aluno_id=state.get("user_id"))
            if r == "boletim":
                return ReportCardView(page, aluno_id=state.get("user_id"))
            if r == "minhas_turmas":
                return ClassesView(page, role=role, current_user_id=state.get("user_id"))
            if r == "horario":
                return ScheduleView(page, role=role, current_user_id=state.get("user_id"))
            if r == "minhas_disciplinas":
                return SubjectsTaughtView(page, role=role, current_user_id=state.get("user_id"))
            if r == "frequencia":
                return FrequenciaView(page)
            if r == "comunicados":
                return ComunicadoView(page, user=state.get("user"))
            if r == "documentos":
                return DocumentoView(page, user=state.get("user"), role=state.get("role"), user_id=state.get("user_id"))
            if r == "calendario":
                return CalendarioView(page)
            return ft.Container(content=ft.Text(f"Tela '{r}' em construção..."), expand=True)
        except Exception as ex:
            import traceback
            tb = traceback.format_exc()
            print("[BUILD_CONTENT] exception:", tb)
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Erro interno ao construir a view", color=ft.Colors.RED, weight="bold"),
                        ft.Text(str(ex)),
                        ft.Divider(),
                        ft.Text(tb, selectable=True, size=10),
                    ]
                ),
                expand=True,
                padding=12,
            )

    def go(view: str, user=None, role=None, user_id=None):
        if user is not None:
            state["user"] = user
        if role is not None:
            state["role"] = role
        if user_id is not None:
            state["user_id"] = user_id

        if view == "logout":
            state["user"] = None
            state["role"] = None
            state["user_id"] = None
            view = "login"
        
        state["route"] = view

        page.views.clear()
        try:
            page.views.append(build_shell(page, state, build_content))
        except Exception as ex:
            page.views.append(ft.View("/", controls=[ft.Text(f"Erro ao construir UI: {ex}")]))

        page.update()

    if os.environ.get("AUTO_LOGIN") == "1":
        go("home", user="admin", role="admin", user_id=1)
    else:
        go("login")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8550"))
    # se estamos em produção (PORT definida pelo ambiente) escutamos em 0.0.0.0
    # se for execução local (sem PORT definida) usamos 127.0.0.1 para que o browser local abra corretamente
    if "PORT" in os.environ:
        host = "0.0.0.0"
        url_host = "0.0.0.0"
    else:
        host = "127.0.0.1"
        url_host = "localhost"

    print(f"[START] listening on {host}:{port} — open http://{url_host}:{port} in your browser")
    ft.app(target=main, view=ft.WEB_BROWSER, host=host, port=port)
