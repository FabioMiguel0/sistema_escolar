import flet as ft
from services.aluno_service import get_all
from services.frequencia_service import registrar, listar
import datetime


def FrequenciaView(page: ft.Page):
    alunos = get_all()
    aluno_options = [ft.dropdown.Option(str(a["id"]), text=a["nome"]) for a in alunos]
    aluno_dd = ft.Dropdown(
        label="Aluno",
        options=aluno_options,
        value=aluno_options[0].value if aluno_options else None,
    )
    data_field = ft.DatePicker(value=datetime.date.today())
    presente_cb = ft.Checkbox(label="Presente", value=True)
    list_view = ft.ListView(expand=True, spacing=6, padding=6)

    def load():
        list_view.controls.clear()
        for f in listar(aluno_id=int(aluno_dd.value) if aluno_dd.value else None):
            list_view.controls.append(
                ft.Row(
                    [
                        ft.Text(f["data"]),
                        ft.Text("Presente" if f["presente"] else "Faltou"),
                    ]
                )
            )
        page.update()

    def on_reg(e):
        if not aluno_dd.value:
            return
        registrar(int(aluno_dd.value), str(data_field.value), presente_cb.value)
        load()

    reg_btn = ft.ElevatedButton("Registrar", on_click=on_reg)
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Frequência", size=18),
                ft.Row([aluno_dd, data_field, presente_cb, reg_btn]),
                ft.Divider(),
                list_view,
            ]
        ),
        expand=True,
    )
    load()
    return container


