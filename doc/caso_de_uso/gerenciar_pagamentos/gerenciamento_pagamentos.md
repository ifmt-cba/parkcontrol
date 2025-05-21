| Nome do Caso de Uso       | Gerenciamento de Pagamentos |
|---------------------------|----------------------------------|
| *Descrição*               | Permite ao contador gerenciar os pagamentos, incluindo a visualização de pagamentos, geração de pagamentos. edição de status de pagamentos e envio de cobrança por E-mail. |
| *Ator Envolvido*          | Contador |

| *Interação entre Ator e Sistema*       |                                                  |
|----------------------------------------|--------------------------------------------------|
| *Ator*                                 | *Sistema*                                        |
| Contador acessa o módulo de "Gerenciamento de Pagamentos". | Sistema exibe a interface principal do módulo Gerenciamento de Pagamentos, contendo opções de "Visualizar Pagamentos Realizados", "Listagem de Pagamentos", "Gerar Pagamentos Mensalistas" e "Enviar E-mail de Cobrança". *(RN01, RI01)* |
| Contador seleciona a opção desejada (visualizar, gerar, editar (listagem de pagamentos), enviar e-mail de cobrança. | Sistema apresenta as funcionalidades específicas de acordo com a opção selecionada. |
| Caso o contador selecione **"Visualizar Pagamentos Realizados"**. | Sistema lista os pagamentos realizados no período, juntamente com um filtro de busca. |
| Caso o contador selecione **"Listagem de Pagamentos"**. | Sistema exibe a lista de pagamentos, juntamente com os detalhes completos do pagamento, com opção para alterar o Status. |
| Caso o contador selecione **"Gerar Pagamentos Mensalista"**. | Sistema exibe lista de mensalistas ativos e opção "Gerar cobrança". |
| Caso o contador selecione **"Enviar E-mail de Cobrança"**. | Sistema exibe a lista de clientes mensalistas ativos, com campo de filtro por nome. |

| *Exceções* |
|------------|
| EX01 - O sistema exibe mensagem de erro caso o contador não tenha permissão para acessar uma das funcionalidades. |

| *Alternativas* |
|----------------|
| AL01 - Contador pode cancelar qualquer operação e retornar à lista de relatórios. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com o perfil de contador podem acessar o módulo de Gerenciamento de Pagamentos. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A interface do módulo deve exibir claramente as opções de "Visualizar Pagamentos Realizados", "Listagem de Pagamentos", "Gerar Pagamentos Mensalistas" e "Enviar E-mail de Cobrança". |
