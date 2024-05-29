# Entrada do usuário
cogumelo_desejado = input()

# Função para sugerir cogumelos com preços mais baixos
def sugerir_cogumelos(cogumelo_desejado):
    # Dicionário de cogumelos e preços
    catalogo = {
        "Shitake": 10,
        "Portobello": 8,
        "Shimeji": 6,
        "Champignon": 12,
        "Funghi": 16,
        "Porcini": 16
    }

    # Verifica se o cogumelo desejado está no catálogo
    if cogumelo_desejado in catalogo:
        # Armazena o preço do cogumelo desejado
        valor_desejado = catalogo[cogumelo_desejado]
        # Cria uma lista vazia para as sugestões
        sugestoes = []

        # Procura por cogumelos mais baratos
        for cogumelo, valor in catalogo.items():
            if valor <= valor_desejado and cogumelo != cogumelo_desejado:
                sugestoes.append((cogumelo, valor))
                if len(sugestoes) == 2:  # Limita a no máximo duas sugestões
                    break

        if sugestoes:
            for sugestao, valor_sugestao in sugestoes:
                print(f"{sugestao} - Valor: {valor_sugestao}")
        else:
            print("Desculpe, não há sugestões disponíveis.")
    else:
        print("Cogumelo não encontrado no catálogo.")

# Chamada da função
sugerir_cogumelos(cogumelo_desejado)