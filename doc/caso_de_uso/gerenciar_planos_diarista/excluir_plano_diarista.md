## Caso de Uso: Excluir Plano Diarista

| Nome do Caso de Uso       | Excluir Plano Diarista                                                                                 |
|---------------------------|--------------------------------------------------------------------------------------------------------|
| *Descrição*               | Permite ao administrador remover um plano de diária do sistema, respeitando regras de exclusão.        |
| *Ator Envolvido*          | Administrador                                                                                           |

| *Interação entre Ator e Sistema*       |                                                                                                         |
|----------------------------------------|---------------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                               |
| Acessa o menu de administração.        | Exibe opções de gerenciamento. *(RI01)*                                                                 |
| Seleciona "Gerenciar Planos Diaristas". | Lista todos os planos disponíveis. *(RI01)*                                                             |
| Clica em "Excluir" no plano desejado.   | Solicita confirmação da ação. *(RI02)*                                                                  |
| Confirma a exclusão.                    | Remove o plano do sistema. *(RN01, EX01)*                                                               |

| *Exceções*                                                                                             |
|--------------------------------------------------------------------------------------------------------|
| EX01 - Tentativa de excluir plano associado a clientes ativos. O sistema impede e informa o motivo.    |
| EX02 - Falha no sistema durante a exclusão. O sistema exibe mensagem de erro.                           |

| *Alternativas*                                                                                         |
|--------------------------------------------------------------------------------------------------------|
| AL01 - O administrador pode cancelar a exclusão após o aviso de confirmação.                           |

| *Regras de Negócio*                                                                                     |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Planos só podem ser excluídos se não estiverem associados a clientes ativos.                     |
| RN02 - Exclusões devem ser registradas em log de auditoria.                                              |

| *Requisitos de Interface com o Usuário*                                                                 |
|--------------------------------------------------------------------------------------------------------|
| RI01 - Apresentar botão "Excluir" próximo a cada plano listado.                                         |
| RI02 - Exibir caixa de diálogo para confirmação da exclusão.                                            |
| RI03 - Após excluir, atualizar imediatamente a lista de planos.                                         |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                              |
|---------------|--------------|-------------------|---------------|------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano.                                                         |
| valor_diario  | Decimal (R$) | ^\d{1,5}(\,\d{2})?$ | 99999,99      | Valor por diária.                                                      |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Validade em dias.                                                      |
| status        | Booleano     | ^(ativo|inativo)$ | -             | Indica se o plano está ativo.                                           |
| descricao     | Texto Longo  | .*                | -             | Informações adicionais sobre o plano.                                 |
