| Nome do Caso de Uso       | Excluir Relatório |
|---------------------------|--------------------------------------------------|
| *Descrição*               | Permite que o contador exclua um relatório financeiro já gerado e finalizado. |
| *Ator Envolvido*          | Contador |

| *Interação entre Ator e Sistema*       |                                                  |
|----------------------------------------|--------------------------------------------------|
| *Ator*                                 | *Sistema*                                        |
| Contador acessa o área de relatórios. | Sistema exibe a  opção "Excluir Relatório". |
| Contador seleciona a opção "Excluir".  | Sistema exibe os relatórios disponíveis para exclusão. *(RI01)* |
| Contador seleciona o relatório a ser excluído. | Sistema exibe os detalhes do relatório selecionado. *(RI02)* |
| Contador clica na opção "Excluir".     | Sistema solicita confirmação para excluir o relatório. *(RI03)* |
| Contador confirma a exclusão.          | Sistema remove o relatório do sistema e exibe uma mensagem de sucesso. *(RI04, RN01)* |
| Contador cancela a exclusão.           | Sistema mantém o relatório na lista sem alterações. *(AL01)* |

| *Exceções* |
|------------|
| EX01 - O processo de exclusão pode ser cancelado a qualquer momento, caso o contador saia da pagina. |

| *Alternativas* |
|----------------|
| AL01 - Contador pode cancelar a exclusão e retornar à lista de relatórios. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com perfil de contador podem excluir relatórios financeiros. |
| RN02 - Relatórios com status "Finalizado" podem ser excluídos. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A lista de relatórios deve permitir seleção do relatório a ser excluído. |
| RI02 - O sistema deve exibir uma opção clara de "Excluir" junto ao relatório. |
| RI03 - O sistema deve exibir uma mensagem de confirmação antes de realizar a exclusão. |
| RI04 - O sistema deve exibir uma mensagem de sucesso confirmando a exclusão do relatório. |
