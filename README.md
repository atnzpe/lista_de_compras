# ListedComprasComPython

**Algoritimo Básico para Inserir, Apagar e Listar uma Lista de Compras.**

* *Faça uma lista de compras com list()*

* *O usuário deve ter a possibilidade de inserir, apagar e listar valores da sua lista.*

* *Não permita que o programa quebre com erros de índices inexistentes na lista.*

## feat: Implementação da funcionalidade de compra e envio de email

Adicionada a funcionalidade de comprar todos os itens da lista de compras, gerando um PDF com os detalhes da compra e enviando por email para o usuário.

As seguintes alterações foram realizadas:

* Adicionado o atributo `email` à classe `Cliente`.
* Implementada a função `comprar_itens` na classe `Listadecompra` para:
    * Calcular o valor total da compra.
    * Gerar um PDF da compra com nome do usuário, endereço, itens e valor total, usando a biblioteca `reportlab`.
    * Enviar um email de confirmação com o PDF em anexo, usando `smtplib` e uma senha de aplicativo do Gmail.
    * Limpar a lista de compras após a compra.
* A função `criar_usuario` foi atualizada para solicitar o email do usuário.
* Adicionado tratamento de erro na função main para quando o usuário digitar um valor inválido.
* Pequenas correções e melhorias no código.
