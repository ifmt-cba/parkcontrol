| **Nome do Caso de Uso**       | Visualizar Pagamentos Realizados |
|------------------------------|-----------------------------------|
| **Descrição**                | Permite que o contador acesse o histórico de pagamentos já realizados pelos clientes mensalistas. |
| **Ator Envolvido**           | Contador |

| **Interação entre Ator e Sistema**       |                                                    |
|------------------------------------------|----------------------------------------------------|
| **Ator**                                 | **Sistema**                                        |
| Contador acessa a área de "Gerência de Pagamentos"  . | Sistema exibe a opção "Visualizar Pagamentos Realizados" . *(RI01)* |
| Contador acessa a opção "Visualizar Pagamentos Realizados" no menu. | Sistema exibe filtros de busca: cliente. *(RI01)* |
| Contador preenche o filtro e clica em "Buscar". | Sistema lista os pagamentos realizados no período. *(RI02)* |
| Contador seleciona um pagamento da lista. | Sistema exibe os detalhes completos do pagamento. *(RI03, RN01)* |

| **Exceções** |
|-------------|
| EX01 - Nenhum pagamento encontrado: sistema exibe mensagem de "Nenhum resultado para os filtros informados". |

| **Alternativas** |
|------------------|
| AL01 - Contador pode exportar a lista de pagamentos em PDF. |

| **Regras de Negócio** |
|-----------------------|
| RN01 - Somente pagamentos com status "Pago" devem aparecer nesta lista. |

| **Requisitos de Interface com o Usuário** |
|-------------------------------------------|
| RI01 - A interface deve permitir filtragem pelo nome do cliente. |
| RI02 - A tabela deve mostrar: cliente, valor, data do pagamento. |
| RI03 - A interface deve permitir acesso aos detalhes completos do pagamento. |

**Dicionário de Dados – Campos de Entrada**

| Nome do Campo    | Tipo de Dado | Expressão Regular            | Máscara       | Descrição                                                | Obrigatório | Único | Default |
|------------------|--------------|-------------------------------|----------------|----------------------------------------------------------|-------------|-------|---------|
| nome_cliente     | Texto        | ^[a-zA-ZÀ-ú\s]{3,100}$        | -              | Nome parcial ou completo do cliente para busca.         | Não         | Não   | -       |

