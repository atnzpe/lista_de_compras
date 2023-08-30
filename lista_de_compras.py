# Pede o nome do usuário
nome_usuario = input('Digite seu nome: ')
# Pede o nome da lista de compras
#nome_da_lista = input(f'Olá, {nome_usuario}, insira um nome para sua lista de compras: ')
# Cria a  a lista
lista_compras = []

def insere():
    novo_elemento = input('Insira a descrição do novo item: ')
    lista_compras.append(novo_elemento)
    print(f'{novo_elemento=} inserido com com sucesso!')


# Cria laço While para interação com o usuário
while True:

    print('Selecione uma opção: \n')
    resposta = input("[i]nserir, [a]pagar, [l]istar ou [s]air? ").lower()




   
