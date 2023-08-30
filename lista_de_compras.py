
# Pede o nome do usuário
nome_usuario = input('Digite seu nome: ')
# Pede o nome da lista de compras
# nome_da_lista = input(f'Olá, {nome_usuario}, insira um nome para sua lista de compras: ')
# Cria a  a lista
lista_compras = []

# Função para incluir item na lista


def incluir_item():
    # Cria uma nova variavel chamada novo_elemento
    novo_elemento = input('Insira a descrição do novo item: ')
    # Executa o metodo append e inclui um novo elemento na lista
    lista_compras.append(novo_elemento)
    # Envia uma mensagem na tela informando que o item foi gravado com sucesso
    print(f'{novo_elemento=} inserido com com sucesso!')

# Funçõa Listar Itens e seus indices


def listar_itens():
    print('listando os objetos de uma lista\n')

    if len(lista_compras) == 0:
        print(f'{nome_usuario} sua lista esta vazia :( ')
    else:
        for indice, produtos in enumerate(lista_compras):
            print(indice, produtos)

# Funçõa para apagar um item através do indice ou do nome


def apagar_item():
    # Pergunta ao usuario o que quer apagar
    print(f'Olá{nome_usuario}! Selecione o que quer apagar : \n')
    # cria a variavel opcao_apagar
    opcao_apagar = input('[i]ndice ou [n]ome do item? ')

    if 'i' in opcao_apagar:
        indice = int(input("Qual indice você deseja remover: "))

        if indice > (len(lista_compras)-1) or indice < 0:
            print(f"{nome_usuario} este indice não existe na sua lista ou sua lista esta vazia. Tente listar ou buscar o pelo nome do item.")

        else:
            item_removido = lista_compras[indice]
            lista_compras.pop(indice)
            print(f"{nome_usuario} você removeu com sucesso o item {item_removido}")

    if 'n' in opcao_apagar:
        nome_do_item = input("Qual nome você deseja remover: ")

        if nome_do_item in lista_compras:
            lista_compras.remove(nome_do_item)
        else:
            print(f'{nome_usuario} este item não existe na lista')

#


# Cria laço While para interação com o usuário
while True:

    print(f'Olá{nome_usuario}! Selecione uma opção: \n')
    resposta = input("[i]nserir, [a]pagar, [l]istar ou [s]air? ").lower()

    if 'i' in resposta:
        incluir_item()
        continue

    elif 'a' in resposta:
        apagar_item()
        continue

    elif 'l' in resposta:
        listar_itens()
        continue
    
    elif 's' in resposta:
        break

    else:
        continue    
   

