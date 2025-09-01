import flet as ft

PRIMARY_COLOR = "#1976D2"
PRIMARY_COLOR_DARK = "#1559a8"
BACKGROUND_COLOR = "#F4F6F8"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#0F172A"

def titulo(texto): return ft.Text(texto, size=22, weight="bold", color=TEXT_COLOR)
def subtitulo(texto): return ft.Text(texto, size=14, color="#64748B")

def card_metric(titulo: str, valor: str, icon):
    return ft.Container(
        bgcolor=CARD_COLOR, border_radius=16, padding=16,
        shadow=ft.BoxShadow(blur_radius=14, color="#00000010"),
        content=ft.Column([
            ft.Icon(icon, size=28, color=PRIMARY_COLOR),
            ft.Text(valor, size=26, weight="w700", color=TEXT_COLOR),
            ft.Text(titulo, size=12, color="#64748B"),
        ], spacing=6)
    )
