import flet as ft
import datetime
from services.comunicado_service import list_comunicados, create

def ComunicadoView(page: ft.Page):
    titulo = ft.TextField(label="Título", width=360)
    texto = ft.TextField(label="Texto", width=720, multiline=True, height=120)
    list_view = ft.ListView(expand=True, spacing=8, padding=8)

    def load():
        list_view.controls.clear()
        for c in list_comunicados():
            row = ft.Column([ft.Text(c["titulo"], weight="bold"), ft.Text(c["texto"]), ft.Divider()])
            list_view.controls.append(row)
        page.update()

    def on_add(e):
        create(titulo.value or "Sem título", texto.value or "", str(datetime.date.today()))
        titulo.value = ""; texto.value = ""
        load()

    add_btn = ft.ElevatedButton("Publicar", on_click=on_add)
    container = ft.Container(content=ft.Column([ft.Text("Comunicados", size=18), ft.Row([titulo, add_btn]), texto, ft.Divider(), list_view]), expand=True)
    load()
    return container
