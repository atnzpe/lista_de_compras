
import os

# Pede o nome do usuário
nome_usuario = input('Digite seu nome: ')
# Pede o nome da lista de compras
# nome_da_lista = input(f'Olá, {nome_usuario}, insira um nome para sua lista de compras: ')
# Cria a  a lista
lista_compras = []

# Função para incluir item na lista

def incluir_item():
    # Limpar a tela
    os.system('cls')
    # Cria uma nova variavel chamada novo_elemento
    novo_elemento = input('Insira a descrição do novo item: ')
    # Executa o metodo append e inclui um novo elemento na lista
    lista_compras.append(novo_elemento)
    # Envia uma mensagem na tela informando que o item foi gravado com sucesso
    print(f'{nome_usuario} o item {novo_elemento} foi inserido na lista!\n')

# Função Listar Itens e seus indices

def listar_itens():
    # Limpar a tela
    os.system('cls')
    print('listando os objetos de uma lista: ')

    if len(lista_compras) == 0:
        print(f'{nome_usuario} sua lista esta vazia :( ')
    else:
        print("\nIncio da Lista\n")
        print("ID", "Descrição", sep=" --- ")
        for indice, produtos in enumerate(lista_compras):
            print(indice, produtos, sep="  --- ")

    print("\nFim da Lista\n")

# Funçõa para apagar um item através do indice ou do nome


            

# Cria laço While para interação com o usuário
while True:

    print(f'Olá {nome_usuario}! Selecione uma opção: \n')
    resposta = input("[i]nserir, [a]pagar, [l]istar ou [s]air? ").lower()

    if 'i' in resposta:

        incluir_item()
        continue

    elif 'a' in resposta:
        os.system('cls')
        apagar_item()
        continue

    elif 'l' in resposta:
        os.system('cls')
        listar_itens()
        continue

    elif 's' in resposta:
        break

    else:
        continue

os.system('cls')
print(f'Até mais {nome_usuario} Sua lista de itens esta logo abaixo :P')
listar_itens()
