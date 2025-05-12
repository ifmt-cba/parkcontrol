## Caso de Uso: Editar Plano Diarista

| Nome do Caso de Uso       | Editar Plano Diarista                                                                                        |
|---------------------------|-------------------------------------------------------------------------------------------------------------|
| *Descrição*               | Permite ao administrador alterar dados de um plano de diária cadastrado, como nome, valor ou validade.     |
| *Ator Envolvido*          | Administrador                                                                                                |

| *Interação entre Ator e Sistema*       |                                                                                                         |
|----------------------------------------|---------------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                               |
| Acessa o menu de administração.        | Exibe opções de gerenciamento. *(RI01)*                                                                 |
| Seleciona "Gerenciar Planos Diaristas". | Lista os planos disponíveis. *(RI01)*                                                                   |
| Clica em "Editar" no plano desejado.    | Carrega o formulário com dados atuais. *(RI02)*                                                         |
| Altera os dados e confirma.             | Valida e atualiza o plano no sistema. *(RN01, RN02, RN03, EX01, RI02, RI03)*                             |

| *Exceções*                                                                                             |
|--------------------------------------------------------------------------------------------------------|
| EX01 - Dados obrigatórios não preenchidos. O sistema emite erro.                                        |
| EX02 - Tentativa de editar plano inexistente.                                                           |

| *Alternativas*                                                                                         |
|--------------------------------------------------------------------------------------------------------|
| AL01 - O administrador pode cancelar a edição a qualquer momento, retornando sem alterações.           |

| *Regras de Negócio*                                                                                     |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Nome do plano deve continuar único.                                                              |
| RN02 - Toda edição deve ser registrada no histórico.                                                    |
| RN03 - Apenas administradores autorizados podem editar planos.                                          |

| *Requisitos de Interface com o Usuário*                                                                 |
|--------------------------------------------------------------------------------------------------------|
| RI01 - Listagem clara dos planos.                                                                       |
| RI02 - Formulário de edição com pré-preenchimento dos dados.                                             |
| RI03 - Mensagens de confirmação após editar.                                                            |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                              |
|---------------|--------------|-------------------|---------------|------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano. Obrigatório.                                            |
| valor_diario  | Decimal (R$) | ^\d{1,5}(\,\d{2})?$ | 99999,99      | Valor por diária. Obrigatório.                                          |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Validade do plano em dias. Obrigatório.                                |
| status        | Booleano     | ^(ativo|inativo)$ | -             | Indica se o plano está ativo.                                           |
| descricao     | Texto Longo  | .*                | -             | Descrição adicional do plano (opcional).                               |
