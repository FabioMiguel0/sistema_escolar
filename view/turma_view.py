import re
import flet as ft
from importlib import import_module

# tenta carregar o módulo de serviço de forma resiliente
_turma_mod = None
try:
    _turma_mod = import_module("services.turma_service")
except Exception:
    _turma_mod = None

def _get_attr(names, default=None):
    if _turma_mod is None:
        return default
    for n in names:
        if hasattr(_turma_mod, n):
            return getattr(_turma_mod, n)
    return default

# mapear nomes comuns usados pelas views
list_turmas = _get_attr(["list_turmas", "get_all", "get_all_turmas", "list_all", "all_turmas"])
get_turma = _get_attr(["get_turma", "get_by_id", "get_turma_by_id", "get"])
create_turma = _get_attr(["create_turma", "create", "add_turma", "insert_turma"])
update_turma = _get_attr(["update_turma", "update", "edit_turma", "modify_turma"])
delete_turma = _get_attr(["delete_turma", "delete", "remove_turma"])

# helpers que geram erro claro quando funções não existem
def _missing(name):
    def _f(*a, **k):
        raise ImportError(f"services.turma_service não fornece '{name}'. Verifique services/turma_service.py ou adapte os nomes.")
    return _f

if list_turmas is None:
    list_turmas = _missing("list_turmas / get_all / get_all_turmas")
if get_turma is None:
    get_turma = _missing("get_turma / get_by_id")
if create_turma is None:
    create_turma = _missing("create_turma / create")
if update_turma is None:
    update_turma = _missing("update_turma / update")
if delete_turma is None:
    delete_turma = _missing("delete_turma / delete")

def TurmaView(page: ft.Page, role="admin", current_user_id=None, go=None):
    page.auto_scroll = True

    nome = ft.TextField(label="Nome", width=320)
    periodo = ft.Dropdown(label="Período", width=180, options=[ft.dropdown.Option("Manhã"), ft.dropdown.Option("Tarde"), ft.dropdown.Option("Noite")], value="Manhã")
    ano = ft.TextField(label="Ano Letivo", width=140)

    list_container = ft.Container(expand=True)

    def _show(m):
        page.snack_bar = ft.SnackBar(ft.Text(m)); page.snack_bar.open = True; page.update()

    def build_list():
        try:
            w = page.window_width or (page.client_size.width if hasattr(page, "client_size") else 1000)
        except Exception:
            w = 1000
        w = w or 1000

        turmas = list_turmas() or []

        if w >= 700:
            cols = [ft.DataColumn(ft.Text("ID")), ft.DataColumn(ft.Text("Nome")), ft.DataColumn(ft.Text("Período")), ft.DataColumn(ft.Text("Ano")), ft.DataColumn(ft.Text("Ações"))]
            rows = []
            for t in turmas:
                tid = t.get("id") if isinstance(t, dict) else (t[0] if isinstance(t, (list, tuple)) else getattr(t, "id", ""))
                name = t.get("nome") if isinstance(t, dict) else (t[1] if isinstance(t, (list, tuple)) and len(t) > 1 else getattr(t, "nome", ""))
                per = t.get("periodo", "") if isinstance(t, dict) else getattr(t, "periodo", "")
                ano_val = t.get("ano_letivo", "") if isinstance(t, dict) else getattr(t, "ano_letivo", "")
                edit_btn = ft.IconButton(ft.icons.EDIT, on_click=lambda e, tid_local=tid: on_edit(tid_local))
                del_btn = ft.IconButton(ft.icons.DELETE, on_click=lambda e, tid_local=tid: on_delete(tid_local))
                rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(tid))),
                    ft.DataCell(ft.Text(str(name), selectable=True)),
                    ft.DataCell(ft.Text(str(per))),
                    ft.DataCell(ft.Text(str(ano_val))),
                    ft.DataCell(ft.Row([edit_btn, del_btn]))
                ]))
            return ft.Container(content=ft.DataTable(columns=cols, rows=rows, heading_text_style=ft.TextStyle(weight="bold")), expand=True, padding=8)
        else:
            cards = []
            for t in turmas:
                tid = t.get("id") if isinstance(t, dict) else (t[0] if isinstance(t, (list, tuple)) else getattr(t, "id", ""))
                name = t.get("nome") if isinstance(t, dict) else (t[1] if isinstance(t, (list, tuple)) and len(t) > 1 else getattr(t, "nome", ""))
                per = t.get("periodo", "") if isinstance(t, dict) else getattr(t, "periodo", "")
                ano_val = t.get("ano_letivo", "") if isinstance(t, dict) else getattr(t, "ano_letivo", "")
                edit_btn = ft.IconButton(ft.icons.EDIT, on_click=lambda e, tid_local=tid: on_edit(tid_local))
                del_btn = ft.IconButton(ft.icons.DELETE, on_click=lambda e, tid_local=tid: on_delete(tid_local))
                card = ft.Card(content=ft.Container(content=ft.Column([
                    ft.Text(str(name), weight="bold"),
                    ft.Text(f"Período: {per}"),
                    ft.Text(f"Ano: {ano_val}"),
                    ft.Row([edit_btn, del_btn], alignment="end")
                ], spacing=6), padding=10))
                cards.append(card)
            return ft.Container(content=ft.Column(cards), expand=True, padding=6)

    def load_list(e=None):
        list_container.content = build_list()
        page.update()

    def on_add(e):
        try:
            create_turma(nome=nome.value.strip(), periodo=periodo.value, ano_letivo=ano.value.strip() if ano.value else None)
            nome.value = ano.value = ""
            periodo.value = "Manhã"
            load_list()
        except Exception as ex:
            _show(f"Erro: {ex}")

    def on_edit(tid):
        t = get_turma(tid)
        if not t:
            _show("Turma não encontrada"); return
        nome.value = t.get("nome") if isinstance(t, dict) else getattr(t, "nome", "")
        periodo.value = t.get("periodo", "Manhã") if isinstance(t, dict) else getattr(t, "periodo", "Manhã")
        ano.value = t.get("ano_letivo", "") if isinstance(t, dict) else getattr(t, "ano_letivo", "")
        page.update()

    def on_delete(tid):
        delete_turma(tid)
        load_list()

    try:
        page.on_resize = lambda e: load_list()
    except Exception:
        pass

    form = ft.Column([ft.Row([nome, periodo, ano]), ft.Row([ft.ElevatedButton("Adicionar", on_click=on_add)])], tight=True)
    container = ft.Container(content=ft.Column([ft.Text("Gestão de Turmas", size=18), form, ft.Divider(), list_container]), expand=True)
    load_list()
    return container
