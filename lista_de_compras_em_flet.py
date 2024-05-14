import flet as ft


def main(page: ft.Page):
    page.title = "Lista de Compras"

    nome_usuario = ft.TextField(label="Digite seu nome")
    lista_compras = []

    def adicionar_item(e):
        novo_item = novo_item_input.value
        lista_compras.append(novo_item)
        # Adicionar data ao ListTile para identificar o item
        lista_itens.controls.append(ft.ListTile(title=ft.Text(novo_item), data=novo_item)) 
        novo_item_input.value = ""
        page.update()

    def apagar_item(e):
        item_removido = item_removido_input.value
        # Remover da lista
        if item_removido in lista_compras:
            lista_compras.remove(item_removido)

        # Remover da interface
        for i, item in enumerate(lista_itens.controls):
            if hasattr(item, 'data') and item.data == item_removido:
                lista_itens.controls.pop(i)
                break

        item_removido_input.value = ""
        page.update()

    # Elementos da interface
    lista_itens = ft.Column()
    novo_item_input = ft.TextField(label="Novo item")
    botao_adicionar = ft.ElevatedButton("Adicionar", on_click=adicionar_item)
    item_removido_input = ft.TextField(label="Item a remover")
    botao_remover = ft.ElevatedButton("Remover", on_click=apagar_item)

    page.add(
        ft.Column(
            [
                nome_usuario,
                ft.Row([novo_item_input, botao_adicionar]),
                ft.Row([item_removido_input, botao_remover]),
                lista_itens,
            ]
        )
    )


ft.app(target=main)
