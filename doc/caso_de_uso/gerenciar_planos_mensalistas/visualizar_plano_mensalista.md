## Caso de Uso: Excluir Plano Mensalista

| Nome do Caso de Uso       | Excluir Plano Mensalista                                                                                        |
|---------------------------|-----------------------------------------------------------------------------------------------------------------|
| *Descrição*               | Permite ao administrador excluir um plano de mensalidade cadastrado, desde que não esteja associado a clientes ativos. |
| *Ator Envolvido*          | Administrador                                                                                                  |

| *Interação entre Ator e Sistema*       |                                                                                                         |
|----------------------------------------|--------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                               |
| Acessa o menu de administração.        | Exibe as opções de gerenciamento. *(RI01)*                                                              |
| Seleciona "Gerenciar Planos".           | Lista os planos existentes em formato de tabela. *(RI01)*                                                |
| Clica em "Excluir" no plano desejado.   | Solicita confirmação da exclusão. *(RI03)*                                                              |
| Confirma a exclusão. | Válida se o plano pode ser excluído e remove do sistema. *(RN01, EX01, AL01, RI02, RI03)*                    |

| *Exceções*                                                                                             |
|--------------------------------------------------------------------------------------------------------|
| EX01 - Tentativa de excluir um plano associado a clientes ativos. O sistema exibe mensagem de impedimento. |
| EX02 - Plano já excluído ou inexistente. O sistema informa que a ação não é possível.                   |

| *Alternativas*                                                                                         |
|--------------------------------------------------------------------------------------------------------|
| AL01 - O administrador pode cancelar a ação de exclusão antes da confirmação, retornando à tela anterior. |

| *Regras de Negócio*                                                                                     |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Um plano só pode ser excluído se não estiver associado a clientes ativos.                        |
| RN02 - Exclusões devem ser registradas no histórico de alterações.                                       |

| *Requisitos de Interface com o Usuário*                                                                 |
|--------------------------------------------------------------------------------------------------------|
| RI01 - Listar planos com opções de "Editar" e "Excluir".                                                |
| RI02 - Exibir janela/modal para confirmação da exclusão.                                                |
| RI03 - Exibir mensagens claras para sucesso ou erro da operação.                                        |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                                 |
|---------------|--------------|-------------------|---------------|---------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano a ser excluído. |
| status        | Booleano     | ^(ativo \| inativo)$ | -            | Indica se o plano está ativo ou inativo (controle de exclusão lógica). |
| clientes_assosciado | Booleano | ^(sim|não)$      | -             | Indica se o plano está vinculado a clientes ativos. |
| data_exclusao | Data         | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa   | Data de exclusão, se aplicável. |
| excluido_por  | Texto        | ^[A-Za-z0-9]{3,30}$ | -             | Identificador do usuário que realizou a exclusão. |
