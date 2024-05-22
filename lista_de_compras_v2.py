import os
import datetime

class Listadecompra:
    """
    Representa uma lista, gerenciando produto / preço e usuários.

    Atributos:
        produtos (list): Uma lista de objetos produtos associados a Lista de Compra.
        cliente (list): Uma lista de objetos Usuario representando
                        os usuários do banco.
    """
    def __init__(self):
        """Inicializa um novo objeto Banco com listas vazias de contas e usuários."""
        self.produto = []
        self.cliente = []
    pass

    
class Produto:
    def __init__(self, numero, agencia, titular, saldo=0):
        """
        Inicializa um novo objeto Conta.

        Args:
            numero (int): Número da conta.
            agencia (str): Agência da conta.
            titular (PessoaFisica): O titular da conta (objeto PessoaFisica).
            saldo (float, optional): Saldo inicial da conta. Defaults to 0.
        """
        self.numero = numero
        self.agencia = agencia
        self.titular = titular
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
    
