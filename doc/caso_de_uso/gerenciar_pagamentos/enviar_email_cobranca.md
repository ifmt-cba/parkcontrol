| **Nome do Caso de Uso**       | Encaminhar E-mail de Cobrança |
|------------------------------|-----------------------------------|
| **Descrição**                | Permite que o contador encaminhe um e-mail de cobrança para os clientes mensalistas ativos no sistema. |
| **Ator Envolvido**           | Contador |

| **Interação entre Ator e Sistema**       |                                                    |
|------------------------------------------|----------------------------------------------------|
| **Ator**                                 | **Sistema**                                        |
| Contador acessa a área de "Gerência de Pagamentos"  . | Sistema exibe a opção "Enviar E-mail de Cobrança" . *(RI01)* |
| Contador seleciona a opção "Enviar E-mail de Cobrança". | Sistema exibe a lista de clientes mensalistas ativos, com campo de filtro por nome. *(RI01)* |
| Contador informa o nome do cliente no filtro e clica em "Buscar". | Sistema exibe os pagamentos não realizados pelo cliente no período. *(RI02)** |
| Contador seleciona um pagamento da lista. | Sistema exibe os detalhes completos do pagamento. *(RI03, RN01)* |
| Contador clica em "Encaminhar E-mail". | Sistema envia o e-mail de cobrança ao cliente com os dados do pagamento e exibe mensagem de sucesso. *(RI04)*  |


| **Exceções** |
|-------------|
| EX01 - Nenhum pagamento encontrado: o sistema exibe a mensagem "Nenhum resultado para os filtros informados". 

| **Alternativas** |
|------------------|
| AL01 - O contador pode exportar a lista de pagamentos filtrada em PDF. |

| **Regras de Negócio** |
|-----------------------|
| RN01 - Somente pagamentos com status "Em aberto" devem ser exibidos na lista de seleção. |

| **Requisitos de Interface com o Usuário** |
|-------------------------------------------|
| RI01 - A interface deve permitir a filtragem por nome do cliente. |
| RI02 -A tabela deve apresentar: nome do cliente, valor e data do pagamento. |
| RI03 - A interface deve permitir acesso aos detalhes completos de um pagamento selecionado. |
| RIL4 - A interface deve exibir uma mensagem de de sucesso após o contador selecionar o botar "Encaminhar E-mail |

**Dicionário de Dados – Campos de Entrada**

| Nome do Campo    | Tipo de Dado | Expressão Regular            | Máscara       | Descrição                                                | Obrigatório | Único | Default |
|------------------|--------------|-------------------------------|----------------|----------------------------------------------------------|-------------|-------|---------|
| nome_cliente     | Texto        | ^[a-zA-ZÀ-ú\s]{3,100}$        | -              | Nome parcial ou completo do cliente para busca.         | Não         | Não   | -       |

