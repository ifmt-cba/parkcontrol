## Caso de Uso: Editar Plano Mensalista

| Nome do Caso de Uso       | Editar Plano Mensalista                                                                                   |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| *Descrição*               | Permite ao administrador editar os dados de um plano de mensalidade já existente no sistema.              |
| *Ator Envolvido*          | Administrador                                                                                            |

| *Interação entre Ator e Sistema*       |                                                                                                         |
|----------------------------------------|---------------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                               |
| Acessa o menu de administração.        | Exibe as opções de gerenciamento. *(RI01)*                                                              |
| Seleciona "Gerenciar Planos".           | Exibe lista dos planos cadastrados. *(RI01)*                                                             |
| Clica em "Editar" no plano desejado.    | Exibe o formulário preenchido com dados atuais do plano. *(RI02)*                                        |
| Altera os campos necessários e confirma. | Valida alterações e salva as atualizações. *(RN01, RN02, RN03, EX01, EX02, AL01, RI02, RI03)*                        |
| Termina a edição.                      | Retorna à tela de gerenciamento sem alterar os dados. *(AL02)*                                          |

| *Exceções*                                                                                           |
|------------------------------------------------------------------------------------------------------|
| EX01 - Tentativa de editar um plano inexistente. O sistema exibe uma mensagem de erro.               |
| EX02 - Dados obrigatórios não preenchidos. O sistema solicita correção.                             |

| *Alternativas*                                                                                       |
|------------------------------------------------------------------------------------------------------|
| AL01 - Administrador pode corrigir dados inválidos e tentar novamente.                                                    |
| AL02 - Pode cancelar a edição, retornando à tela inicial sem alterações.                                                      |

| *Regras de Negócio*                                                                                   |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Alterações devem manter o nome único do plano.                                                 |
| RN02 - A validade e o valor devem seguir os padrões definidos.                                        |
| RN03 - O sistema deve registrar a data da última alteração.                                           |

| *Requisitos de Interface com o Usuário*                                                               |
|--------------------------------------------------------------------------------------------------------|
| RI01 - Listar planos com botões de "Editar" e "Excluir".                                              |
| RI02 - Formulário de edição com campos pré-preenchidos e validados.                                   |
| RI03 - Exibir mensagem de sucesso ou erro após tentativa de edição.                                   |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                                 |
|---------------|--------------|-------------------|---------------|---------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano. Obrigatório. |
| valor         | Decimal (R$) | ^\d{1,5}(,\d{2})?$  | 99999,99      | Valor do plano. Obrigatório. |
| tipo          | Texto        | ^(Mensal|Anual|Semestral)$ | -     | Tipo de plano. Obrigatório. |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Validade do plano em dias. Obrigatório. |
| descrição     | Texto Longo  | .*                | -             | Descrição adicional do plano. Opcional. |
| status        | Booleano     |^(ativo \| inativo)$| -             | Indica se o plano está ativo. |
| data_criacao  | Data         | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa   | Data de criação do plano. |
| ultima_alteracao | DataHora | ^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}$ | dd/mm/aaaa hh:mm:ss | Última alteração feita. |
| criado_por    | Texto        | ^[A-Za-z0-9]{3,30}$ | -           | Usuário que criou o plano. |
