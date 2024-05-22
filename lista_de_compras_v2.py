import os
import datetime

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
        self.produto = []
        self.clientes = []
    

    def criar_usuario(self, nome, cpf, forma_pagamento, endereco):
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
        cliente = Cliente(nome, cpf, forma_pagamento, endereco)
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
    
class Produto:
    def __init__(self, nome, quantidade, valor):
        """
        Inicializa um novo objeto Conta.

        Args:
            nome (str): Nome do Produto.
            quantidade (float): Quantidade do item.
            valor(float): Valor do Item.
            
        """
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
    pass
class Cliente:
    """
    Representa um Cliente com seus dados pessoais.

    Atributos:
        nome (str): Nome da pessoa.
        cpf (str): CPF da pessoa.
        forma_pagamento (str): Forma de pagamento da lista.
        endereco (str): Endereço da pessoa.
    """

    def __init__(self, nome, cpf, forma_pagamento, endereco):
        """
        Inicializa um novo objeto Cliente.

        Args:
            nome (str): Nome da pessoa.
            cpf (str): CPF da pessoa.
            forma_pagamento (str): Forma de pagamento da lista.
            endereco (str): Endereço da pessoa.
        """
        self.nome = nome
        self.cpf = cpf
        self.forma_pagamento = forma_pagamento
        self.endereco = endereco
    
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
    
    # Inciar um Laço True esperando o usuario interagir com o menu
    while True:
        # Cria a Veriável opção para que recebe uma escolha do usuario nas opções dispostas pela função Menu()
        opcao = menu()
        
        if opcao == "i":
            pass
        elif opcao == "e":
            pass
        elif opcao == "l":
            pass
        elif opcao == "c":
            pass
        elif opcao == "n":
            nome = input("Digite o nome do usuário: ")
            cpf = input("Digite o CPF do usuário: ")
            forma_pagamento = input("Digite a forma de pagamento (Dinheiro, Cartão ou PIX): ")
            endereco = input("Digite o endereço: ")
            try:
                lista.criar_usuario(nome, cpf, forma_pagamento, endereco)
                print("Usuário criado com sucesso!")
            except ValueError as e:
                print(e)
                
        elif opcao == "q":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")
        
        
main()