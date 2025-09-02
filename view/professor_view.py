import re
import flet as ft

# tenta vários nomes de serviço compatíveis
try:
    from services.professor_service import list_professores, get_professor, create_professor, update_professor, delete_professor
except Exception:
    # fallback para compatibilidade com implementações variadas
    from services.professor_service import get_all as list_professores  # type: ignore
    get_professor = lambda _id: None  # type: ignore
    create_professor = lambda **kw: None  # type: ignore
    update_professor = lambda _id, **kw: None  # type: ignore
    delete_professor = lambda _id: None  # type: ignore

NAME_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'\-]+$")

def _sanitize_name(s: str) -> str:
    return re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ\s'\-]", "", s or "")

def ProfessorView(page: ft.Page, role="professor", current_user_id=None, go=None):
    page.auto_scroll = True

    nome = ft.TextField(label="Nome", width=360)
    email = ft.TextField(label="E-mail", width=320)
    telefone = ft.TextField(label="Telefone", width=160, max_length=9)
    disciplina = ft.TextField(label="Disciplina principal", width=300)

    list_container = ft.Container(expand=True)

    def _show_msg(m):
        page.snack_bar = ft.SnackBar(ft.Text(m)); page.snack_bar.open = True; page.update()

    # sanitizers
    nome.on_change = lambda e: (nome.__setattr__("value", _sanitize_name(nome.value)) or page.update()) if nome.value and _sanitize_name(nome.value) != nome.value else None

    def can_manage():
        return role == "admin"

    # build responsive list
    def build_list():
        try:
            w = page.window_width or (page.client_size.width if hasattr(page, "client_size") else 1000)
        except Exception:
            w = 1000
        w = w or 1000

        profs = list_professores() or []

        if w >= 700:
            cols = [ft.DataColumn(ft.Text("ID")), ft.DataColumn(ft.Text("Nome")), ft.DataColumn(ft.Text("E-mail")), ft.DataColumn(ft.Text("Telefone")), ft.DataColumn(ft.Text("Disciplina")), ft.DataColumn(ft.Text("Ações"))]
            rows = []
            for p in profs:
                pid = p.get("id") if isinstance(p, dict) else (p[0] if isinstance(p, (list, tuple)) else getattr(p, "id", ""))
                name = p.get("nome") if isinstance(p, dict) else (p[1] if isinstance(p, (list, tuple)) and len(p) > 1 else getattr(p, "nome", ""))
                mail = p.get("email", "") if isinstance(p, dict) else getattr(p, "email", "")
                phone = p.get("telefone", "") if isinstance(p, dict) else getattr(p, "telefone", "")
                subj = p.get("disciplina", "") if isinstance(p, dict) else getattr(p, "disciplina", "")
                edit_btn = ft.IconButton(ft.icons.EDIT, on_click=lambda e, pid_local=pid: on_edit(pid_local))
                del_btn = ft.IconButton(ft.icons.DELETE, on_click=lambda e, pid_local=pid: on_delete(pid_local))
                actions = ft.Row([edit_btn, del_btn])
                rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(pid))),
                    ft.DataCell(ft.Text(str(name), selectable=True)),
                    ft.DataCell(ft.Text(str(mail))),
                    ft.DataCell(ft.Text(str(phone))),
                    ft.DataCell(ft.Text(str(subj))),
                    ft.DataCell(actions),
                ]))
            return ft.Container(content=ft.DataTable(columns=cols, rows=rows, heading_text_style=ft.TextStyle(weight="bold")), expand=True, padding=8)
        else:
            cards = []
            for p in profs:
                pid = p.get("id") if isinstance(p, dict) else (p[0] if isinstance(p, (list, tuple)) else getattr(p, "id", ""))
                name = p.get("nome") if isinstance(p, dict) else (p[1] if isinstance(p, (list, tuple)) and len(p) > 1 else getattr(p, "nome", ""))
                mail = p.get("email", "") if isinstance(p, dict) else getattr(p, "email", "")
                phone = p.get("telefone", "") if isinstance(p, dict) else getattr(p, "telefone", "")
                subj = p.get("disciplina", "") if isinstance(p, dict) else getattr(p, "disciplina", "")
                edit_btn = ft.IconButton(ft.icons.EDIT, on_click=lambda e, pid_local=pid: on_edit(pid_local))
                del_btn = ft.IconButton(ft.icons.DELETE, on_click=lambda e, pid_local=pid: on_delete(pid_local))
                card = ft.Card(content=ft.Container(content=ft.Column([
                    ft.Text(str(name), weight="bold"),
                    ft.Text(f"E-mail: {mail}"),
                    ft.Text(f"Telefone: {phone}"),
                    ft.Text(f"Disciplina: {subj}"),
                    ft.Row([edit_btn, del_btn], alignment="end")
                ], spacing=6), padding=10))
                cards.append(card)
            return ft.Container(content=ft.Column(cards), expand=True, padding=6)

    def load_list(e=None):
        list_container.content = build_list()
        page.update()

    def on_add(e):
        if not can_manage():
            _show_msg("Sem permissão")
            return
        try:
            create_professor(nome=nome.value.strip(), email=email.value.strip() if email.value else None, telefone=telefone.value.strip() if telefone.value else None, disciplina=disciplina.value.strip() if disciplina.value else None)
            nome.value = email.value = telefone.value = disciplina.value = ""
            load_list()
        except Exception as ex:
            _show_msg(f"Erro: {ex}")

    def on_edit(pid):
        p = get_professor(pid)
        if not p:
            _show_msg("Professor não encontrado"); return
        nome.value = p.get("nome") if isinstance(p, dict) else getattr(p, "nome", "")
        email.value = p.get("email", "") if isinstance(p, dict) else getattr(p, "email", "")
        telefone.value = p.get("telefone", "") if isinstance(p, dict) else getattr(p, "telefone", "")
        disciplina.value = p.get("disciplina", "") if isinstance(p, dict) else getattr(p, "disciplina", "")
        page.update()

    def on_delete(pid):
        delete_professor(pid)
        load_list()

    try:
        page.on_resize = lambda e: load_list()
    except Exception:
        pass

    form = ft.Column([ft.Row([nome, email, telefone]), ft.Row([disciplina, ft.ElevatedButton("Adicionar", on_click=on_add) if can_manage() else ft.Text("")])], tight=True)
    container = ft.Container(content=ft.Column([ft.Text("Professores", size=18), form, ft.Divider(), list_container]), expand=True)
    load_list()
    return container
