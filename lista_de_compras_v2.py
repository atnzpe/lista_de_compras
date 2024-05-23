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

    def criar_usuario(self, nome, cpf, forma_pagamento, endereco,email):
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
        cliente = Cliente(nome, cpf, forma_pagamento, endereco,email)
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

    def incluir_produto(self, nome, quantidade, valor):
        """
        Inclui um novo produto à lista de produtos.

        Args:
            nome (str): Nome do produto.
            quantidade (float): Quantidade do item.
            valor (float): Valor unitário do item.
        """
        produto = Produto(nome, quantidade, valor)
        self.produtos.append(produto)  # Corrigido: adicionado à lista self.produtos

    def listar_produtos(self):
        """Imprime na tela a lista de produtos com seus nomes, quantidades e valores."""
        if not self.produtos:
            print("A lista de compras está vazia.")
        else:
            print("Produtos na lista:")
            for produto in self.produtos:
                print(
                    f"- {produto.nome} (Quantidade: {produto.quantidade}, Valor Total do Item: {produto.valor:.2f})"
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
        valor_total = sum(produto.valor for produto in self.produtos)

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

        story.append(Paragraph(f"Nome: {usuario.nome}", styles["Normal"]))
        story.append(Paragraph(f"Endereço de Entrega: {usuario.endereco}", styles["Normal"]))
        story.append(Paragraph(f"Forma de Pagamento: {usuario.forma_pagamento}", styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Itens Comprados:", styles["Heading2"]))
        for produto in self.produtos:
            story.append(
                Paragraph(
                    f"- {produto.nome} (Quantidade: {produto.quantidade}, Valor Total do Item: {produto.valor:.2f})",
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
            servidor.sendmail(remetente_email, usuario.email, mensagem.as_string())

        print("Email de confirmação enviado com sucesso!")


class Produto:
    def __init__(self, nome, quantidade, valor):
        """
        Inicializa um novo objeto Produto.

        Args:
            nome (str): Nome do Produto.
            quantidade (float): Quantidade do item.
            valor(float): Valor do Item.

        """
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor

    


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


def menu():
    """
    Exibe o menu de opções da lista de compras para o usuário.

    Returns:
        str: A opção escolhida pelo usuário.
    """
    # Exibe as opções para escolha
    menu = """
    O que deseja fazer?
    [i] Incluir um Item
    [e] Excluir um item
    [l] Listar produtos incluídos na Lista
    [c] Comprar os itens da lista
    [n] Novo Usuário
    [q] Sair
    -> """
    return input(menu)


def main():
    """
    Função principal da Lista de Comprars. Gerencia as operações e interações com o usuário.
    """
    lista = Listadecompra()
    usuario_atual = None  # Armazena o usuário logado no momento

    # Inciar um Laço True esperando o usuario interagir com o menu
    while True:
        # Cria a Veriável opção para que recebe uma escolha do usuario nas opções dispostas pela função Menu()
        opcao = menu()

        if opcao == "i":
            if usuario_atual:
                nome = input("Informe o nome do Produto: ")

                try:
                    quantidade = float(input("Informe a quantidade do Produto: "))
                    valor = float(input("Informe o VALOR UNITARIO do Produto: "))
                except ValueError:
                    print('Tente novamente e Digite um valor válido! Ex: 1.7')
                    
                valor_total = quantidade * valor
                lista.incluir_produto(nome, quantidade, valor_total)
                print("Produto incluído com sucesso!")
            else:
                print("Você precisa fazer login primeiro (opção 'n').")

        elif opcao == "e":
            if usuario_atual:
                lista.apagar_item(
                    usuario_atual.nome
                )  # Chama a função apagar_item da classe Listadecompra
            else:
                print("Você precisa fazer login primeiro (opção 'n').")

        elif opcao == "l":
            lista.listar_produtos()

        elif opcao == "c":
            if usuario_atual:
                lista.comprar_itens(usuario_atual)
            else:
                print("Você precisa fazer login primeiro (opção 'n').")

        elif opcao == "n":
            nome = input("Digite o nome do usuário: ")
            cpf = input("Digite o CPF do usuário: ")
            forma_pagamento = input(
                "Digite a forma de pagamento (Dinheiro, Cartão ou PIX): "
            )
            endereco = input("Digite o endereço: ")
            email = input("Digite seu email: ")
            try:
                usuario_atual = lista.criar_usuario(
                    nome, cpf, forma_pagamento, endereco,email
                )
                print("Usuário criado e logado com sucesso!")
            except ValueError as e:
                print(e)

        elif opcao == "q":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")


main()
