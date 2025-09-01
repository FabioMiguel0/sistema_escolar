import os
import sys
import flet as ft

# garante imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db import create_tables_and_seed
from UI import LoginView, Shell   
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
from view.teacher.classes_view import ClassesView
from view.teacher.schedule_view import ScheduleView
from view.teacher.subjects_taught_view import SubjectsTaughtView


def main(page: ft.Page):
    page.title = "Sistema Escolar"
    page.window_width = 1100
    page.window_height = 700
    page.scroll = "auto"

    create_tables_and_seed()

    state = {"user": None, "user_id": None, "role": None, "route": "dashboard"}

    permissions = {
        "admin": {"dashboard", "usuarios", "professores", "disciplinas", "turmas", "alunos", "documentos", "comunicados", "calendario", "frequencia", "notas"},
        "secretaria": {"dashboard", "alunos", "turmas", "documentos", "comunicados", "calendario", "disciplinas"},
        "professor": {"dashboard", "frequencia", "notas", "comunicados", "minhas_turmas", "horario", "minhas_disciplinas"},
        # aluno: apenas desempenho, boletim e horario
        "aluno": {"desempenho", "boletim", "horario"},
        "responsavel": {"dashboard", "comunicados", "calendario"},
        "suporte": {"dashboard"},
    }

    def build_content():
        # retorna um control (container) conforme state["route"]
        r = state.get("route", "dashboard")
        role = state.get("role")
        print(f"[BUILD_CONTENT] route={r} role={role}")
        try:
            if r == "dashboard":
                return DashboardView(page, role=role, username=state.get("user"), go=go)
            if r == "usuarios":
                # passa o usuário logado para que ele não possa rebaixar a si mesmo
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
                return ComunicadoView(page)
            if r == "documentos":
                return DocumentoView(page)
            if r == "calendario":
                return CalendarioView(page)
            # fallback
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
        # atualiza estado se fornecido
        if user is not None:
            state["user"] = user
        if role is not None:
            state["role"] = role
        if user_id is not None:
            state["user_id"] = user_id

        # define rota padrão ao entrar na home: aluno -> desempenho, outros -> dashboard
        if view == "home" and not state.get("route"):
            if state.get("role") == "aluno":
                state["route"] = "desempenho"
            else:
                state["route"] = "dashboard"
        
        # limpa views e decide o que construir
        page.views.clear()

        # login view
        if view == "login":
            page.views.append(LoginView(page, go))
            # prepara rota padrão (apenas se não houver)
            if not state.get("route"):
                state["route"] = "dashboard"
            page.update()
            return

        # home / shell
        if view == "home":
            # Não sobrescrever state['route'] aqui — usa o valor que foi definido por on_route_change.
            # Garante uma rota padrão apenas se ainda não foi definida
            if not state.get("route"):
                state["route"] = "dashboard"

            def on_route_change(new_route: str):
                if new_route == "logout":
                    state["user"] = None
                    state["user_id"] = None
                    state["role"] = None
                    go("login")
                    return
                allowed = permissions.get(state.get("role", "aluno"), {"dashboard"})
                # só altera a rota se permitido
                if new_route not in allowed:
                    state["route"] = "dashboard"
                else:
                    state["route"] = new_route
                # reconstrói a home com a nova rota (não resetará para dashboard)
                go("home")

            # constroi shell com content builder
            try:
                page.views.append(
                    Shell(
                        page,
                        username=state.get("user") or "Usuário",
                        role=state.get("role") or "aluno",
                        on_route_change=on_route_change,
                        content_builder=build_content,
                    ).build()
                )
            except Exception as ex:
                page.views.append(ft.View("/error", controls=[ft.Column([ft.Text("Erro interno:"), ft.Text(str(ex))])]))

            # processa pedidos de navegação gerados por shortcuts (Dashboard)
            try:
                go_to = page.client_storage.get("go_to")
                if go_to:
                    page.client_storage.set("go_to", None)
                    on_route_change(go_to)
            except Exception:
                pass

            page.update()
            return

        # se solicitar qualquer outra view diretamente, tenta abrir home e ajustar rota
        state["route"] = view
        go("home")

    # inicia com login se não houver user, ou com home se AUTO_LOGIN
    if os.environ.get("AUTO_LOGIN") == "1":
        go("home", user="admin", role="admin", user_id=1)
    else:
        go("login")


if __name__ == "__main__":
    ft.app(target=main)
