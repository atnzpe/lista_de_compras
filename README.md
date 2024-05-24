# ListedComprasComPython

**Algoritimo Básico para Inserir, Apagar e Listar uma Lista de Compras.**

* *Faça uma lista de compras com list()*

* *O usuário deve ter a possibilidade de inserir, apagar e listar valores da sua lista.*

* *Não permita que o programa quebre com erros de índices inexistentes na lista.*


feat: Implementação da interface de usuário com Flet e novas funcionalidades

Refatoração completa do código para usar a biblioteca Flet, criando uma interface gráfica de usuário interativa.

**Funcionalidades Implementadas:**

- Tela de login com campos para nome, CPF, forma de pagamento, endereço e email.
- Autenticação de usuário com base no CPF.
- Gerenciamento de lista de compras:
    - Adição de itens com nome, quantidade e valor unitário.
    - Exclusão de itens por índice ou nome.
    - Visualização da lista de compras.
    - Confirmação de compra com exibição detalhada dos itens e valor total.
    - Geração de PDF da compra e envio por email.
- Botões interativos para cada ação, organizados em modais (AlertDialog) para melhor experiência do usuário.
- Mensagens de alerta (SnackBar) centralizadas na tela para feedback ao usuário.
- Tratamento de erros básico para entradas inválidas.
- Desabilitação de botões de ação até que o usuário faça login.

**Melhorias:**

- Organização do código em classes e funções para melhor legibilidade e manutenção.
- Separação de telas (views) para cada etapa do processo (login, gerenciamento de produtos, etc.).
- Uso de componentes visuais do Flet (TextField, ElevatedButton, AlertDialog, SnackBar, etc.) para criar uma interface mais intuitiva.

**Próximos Passos:**

- Implementar funcionalidades adicionais, como edição de itens, histórico de compras, etc.
- Aprimorar o tratamento de erros e a validação de entradas do usuário.
- Refinar o design da interface para uma melhor experiência do usuário.

### Em 24/05/2024

feat: Implementada a funcionalidade de edição de itens

Adicionada a capacidade de editar itens existentes na lista de compras.

- Adicionado um botão "Editar Item" à tela principal.
- Criado um modal para edição de itens, permitindo ao usuário:
    - Selecionar o item a ser editado através de um dropdown.
    - Alterar o nome, quantidade e valor unitário do item.
- Implementada a lógica para salvar as alterações do item na lista de compras.
- Habilitado o botão "Editar Item" após o login do usuário.

Essa funcionalidade aumenta a flexibilidade do aplicativo, permitindo que os usuários corrijam ou modifiquem os itens da sua lista de compras de forma conveniente.git