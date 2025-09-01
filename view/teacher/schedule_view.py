import flet as ft

def ScheduleView(page: ft.Page, role=None, current_user_id=None):
    page.auto_scroll = True
    # placeholder: projetado para usar um serviço de horário quando existir
    title = ft.Text("Horário", size=18, weight="bold")
    body = ft.Column([ft.Text("Horário do professor (placeholder).")])
    return ft.Container(content=ft.Column([title, ft.Divider(), body]), expand=True, padding=12)