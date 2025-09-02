import re
import flet as ft

try:
    from services.turma_service import list_turmas, get_turma, create_turma, update_turma, delete_turma
except Exception:
    from services.turma_service import get_all as list_turmas  # type: ignore
    get_turma = lambda _id: None  # type: ignore
    create_turma = lambda **kw: None  # type: ignore
    update_turma = lambda _id, **kw: None  # type: ignore
    delete_turma = lambda _id: None  # type: ignore

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
