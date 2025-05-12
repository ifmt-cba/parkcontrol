| **Nome do Caso de Uso**       | Editar Status de Pagamento |
|------------------------------|----------------------------|
| **Descrição**                | Permite que o contador edite o status de um pagamento, alterando-o de "Em aberto" para "Pago" ou vice-versa. |
| **Ator Envolvido**           | Contador |

| **Interação entre Ator e Sistema**       |                                                    |
|------------------------------------------|----------------------------------------------------|
| **Ator**                                 | **Sistema**                                        |
| Contador acessa a área de "Gerência de Pagamentos" | Sistema exibe a opção "Listagem de Pagamentos" . *(RI01)* |
| Contador acessa a área "Listagem de Pagamentos". | Sistema exibe a lista de pagamentos |
| Contador seleciona um pagamento da lista para editar. | Sistema exibe os detalhes completos do pagamento, com opção para alterar o status. *(RI02, RI03)* |
| Contador edita o status do pagamento (de "Em aberto" para "Pago", ou vice-versa). | Sistema atualiza o status do pagamento e exibe uma mensagem de sucesso. *(RN01)* |
| Contador clica em "Salvar". | Sistema salva a alteração e exibe a mensagem "Status de pagamento atualizado com sucesso". *(RI04)* |

| **Exceções** |
|-------------|
| EX01 - Pagamento não encontrado: o sistema exibe a mensagem "Pagamento não encontrado". |

| **Alternativas** |
|------------------|
| AL01 - O contador pode exportar a lista de pagamentos filtrada em PDF. |
| AL02 - O contador pode cancelar a alteração, e o status do pagamento volta ao estado anterior. |

| **Regras de Negócio** |
|-----------------------|
| RN01 - O status de pagamento pode ser alterado apenas entre os valores "Em aberto" e "Pago". |

| **Requisitos de Interface com o Usuário** |
|-------------------------------------------|
| RI01 - A interface deve exibir somente pagamentos com status "Em aberto" ou "Pago" para edição. |
| RI02 - A interface deve exibir os detalhes do pagamento selecionado, incluindo o campo para alteração de status. |
| RI03 - A interface deve permitir que o contador altere o status de pagamento, com opções de "Em aberto" e "Pago". |
| RI04 - A interface deve informar uma mensagem de "Status de pagamento atualizado com sucesso" após salvar a opção. |

**Dicionário de Dados – Campos de Entrada**

| Nome do Campo    | Tipo de Dado | Expressão Regular            | Máscara       | Descrição                                                | Obrigatório | Único | Default |
|------------------|--------------|-------------------------------|----------------|----------------------------------------------------------|-------------|-------|---------|
| nome_cliente     | Texto        | ^[a-zA-ZÀ-ú\s]{3,100}$        | -              | Nome parcial ou completo do cliente para busca.         | Não         | Não   | -       |
| status_pagamento | Texto        | ^(Em aberto\Pago |             | -              | Status atual do pagamento.                             | Sim         | Não   | Em aberto |
