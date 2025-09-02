import flet as ft

def LoginView(page: ft.Page, go):
    page.auto_scroll = True
    user_field = ft.TextField(label="Usuário")
    pwd_field = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    msg = ft.Text("")

    def on_login(e):
        username = (user_field.value or "").strip()
        # autenticação de teste: ajusta para usar user_service se desejar
        if username == "aluno":
            go("dashboard", user=username, role="aluno", user_id=2)
        elif username == "professor":
            go("dashboard", user=username, role="professor", user_id=3)
        elif username == "admin":
            go("dashboard", user=username, role="admin", user_id=1)
        else:
            msg.value = "Credenciais inválidas (use aluno/professor/admin)"
            page.update()

    login_btn = ft.ElevatedButton("Entrar", on_click=on_login)
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Login", size=20, weight="bold"),
                user_field,
                pwd_field,
                login_btn,
                msg,
            ],
            spacing=8,
        ),
        padding=20,
        width=360,
    )
    return container