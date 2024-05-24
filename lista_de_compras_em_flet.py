
import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import ssl

import flet as ft


class Listadecompra:
    """
    Representa uma lista, gerenciando produto / preço e usuários.

    Atributos:
        produtos (list): Uma lista de objetos produtos associados a Lista de Compra.
        clientes (list): Uma lista de objetos Usuario representando
                        os usuários do banco.
    """

    def __init__(self):
        """Inicializa um novo objeto Banco com listas vazias de contas e usuários."""
        self.produtos = []  # Corrigido: de self.produto para self.produtos
        self.clientes = []

    def criar_usuario(self, nome, cpf, forma_pagamento, endereco, email):
        """ "
        Cria um novo usuário e o adiciona à lista de usuários do banco.

        Args:
            nome (str): Nome do usuário.
            cpf (str): CPF do usuário.
            forma_pagamento (str): Forma de pagamento da lista.
            endereco (str): Endereço do usuário.

        Returns:
            cliente: O objeto cliente representando o usuário criado.

        Raises:
            ValueError: Se já existir um cliente com o mesmo CPF.
        """
        if self.obter_usuario_por_cpf(cpf):
            raise ValueError("Usuário já cadastrado com esse CPF.")
        cliente = Cliente(nome, cpf, forma_pagamento, endereco, email)
        self.clientes.append(cliente)
        return cliente

    def obter_usuario_por_cpf(self, cpf):
        """
        Busca um usuário pelo CPF.

        Args:
            cpf (str): O CPF do usuário.

        Returns:
            cliente: O objeto cliente se encontrado, None caso contrário.
        """
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def incluir_produto(self, nome, quantidade, valor_unitario, valor_total):
        """
        Inclui um novo produto à lista de produtos.

        Args:
            nome (str): Nome do produto.
            quantidade (float): Quantidade do item.
            valor (float): Valor unitário do item.
        """
        produto = Produto(nome, quantidade, valor_unitario, valor_total)
        # Corrigido: adicionado à lista self.produtos
        self.produtos.append(produto)

    def listar_produtos(self):
        """Imprime na tela a lista de produtos com seus nomes, quantidades e valores."""
        if not self.produtos:
            print("A lista de compras está vazia.")
        else:
            print("Produtos na lista:")
            for produto in self.produtos:
                print(
                    f"- {produto.nome} (Quantidade: {produto.quantidade}, Valor unitário do item: {produto.valor_unitario:.2f} Valor Total do Item: {produto.valor_total:.2f})"
                )

    def apagar_item(self, nome_usuario):
        """
        Permite ao usuário apagar um item da lista de compras por índice ou nome.

        Args:
            nome_usuario (str): O nome do usuário.
        """
        os.system("cls" if os.name == "nt" else "clear")  # Limpa a tela

        if not self.produtos:
            print(f"{nome_usuario}, sua lista de compras está vazia!")
            return

        print(f"Olá, {nome_usuario}! Selecione como deseja apagar o item: \n")
        opcao_apagar = input("[i]ndice ou [n]ome do item? ").lower()

        if opcao_apagar == "i":
            try:
                indice = int(input("Qual índice você deseja remover? "))
                if 0 <= indice < len(self.produtos):
                    item_removido = self.produtos.pop(indice)
                    print(
                        f"{nome_usuario}, você removeu com sucesso o item: {item_removido.nome}"
                    )
                else:
                    print(
                        f"{nome_usuario}, este índice não existe na sua lista. Tente novamente."
                    )
            except ValueError:
                print(
                    f"{nome_usuario}, por favor, insira um número inteiro válido para o índice."
                )

        elif opcao_apagar == "n":
            nome_do_item = input("Qual nome você deseja remover? ")
            for i, produto in enumerate(self.produtos):
                if produto.nome == nome_do_item:
                    del self.produtos[i]
                    print(
                        f"{nome_usuario}, você removeu com sucesso o item: {nome_do_item}"
                    )
                    return
            print(f"{nome_usuario}, este item não existe na lista.")

        else:
            print("Opção inválida. Escolha 'i' para índice ou 'n' para nome.")

    def comprar_itens(self, usuario):
        """
        Processa a compra dos itens da lista, gera um PDF com os detalhes
        da compra e envia por email para o usuário.
        """
        if not self.produtos:
            print("Sua lista de compras está vazia!")
            return

        # Calcula o valor total da compra
        valor_total = sum(produto.valor_total for produto in self.produtos)

        # Gera o PDF da compra
        nome_arquivo_pdf = f"compra_{usuario.nome}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        self.gerar_pdf_compra(usuario, nome_arquivo_pdf, valor_total)

        # Envia o email com o PDF
        self.enviar_email_confirmacao(usuario, nome_arquivo_pdf, valor_total)

        # Limpa a lista de compras após a compra
        self.produtos = []

    def gerar_pdf_compra(self, usuario, nome_arquivo_pdf, valor_total):
        """Gera um PDF com os detalhes da compra."""
        doc = SimpleDocTemplate(nome_arquivo_pdf, pagesize=letter)
        styles = getSampleStyleSheet()

        story = []
        story.append(Paragraph("Confirmação de Compra", styles["Heading1"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Dados do Comparador", styles["Heading2"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"Nome: {usuario.nome}", styles["Normal"]))
        story.append(
            Paragraph(f"Endereço de Entrega: {usuario.endereco}", styles["Normal"]))
        story.append(
            Paragraph(f"Forma de Pagamento: {usuario.forma_pagamento}", styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Itens Comprados:", styles["Heading2"]))
        for produto in self.produtos:
            story.append(
                Paragraph(
                    f"- {produto.nome} (Quantidade: {produto.quantidade}, Valor unitário do item: {produto.valor_unitario:.2f} Valor Total do Item: {produto.valor_total:.2f})",
                    styles["Normal"],
                )
            )
        story.append(Spacer(1, 12))

        story.append(
            Paragraph(f"Valor Total: R$ {valor_total:.2f}", styles["Heading2"])
        )

        doc.build(story)
        print(f"PDF da compra gerado com sucesso: {nome_arquivo_pdf}")

    def enviar_email_confirmacao(self, usuario, nome_arquivo_pdf, valor_total):
        """Envia um email de confirmação com o PDF da compra."""
        remetente_email = "applistadecompraspython@gmail.com"  # Substitua pelo seu endereço de email
        remetente_senha = "arzf mwtc wjgc iugb"  # Substitua pela sua senha
        destinatario_email = usuario.email

        mensagem = MIMEMultipart()
        mensagem["From"] = remetente_email
        mensagem["To"] = destinatario_email  # Usando o email do usuário
        mensagem["Subject"] = "Confirmação de Compra - Sua Lista de Compras"

        corpo_email = f"""
        Olá {usuario.nome},

        Obrigado por comprar conosco!

        Segue em anexo o PDF com a confirmação da sua compra no valor total de R$ {valor_total:.2f}.

        Atenciosamente,

        Sua Lista de Compras
        """
        mensagem.attach(MIMEText(corpo_email, "plain"))

        # Anexa o PDF à mensagem
        with open(nome_arquivo_pdf, "rb") as anexo:
            parte_anexo = MIMEBase("application", "octet-stream")
            parte_anexo.set_payload(anexo.read())
            encoders.encode_base64(parte_anexo)
            parte_anexo.add_header(
                "Content-Disposition", f"attachment; filename= {nome_arquivo_pdf}"
            )
            mensagem.attach(parte_anexo)

        # Cria uma conexão segura com o servidor SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as servidor:
            servidor.login(remetente_email, remetente_senha)
            servidor.sendmail(remetente_email, usuario.email,
                              mensagem.as_string())

        print("Email de confirmação enviado com sucesso!")


class Produto:
    def __init__(self, nome, quantidade, valor_unitario, valor_total):
        """
        Inicializa um novo objeto Produto.

        Args:
            nome (str): Nome do Produto.
            quantidade (float): Quantidade do item.
            valor_unitario(float): Valor do Item.
            valor_valor_total(float): Valor unitario x a quantidade

        """
        self.nome = nome
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.valor_unitario = valor_unitario


class Cliente:
    """
    Representa um Cliente com seus dados pessoais.

    Atributos:
        nome (str): Nome da pessoa.
        cpf (str): CPF da pessoa.
        forma_pagamento (str): Forma de pagamento da lista.
        endereco (str): Endereço da pessoa.
        email (str): Endereço de email do cliente.  <-- Adicionado!
    """

    def __init__(self, nome, cpf, forma_pagamento, endereco, email):
        """
        Inicializa um novo objeto Cliente.

        Args:
            nome (str): Nome da pessoa.
            cpf (str): CPF da pessoa.
            forma_pagamento (str): Forma de pagamento da lista.
            endereco (str): Endereço da pessoa.
            email (str): Endereço de email do cliente.  <-- Adicionado!
        """
        self.nome = nome
        self.cpf = cpf
        self.forma_pagamento = forma_pagamento
        self.endereco = endereco
        self.email = email


class ListaComprasApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.lista = Listadecompra()
        self.usuario_atual = None

        # Define a tela inicial com botões

        self.view = ft.Column(
            [
                ft.Text("Bem-vindo à Lista de Compras!", size=20),#Titulo
                ft.ElevatedButton("Login", on_click=self.abrir_modal_login), #Botao [1]
                ft.ElevatedButton(
                    "Incluir Item", on_click=self.abrir_modal_adicionar_item, disabled=True),#Botao [2]
                ft.ElevatedButton(
                    "Excluir Item", on_click=self.abrir_modal_apagar_item, disabled=True),#Botao [3]
                ft.ElevatedButton(
                    "Listar Produtos", on_click=self.abrir_modal_listar_produtos, disabled=True),#Botao [4]
                ft.ElevatedButton(
                    "Editar Item",on_click=self.abrir_modal_editar_item,disabled=True),#Botao [5]
                ft.ElevatedButton(
                    "Comprar Itens", on_click=self.abrir_modal_comprar_itens, disabled=True),#Botao [6]
                ft.ElevatedButton("Sair", on_click=self.sair_do_app),#Botao [7]
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def build(self):
        return self.view

    def atualizar_estado_botoes(self):
        """Atualiza o estado dos botões com base no login."""
        logado = bool(self.usuario_atual)  # True se usuario_atual não for None

        if logado:
            self.view.controls[1].disabled = True

        self.view.controls[2].disabled = not logado  # Incluir Item
        self.view.controls[3].disabled = not logado  # Excluir Item
        self.view.controls[4].disabled = not logado  # Listar Produtos
        self.view.controls[5].disabled = not logado  # Editar Itens
        self.view.controls[6].disabled = not logado  # Comprar Itens

        # Atualiza a view para refletir as mudanças
        self.view.update()

    def abrir_modal_login(self, e):
        self.dlg_login = ft.AlertDialog(
            modal=True,
            title=ft.Text("Login"),
            content=ft.Column(
                [
                    ft.TextField(label="Digite seu Nome", ref=ft.Ref[str]()),
                    ft.TextField(label="CPF", ref=ft.Ref[str]()),
                    ft.TextField(label="Forma de Pagamento",
                                 ref=ft.Ref[str]()),
                    ft.TextField(
                        label="Informe o endereço (logradouro, nro - bairro - cidade/sigla estado)", ref=ft.Ref[str]()),
                    ft.TextField(label="Email", ref=ft.Ref[str]()),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_modal),
                ft.ElevatedButton("Entrar", on_click=self.fazer_login),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg_login
        self.dlg_login.open = True
        self.page.update()

    def fazer_login(self, e):
        dlg = self.page.dialog
        nome = dlg.content.controls[0].value
        cpf = dlg.content.controls[1].value
        forma_pagamento = dlg.content.controls[2].value
        endereco = dlg.content.controls[3].value
        email = dlg.content.controls[4].value

        try:
            self.usuario_atual = self.lista.criar_usuario(
                nome, cpf, forma_pagamento, endereco, email)
            self.fechar_modal(e)  # Fecha o modal de login
            # Atualiza o estado dos botões
            self.atualizar_estado_botoes()

        except ValueError as e:
            print(f"Erro no login: {e}")
            # Aqui você pode adicionar lógica para exibir a mensagem de erro no modal, se desejar

    def abrir_modal_adicionar_item(self, e):
        self.dlg_adicionar_item = ft.AlertDialog(
            modal=True,
            title=ft.Text("Adicionar Item"),
            content=ft.Column(
                [
                    ft.TextField(label="Digite o Nome do Produto",
                                 ref=ft.Ref[str]()),
                    ft.TextField(label="Ditie a Quantidade",
                                 ref=ft.Ref[str]()),
                    ft.TextField(label="Digite o Valor Unitário",
                                 ref=ft.Ref[str]()),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_modal),
                ft.ElevatedButton("Adicionar", on_click=self.adicionar_item),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg_adicionar_item
        self.dlg_adicionar_item.open = True
        self.page.update()

    def adicionar_item(self, e):
        dlg = self.page.dialog
        nome = dlg.content.controls[0].value
        quantidade = dlg.content.controls[1].value
        valor_unitario = dlg.content.controls[2].value

        if self.usuario_atual:
            try:
                quantidade = float(quantidade)
                valor_unitario = float(valor_unitario)
                valor_total = quantidade * valor_unitario
                self.lista.incluir_produto(
                    nome, quantidade, valor_unitario, valor_total)
                self.fechar_modal(e)  # Fecha o modal
            except ValueError:
                print("Digite valores numéricos válidos.")
        else:
            print("Você precisa fazer login primeiro.")


    def abrir_modal_comprar_itens(self, e):
        if not self.lista.produtos:
            self.mostrar_alerta("Sua lista de compras está vazia!")
            return

        # Cria a lista de itens para o modal
        itens_lista = [
            ft.ListTile(
                title=ft.Text(produto.nome),
                subtitle=ft.Text(
                    f"-(Quantidade: {produto.quantidade}, Valor unitário do item: {produto.valor_unitario:.2f} Valor Total do Item: {produto.valor_total:.2f}"
                ),
            )
            for produto in self.lista.produtos
        ]

        # Calcula o valor total da compra
        valor_total = sum(
            produto.valor_total for produto in self.lista.produtos)

        # Cria o modal de confirmação de compra
        self.dlg_comprar_itens = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Compra"),
            content=ft.Column(
                [
                    ft.Text("Itens da sua compra:"),
                    ft.Column(itens_lista),
                    ft.Text(
                        f"Valor Total: R$ {valor_total:.2f}", size=16, weight=ft.FontWeight.BOLD),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_modal),
                ft.ElevatedButton("Confirmar", on_click=self.confirmar_compra),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg_comprar_itens
        self.dlg_comprar_itens.open = True
        self.mostrar_alerta("Email de confirmação enviado com sucesso!")
        self.page.update()

    def confirmar_compra(self, e):
        if self.usuario_atual:
            self.lista.comprar_itens(self.usuario_atual)
            self.fechar_modal(e)  # Fecha o modal de compra
        else:
            print("Você precisa fazer login primeiro.")

    def fechar_modal(self, e):
        self.page.dialog.open = False
        self.page.update()

    def sair_do_app(self, e):
        self.page.window_destroy()

    def abrir_modal_apagar_item(self, e):
        """Abre o modal para apagar um item."""
        if not self.lista.produtos:
            self.mostrar_alerta("Sua lista de compras está vazia!")
            return

        self.dlg_apagar_item = ft.AlertDialog(
            modal=True,
            title=ft.Text("Apagar Item"),
            content=ft.Column(
                [
                    ft.Text("Escolha uma opção:"),
                    ft.RadioGroup(
                        content=ft.Row(
                            [
                                ft.Radio(value="indice", label="Por Índice"),
                                ft.Radio(value="nome", label="Por Nome"),
                            ]
                        ),
                        ref=ft.Ref[ft.RadioGroup](),
                    ),
                    ft.TextField(label="Índice ou Nome",
                                 ref=ft.Ref[ft.TextField]()),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_modal),
                ft.ElevatedButton(
                    "Apagar", on_click=self.confirmar_apagar_item),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg_apagar_item
        self.dlg_apagar_item.open = True
        self.page.update()

    def confirmar_apagar_item(self, e):
        """Confirma a exclusão do item."""
        dlg = self.page.dialog
        opcao = dlg.content.controls[1].value
        valor = dlg.content.controls[2].value

        try:
            if opcao == "indice":
                indice = int(valor)
                if 0 <= indice < len(self.lista.produtos):
                    self.lista.produtos.pop(indice)
                    self.mostrar_alerta("Item apagado com sucesso!")
                else:
                    self.mostrar_alerta("Índice inválido!")
            elif opcao == "nome":
                for i, produto in enumerate(self.lista.produtos):
                    if produto.nome == valor:
                        del self.lista.produtos[i]
                        self.mostrar_alerta("Item apagado com sucesso!")
                        break
                else:
                    self.mostrar_alerta("Item não encontrado!")
            else:
                self.mostrar_alerta("Opção inválida!")
        except ValueError:
            self.mostrar_alerta("Índice inválido!")

        self.fechar_modal(e)

    def abrir_modal_listar_produtos(self, e):
        """Abre o modal para listar os produtos."""
        if not self.lista.produtos:
            self.mostrar_alerta("Sua lista de compras está vazia!")
            return

        itens_lista = [
            ft.ListTile(
                title=ft.Text(produto.nome),
                subtitle=ft.Text(
                    f"- Quantidade: {produto.quantidade}, Valor unitário do item: {produto.valor_unitario:.2f} Valor Total do Item: {produto.valor_total:.2f}"
                ),
            )
            for produto in self.lista.produtos
        ]

        dlg_listar_produtos = ft.AlertDialog(
            modal=True,
            title=ft.Text("Lista de Produtos"),
            content=ft.Column(itens_lista),
            actions=[
                ft.TextButton("Fechar", on_click=self.fechar_modal),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg_listar_produtos
        dlg_listar_produtos.open = True
        self.page.update()

    def abrir_modal_editar_item(self, e):
    
        """Abre o modal para editar um item da lista."""
        if not self.lista.produtos:
            self.mostrar_alerta("Sua lista de compras está vazia!")
            return

        self.dlg_editar_item = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Item"),
            content=ft.Column(
                [
                    ft.Text("Escolha o item a ser editado:"),
                    ft.Dropdown(
                        width=300,
                        options=[
                            ft.dropdown.Option(produto.nome) for produto in self.lista.produtos
                        ],
                        ref=ft.Ref[ft.Dropdown](),
                    ),
                    ft.TextField(label="Novo Nome", ref=ft.Ref[ft.TextField]()),
                    ft.TextField(label="Nova Quantidade", ref=ft.Ref[ft.TextField]()),
                    ft.TextField(label="Novo Valor Unitário", ref=ft.Ref[ft.TextField]()),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_modal),
                ft.ElevatedButton("Salvar", on_click=self.salvar_edicao_item),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg_editar_item
        self.dlg_editar_item.open = True
        self.page.update()
    '''def mostrar_alerta(self, mensagem):
        """Exibe um alerta (SnackBar) na tela."""
        self.page.snack_bar = ft.SnackBar(ft.Text(mensagem))
        self.page.snack_bar.open = True
        self.page.update()
    '''
    def salvar_edicao_item(self, e):
        """Salva as alterações feitas no item."""
        dlg = self.page.dialog
        nome_item_selecionado = dlg.content.controls[1].value
        novo_nome = dlg.content.controls[2].value
        nova_quantidade = dlg.content.controls[3].value
        novo_valor_unitario = dlg.content.controls[4].value

        try:
            nova_quantidade = float(nova_quantidade) if nova_quantidade else None
            novo_valor_unitario = float(novo_valor_unitario) if novo_valor_unitario else None

            for i, produto in enumerate(self.lista.produtos):
                if produto.nome == nome_item_selecionado:
                    if novo_nome:
                        self.lista.produtos[i].nome = novo_nome
                    if nova_quantidade:
                        self.lista.produtos[i].quantidade = nova_quantidade
                    if novo_valor_unitario:
                        self.lista.produtos[i].valor = nova_quantidade * novo_valor_unitario  # Recalcula o valor total
                    break

            self.fechar_modal(e)
            self.mostrar_alerta("Item editado com sucesso!")
        except ValueError:
            self.mostrar_alerta("Digite valores numéricos válidos para Quantidade e Valor Unitário.")
    
    def mostrar_alerta(self, mensagem):
        """Exibe um alerta (SnackBar) na parte CENTRAL da tela."""
        self.page.snack_bar = ft.SnackBar(
            ft.Container(
                ft.Text(mensagem),
                padding=ft.padding.all(10),
                bgcolor=ft.colors.BLUE_GREY_100,
                border_radius=ft.border_radius.all(5),
            ),
            # Define a posição horizontal como center
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page):
    page.title = "Lista de Compras"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    app = ListaComprasApp()
    page.add(app)
    app.atualizar_estado_botoes()


ft.app(target=main)
