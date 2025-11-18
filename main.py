import flet as ft


def converter_decimal_para_base(numero, base):
    """
    CENÁRIO 1: Decimal -> Base X
    Método: Divisões Sucessivas (Escada).
    """
    if numero == 0:
        return "0", ["O número já é 0."]

    digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    resultado = ""
    passos = []

    numero_abs = abs(numero)
    if numero < 0:
        passos.append(
            f"Calculando com o valor absoluto: |{numero}| = {numero_abs}"
        )

    temp_num = numero_abs
    while temp_num > 0:
        resto = temp_num % base
        quociente = temp_num // base
        passos.append(
            f"{temp_num} ÷ {base} = {quociente} "
            f"(resto {resto} -> '{digitos[resto]}')"
        )
        resultado = digitos[resto] + resultado
        temp_num = quociente

    passos.append(
        f"\nLendo os restos de baixo para cima, o resultado é: {resultado}"
    )

    if numero < 0:
        resultado = "-" + resultado
        passos.append(f"Adicionando o sinal negativo de volta: {resultado}")

    return resultado, passos


def converter_base_para_decimal(numero_str, base_origem):
    """
    CENÁRIO 2: Base X -> Decimal
    Método: Notação Posicional (Soma de Potências).
    """
    digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numero_str = numero_str.upper()
    decimal_final = 0
    tamanho = len(numero_str)
    passos = []
    passos_soma = []

    for i, digito_char in enumerate(numero_str):
        expoente = (tamanho - 1) - i
        valor_digito = digitos.index(digito_char)

        if valor_digito >= base_origem:
            raise ValueError(
                f"Dígito '{digito_char}' inválido para a base {base_origem}"
            )

        termo = valor_digito * (base_origem**expoente)
        decimal_final += termo
        passos.append(
            f"Dígito '{digito_char}' (valor {valor_digito}) "
            f"na posição {i} (expoente {expoente}): "
            f"{valor_digito} × {base_origem}^{expoente} = {termo}"
        )
        passos_soma.append(str(termo))

    if len(passos_soma) > 1:
        passos.append(
            f"\nSomando os termos: {' + '.join(passos_soma)} = {decimal_final}"
        )

    passos.append(f"O resultado final em decimal é: {decimal_final}")

    return decimal_final, passos


def main(page: ft.Page):
    page.title = "Conversor de Bases Numéricas e Aritmética Binária"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Substituir a linha window_full_screen por estas dimensões ergonómicas:
    page.window_width = 1280
    page.window_height = 1000
    page.window_resizable = True  # Deixar o utilizador ajustar se quiser
    
    page.window_icon = "circuito.png"

    # --- Pop-up "Sobre" ---
    def abrir_dialogo_sobre(e):
        def fechar_dialogo(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sobre o App"),
            content=ft.Text(
                "Este é um aplicativo para conversão de bases numéricas e "
                "realização de operações de aritmética binária."
            ),
            actions=[
                ft.TextButton("Fechar", on_click=fechar_dialogo),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    def fechar_banner(e):
        page.banner.open = False
        page.update()

    page.banner = ft.Banner(
        bgcolor=ft.Colors.AMBER_100,
        leading=ft.Icon(
            ft.Icons.WARNING_AMBER_ROUNDED, color="amber", size=40
        ),
        content=ft.Text(""),
        actions=[
            ft.TextButton("Fechar", on_click=fechar_banner),
        ],
    )

    def mostrar_erro(mensagem):
        page.banner.content.value = mensagem
        page.banner.open = True
        page.update()

    def fechar_janela(e):
        page.window_close()

    # --- Lógica de Conversão de Bases ---
    def calcular_conversao(e):
        coluna_passos_conversao.controls.clear()
        coluna_passos_conversao.controls.append(
            ft.Text("Como o cálculo foi feito:",
                    weight=ft.FontWeight.BOLD, size=16)
        )
        coluna_passos_conversao.controls.append(
            ft.Divider(height=5, color="transparent")
        )

        try:
            base_origem = int(dd_base_origem.value)
            base_destino = int(dd_base_destino.value)
            numero_str = txt_numero_converter.value
            passos = []

            if not numero_str:
                mostrar_erro("Por favor, digite um número.")
                return

            if base_origem == base_destino:
                resultado_final = numero_str
                passos.append(
                    f"A base de origem e destino são as mesmas ({base_origem})."
                )
                passos.append("Nenhuma conversão é necessária.")

            elif base_origem == 10:
                numero_int = int(numero_str)
                resultado_final, passos = converter_decimal_para_base(
                    numero_int, base_destino
                )
            elif base_destino == 10:
                resultado_final_int, passos = converter_base_para_decimal(
                    numero_str, base_origem
                )
                resultado_final = str(resultado_final_int)
            else:
                passos.append(
                    ft.Text(
                        f"Passo 1: Converter de Base {base_origem} para "
                        "Decimal (Base 10)",
                        weight=ft.FontWeight.BOLD
                    )
                )
                decimal_intermediario, passos_pt1 = converter_base_para_decimal(
                    numero_str, base_origem
                )
                passos.extend(passos_pt1)

                passos.append(
                    ft.Text(
                        f"\nPasso 2: Converter de Decimal (Base 10) para "
                        f"Base {base_destino}",
                        weight=ft.FontWeight.BOLD
                    )
                )
                resultado_final, passos_pt2 = converter_decimal_para_base(
                    decimal_intermediario, base_destino
                )
                passos.extend(passos_pt2)

            txt_resultado_conversao.value = resultado_final
            txt_resultado_conversao.error_text = None

            for passo in passos:
                if isinstance(passo, str):
                    coluna_passos_conversao.controls.append(
                        ft.Text(passo, selectable=True)
                    )
                else:
                    coluna_passos_conversao.controls.append(passo)

        except ValueError as ex:
            mostrar_erro(f"Erro de valor: {ex}")
            txt_resultado_conversao.error_text = str(ex)
            txt_resultado_conversao.value = ""
        except Exception as ex:
            mostrar_erro(f"Ocorreu um erro inesperado: {ex}")
            txt_resultado_conversao.error_text = str(ex)
            txt_resultado_conversao.value = ""

        coluna_passos_conversao.visible = (
            len(coluna_passos_conversao.controls) > 2
        )
        page.update()

    # --- Lógica de Aritmética Binária ---
    def calcular_aritmetica(e):
        try:
            num1_str = txt_binario1.value
            num2_str = txt_binario2.value
            operacao = dd_operacao_aritmetica.value

            if not num1_str or not num2_str:
                mostrar_erro("Por favor, digite os dois números binários.")
                return

            if not all(c in "01" for c in num1_str) or not all(
                c in "01" for c in num2_str
            ):
                mostrar_erro(
                    "Os números binários devem conter apenas '0' e '1'."
                )
                return

            num1_dec, _ = converter_base_para_decimal(num1_str, 2)
            num2_dec, _ = converter_base_para_decimal(num2_str, 2)

            resultado_dec = 0
            if operacao == "Soma":
                resultado_dec = num1_dec + num2_dec
            elif operacao == "Subtração":
                resultado_dec = num1_dec - num2_dec
            elif operacao == "Multiplicação":
                resultado_dec = num1_dec * num2_dec
            elif operacao == "Divisão":
                if num2_dec == 0:
                    mostrar_erro("Erro: Divisão por zero não é permitida.")
                    txt_resultado_aritmetica.value = ""
                    txt_resultado_aritmetica.error_text = "Divisão por zero"
                    page.update()
                    return
                # Divisão inteira
                resultado_dec = num1_dec // num2_dec

            resultado_bin, _ = converter_decimal_para_base(resultado_dec, 2)

            txt_resultado_aritmetica.value = (
                f"{resultado_bin} (Decimal: {resultado_dec})"
            )
            txt_resultado_aritmetica.error_text = None

        except ValueError as ex:
            mostrar_erro(f"Erro de valor: {ex}")
            txt_resultado_aritmetica.error_text = str(ex)
            txt_resultado_aritmetica.value = ""
        except Exception as ex:
            mostrar_erro(f"Ocorreu um erro inesperado: {ex}")
            txt_resultado_aritmetica.error_text = str(ex)
            txt_resultado_aritmetica.value = ""

        page.update()

    # --- UI: Componentes de Conversão ---
    bases_disponiveis = [ft.dropdown.Option(str(b)) for b in [2, 8, 10, 16]]
    txt_numero_converter = ft.TextField(label="Número a ser convertido")
    dd_base_origem = ft.Dropdown(
        label="Base de Origem", options=bases_disponiveis, value="10"
    )
    dd_base_destino = ft.Dropdown(
        label="Base de Destino", options=bases_disponiveis, value="2"
    )
    btn_converter = ft.ElevatedButton(
        text="Converter",
        icon=ft.Icons.SWAP_HORIZ,
        on_click=calcular_conversao,
        bgcolor=ft.Colors.BLUE_700,
        color="white",
    )
    txt_resultado_conversao = ft.TextField(
        label="Resultado", read_only=True, text_size=18
    )

    coluna_passos_conversao = ft.Column(
        spacing=5,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        visible=False,
        controls=[]
    )

    card_conversao_inputs = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=15,
            content=ft.Column(
                [
                    ft.Text(
                        "Entrada", size=18, weight=ft.FontWeight.BOLD
                    ),
                    txt_numero_converter,
                    ft.Row(
                        [dd_base_origem, dd_base_destino],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    btn_converter,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        ),
    )

    card_conversao_resultado = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=15,
            content=ft.Column(
                [
                    txt_resultado_conversao,
                    ft.Divider(height=10),
                    coluna_passos_conversao
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        ),
    )

    tab_conversao = ft.Container(
        padding=20,
        content=ft.Column(
            [
                ft.Text(
                    "Conversor de Bases Numéricas",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                card_conversao_inputs,
                card_conversao_resultado,
            ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # --- UI: Componentes de Aritmética ---
    txt_binario1 = ft.TextField(label="Primeiro número binário")
    txt_binario2 = ft.TextField(label="Segundo número binário")
    dd_operacao_aritmetica = ft.Dropdown(
        label="Operação",
        options=[
            ft.dropdown.Option("Soma"),
            ft.dropdown.Option("Subtração"),
            ft.dropdown.Option("Multiplicação"),
            ft.dropdown.Option("Divisão"),
        ],
        value="Soma",
    )
    btn_calcular_aritmetica = ft.ElevatedButton(
        text="Calcular",
        icon=ft.Icons.CALCULATE,
        on_click=calcular_aritmetica,
        bgcolor=ft.Colors.BLUE_700,
        color="white",
    )
    txt_resultado_aritmetica = ft.TextField(
        label="Resultado", read_only=True, text_size=18
    )

    card_aritmetica_inputs = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=15,
            content=ft.Column(
                [
                    ft.Text(
                        "Entrada", size=18, weight=ft.FontWeight.BOLD
                    ),
                    txt_binario1,
                    txt_binario2,
                    dd_operacao_aritmetica,
                    btn_calcular_aritmetica,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        ),
    )

    card_aritmetica_resultado = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=15,
            content=ft.Column(
                [txt_resultado_aritmetica],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        ),
    )

    tab_aritmetica = ft.Container(
        padding=20,
        content=ft.Column(
            [
                ft.Text(
                    "Aritmética Binária",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                card_aritmetica_inputs,
                card_aritmetica_resultado,
            ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # --- Abas Principais ---

    menu_bar = ft.MenuBar(
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Arquivo"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Sair"), on_click=fechar_janela
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Ajuda"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Sobre"), on_click=abrir_dialogo_sobre
                    ),
                ],
            ),
        ]
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Conversão de Bases", content=tab_conversao),
            ft.Tab(text="Aritmética Binária", content=tab_aritmetica),
        ],
        expand=1,
    )

    page.add(menu_bar, tabs)


if __name__ == "__main__":
    ft.app(target=main)