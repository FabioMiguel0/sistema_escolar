import re
import flet as ft
from services.aluno_service import get_all, create, update, delete, assign_turma, get
from services.turma_service import list_turmas
from services.permission_service import has_permission

# validações
NAME_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'\-]+$")
def _valid_name(s: str) -> bool:
    return bool(s and NAME_RE.match(s.strip()))

def _valid_digits(s: str) -> bool:
    return bool(s and s.isdigit())

def _valid_bi(s: str) -> bool:
    return bool(s and re.fullmatch(r"[A-Za-z0-9]{14}", s.strip()))

def _valid_phone(s: str) -> bool:
    return bool(s and re.fullmatch(r"\d{9}", s.strip()))

def _sanitize_name_input(s: str) -> str:
    return re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ\s'\-]", "", s or "")

def _sanitize_digits_input(s: str) -> str:
    return re.sub(r"[^\d]", "", s or "")

def AlunoView(page: ft.Page, role="aluno", current_user_id=None, go=None):
    page.auto_scroll = True

    nome = ft.TextField(label="Nome", width=360)
    bi_field = ft.TextField(label="Nº BI", width=200, max_length=14, tooltip="14 caracteres alfanuméricos")
    matricula = ft.TextField(label="Matrícula", width=200)
    nome_pai = ft.TextField(label="Nome do Pai", width=360)
    nome_mae = ft.TextField(label="Nome da Mãe", width=360)
    idade = ft.TextField(label="Idade", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    localidade = ft.TextField(label="Localidade", width=240)
    numero_casa = ft.TextField(label="Número da Casa", width=160, keyboard_type=ft.KeyboardType.NUMBER)
    periodo = ft.Dropdown(label="Período", width=200, options=[ft.dropdown.Option("Manhã", text="Manhã"), ft.dropdown.Option("Tarde", text="Tarde"), ft.dropdown.Option("Noite", text="Noite")], value="Manhã")
    ano_letivo = ft.TextField(label="Ano Letivo", width=140)
    telefone = ft.TextField(label="Telefone", width=160, max_length=9, keyboard_type=ft.KeyboardType.NUMBER, tooltip="9 dígitos")

    turma_options = [ft.dropdown.Option("", text="-- sem turma --")]
    turma_options += [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in list_turmas()]
    turma_dropdown = ft.Dropdown(label="Turma (nova matrícula)", width=240, options=turma_options, value="")

    list_container = ft.Container(expand=True)

    def can_manage_students():
        if role == "admin":
            return True
        if role == "secretaria":
            return has_permission(current_user_id, "matricular")
        return False

    def _show_error(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg)); page.snack_bar.open = True; page.update()

    # input sanitizers
    def on_name_change(e):
        v = _sanitize_name_input(nome.value)
        if v != nome.value:
            nome.value = v; page.update()

    def on_nome_pai_change(e):
        v = _sanitize_name_input(nome_pai.value)
        if v != nome_pai.value:
            nome_pai.value = v; page.update()

    def on_nome_mae_change(e):
        v = _sanitize_name_input(nome_mae.value)
        if v != nome_mae.value:
            nome_mae.value = v; page.update()

    def on_idade_change(e):
        v = _sanitize_digits_input(idade.value)
        if v != idade.value:
            idade.value = v; page.update()

    def on_numero_casa_change(e):
        v = _sanitize_digits_input(numero_casa.value)
        if v != numero_casa.value:
            numero_casa.value = v; page.update()

    def on_telefone_change(e):
        v = _sanitize_digits_input(telefone.value)[:9]
        if v != telefone.value:
            telefone.value = v; page.update()

    def on_bi_change(e):
        v = re.sub(r"[^A-Za-z0-9]", "", bi_field.value or "")[:14]
        if v != bi_field.value:
            bi_field.value = v; page.update()

    nome.on_change = on_name_change
    nome_pai.on_change = on_nome_pai_change
    nome_mae.on_change = on_nome_mae_change
    idade.on_change = on_idade_change
    numero_casa.on_change = on_numero_casa_change
    telefone.on_change = on_telefone_change
    bi_field.on_change = on_bi_change

    # ações CRUD
    def _validate_all_fields():
        if not _valid_name(nome.value):
            return False, "Nome inválido (apenas letras, espaços, - e ')."
        if nome_pai.value and not _valid_name(nome_pai.value):
            return False, "Nome do pai inválido."
        if nome_mae.value and not _valid_name(nome_mae.value):
            return False, "Nome da mãe inválido."
        if idade.value and not _valid_digits(idade.value):
            return False, "Idade deve conter apenas números."
        if idade.value:
            iv = int(idade.value)
            if iv < 0 or iv > 120:
                return False, "Idade fora do intervalo válido."
        if numero_casa.value and not _valid_digits(numero_casa.value):
            return False, "Número da casa deve conter apenas dígitos."
        if bi_field.value and not _valid_bi(bi_field.value):
            return False, "BI inválido: deve ter exatamente 14 caracteres alfanuméricos."
        if telefone.value and not _valid_phone(telefone.value):
            return False, "Telefone inválido: deve ter exatamente 9 dígitos."
        return True, None

    def on_add(e):
        if not can_manage_students():
            _show_error("Sem permissão para cadastrar alunos"); return
        ok, msg = _validate_all_fields()
        if not ok:
            _show_error(msg); return

        tval = turma_dropdown.value
        turma_id = int(tval) if tval and str(tval).isdigit() else None
        idade_val = int(idade.value) if idade.value and idade.value.isdigit() else None

        try:
            create(
                nome=nome.value.strip(),
                matricula=matricula.value.strip() if matricula.value else None,
                turma_id=turma_id,
                bi=bi_field.value.strip() if bi_field.value else None,
                nome_pai=nome_pai.value.strip() if nome_pai.value else None,
                nome_mae=nome_mae.value.strip() if nome_mae.value else None,
                idade=idade_val,
                localidade=localidade.value.strip() if localidade.value else None,
                numero_casa=numero_casa.value.strip() if numero_casa.value else None,
                periodo=periodo.value if periodo.value else None,
                ano_letivo=ano_letivo.value.strip() if ano_letivo.value else None,
                telefone=telefone.value.strip() if telefone.value else None,
            )
        except Exception as ex:
            _show_error(f"Erro ao salvar no banco: {ex}"); return

        nome.value = bi_field.value = matricula.value = nome_pai.value = nome_mae.value = idade.value = localidade.value = numero_casa.value = ano_letivo.value = telefone.value = ""
        periodo.value = "Manhã"
        turma_dropdown.value = ""
        page.update()
        load_list()

    save_btn = ft.ElevatedButton("Salvar", on_click=lambda e: None, visible=False)  # placeholder
    add_btn = ft.ElevatedButton("Adicionar", on_click=on_add, disabled=not can_manage_students())

    form = ft.Column([
        ft.Row([nome, bi_field]),
        ft.Row([matricula, turma_dropdown]),
        ft.Row([nome_pai, nome_mae]),
        ft.Row([idade, localidade, numero_casa]),
        ft.Row([periodo, ano_letivo, telefone]),
        ft.Row([add_btn, save_btn])
    ], tight=True)

    # função que constrói a listagem de forma responsiva
    def build_list_view():
        width = None
        try:
            width = page.window_width or (page.client_size.width if hasattr(page, "client_size") else None)
        except Exception:
            width = 1000
        width = width or 1000

        students = get_all()
        turmas = {str(t["id"]): t["nome"] for t in list_turmas()}

        if width >= 700:
            # DataTable para desktop/tablet largo
            columns = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("BI")),
                ft.DataColumn(ft.Text("Matrícula")),
                ft.DataColumn(ft.Text("Telefone")),
                ft.DataColumn(ft.Text("Turma")),
                ft.DataColumn(ft.Text("Ações")),
            ]
            rows = []
            for a in students:
                aid = a["id"]
                current_turma = str(a.get("turma_id")) if a.get("turma_id") else ""
                # ações
                edit_btn = ft.IconButton(ft.icons.EDIT, on_click=lambda e, aid_local=aid: on_edit(aid_local))
                delete_btn = ft.IconButton(ft.icons.DELETE, on_click=lambda e, aid_local=aid: on_delete(aid_local))
                # matricular dropdown + button
                row_turma_dd = ft.Dropdown(options=[ft.dropdown.Option("", text="-- sem turma --")] + [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in list_turmas()], value=current_turma, width=160)
                mat_btn = ft.ElevatedButton("Matricular", on_click=lambda e, aid_local=aid, dd=row_turma_dd: on_matricular(aid_local, dd), width=110)
                mat_btn.disabled = not can_manage_students()

                actions_cell = ft.Row([row_turma_dd, mat_btn, edit_btn, delete_btn], spacing=6)
                rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(aid))),
                    ft.DataCell(ft.Text(a.get("nome") or "", selectable=True)),
                    ft.DataCell(ft.Text(a.get("bi") or "")),
                    ft.DataCell(ft.Text(a.get("matricula") or "")),
                    ft.DataCell(ft.Text(a.get("telefone") or "")),
                    ft.DataCell(ft.Text(turmas.get(current_turma, "--"))),
                    ft.DataCell(actions_cell),
                ]))
            data_table = ft.DataTable(columns=columns, rows=rows, heading_text_style=ft.TextStyle(weight="bold"))
            return ft.Container(content=data_table, expand=True, padding=6)

        else:
            # mobile: lista vertical com cartões (cada cartão com campos principais e ações)
            cards = []
            for a in students:
                aid = a["id"]
                current_turma = str(a.get("turma_id")) if a.get("turma_id") else ""
                turmaname = turmas.get(current_turma, "--")
                edit_btn = ft.IconButton(ft.icons.EDIT, on_click=lambda e, aid_local=aid: on_edit(aid_local))
                delete_btn = ft.IconButton(ft.icons.DELETE, on_click=lambda e, aid_local=aid: on_delete(aid_local))
                row_turma_dd = ft.Dropdown(options=[ft.dropdown.Option("", text="-- sem turma --")] + [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in list_turmas()], value=current_turma, width=160)
                mat_btn = ft.ElevatedButton("Matricular", on_click=lambda e, aid_local=aid, dd=row_turma_dd: on_matricular(aid_local, dd), width=100)
                mat_btn.disabled = not can_manage_students()

                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Text(f"{a.get('nome') or ''}", weight="bold")]),
                            ft.Row([ft.Text(f"BI: {a.get('bi') or '--'}"), ft.Text(f"Matrícula: {a.get('matricula') or '--'}")]),
                            ft.Row([ft.Text(f"Telefone: {a.get('telefone') or '--'}"), ft.Text(f"Turma: {turmaname}")]),
                            ft.Row([row_turma_dd, mat_btn, edit_btn, delete_btn], alignment="spaceBetween")
                        ], spacing=6),
                        padding=10
                    ), margin=ft.margin.symmetric(vertical=6, horizontal=4)
                )
                cards.append(card)
            return ft.Container(content=ft.Column(cards), expand=True, padding=6)

    # load/refresh
    def load_list(e: ft.ControlEvent = None):
        list_container.content = build_list_view()
        page.update()

    # CRUD helpers reuse earlier logic
    def on_edit(aid):
        a = get(aid)
        if not a: return
        nome.value = a.get("nome") or ""
        matricula.value = a.get("matricula") or ""
        turma_dropdown.value = str(a.get("turma_id")) if a.get("turma_id") else ""
        bi_field.value = a.get("bi") or ""
        nome_pai.value = a.get("nome_pai") or ""
        nome_mae.value = a.get("nome_mae") or ""
        idade.value = str(a.get("idade")) if a.get("idade") is not None else ""
        localidade.value = a.get("localidade") or ""
        numero_casa.value = a.get("numero_casa") or ""
        periodo.value = a.get("periodo") or "Manhã"
        ano_letivo.value = a.get("ano_letivo") or ""
        telefone.value = a.get("telefone") or ""
        page.update()

    def on_save(e):
        # implement if you use save flow
        pass

    def on_delete(aid):
        delete(aid)
        load_list()

    def on_matricular(aid, dd):
        if not can_manage_students():
            _show_error("Sem permissão para matricular alunos"); return
        val = dd.value
        turma_id = int(val) if val and str(val).isdigit() else None
        assign_turma(aid, turma_id)
        page.snack_bar = ft.SnackBar(ft.Text("Matrícula atualizada")); page.snack_bar.open = True
        page.update()
        load_list()

    # atualizar na criação e ao redimensionar
    try:
        page.on_resize = lambda e: load_list()
    except Exception:
        pass

    container = ft.Container(content=ft.Column([ft.Text("Cadastro de Alunos", size=18), form, ft.Divider(), list_container]), expand=True)
    load_list()
    return container
