| Nome do Caso de Uso       | Gerenciar Planos                                                                                     |
|---------------------------|------------------------------------------------------------------------------------------------------|
| *Descrição*               | Este caso de uso permite ao administrador cadastrar, editar ou remover planos de mensalidade oferecidos pelo estacionamento, definindo valores, duração e condições dos planos. |
| *Ator Envolvido*          | Administrador                                                                                         |

| *Interação entre Ator e Sistema*       |                                                                                                         |
|----------------------------------------|---------------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                               |
| Acessa o menu de administração.        | Exibe as opções de gerenciamento. *(RI01)*                                                              |
| Seleciona a opção "Gerenciar Planos". | Carrega a tela com os planos cadastrados. *(RI01)*                                                      |
| Clica em "Novo Plano".                 | Exibe um formulário para cadastro de plano. *(RI02)*                                                    |
| Preenche os dados do plano (nome, valor, tipo, validade, etc) e confirma. | Valida os dados e salva o plano no sistema. *(RN01, RN03, EX01, AL02, RI02, RI03)*          |
| Pode cancelar o cadastro durante o preenchimento do formulário. | O sistema retorna à tela inicial de gerenciamento. *(AL01)*                                             |
| Pode também editar ou excluir planos existentes. | Atualiza ou remove os dados conforme ação escolhida. *(EX02, RN02, RN03, RI01, RI03)*        |

| *Exceções*                                                                                      |
|--------------------------------------------------------------------------------------------------|
| EX01 - Dados obrigatórios do plano não preenchidos. O sistema exibe uma mensagem de erro.       |
| EX02 - Tentativa de editar ou excluir um plano inexistente. O sistema exibe uma notificação de erro. |

| *Alternativas*                                                                                       |
|--------------------------------------------------------------------------------------------------------|
| AL01 - O administrador pode cancelar o cadastro a qualquer momento. O sistema retorna à tela inicial de gerenciamento. |
| AL02 - Ao tentar salvar um plano com nome duplicado, o sistema pode sugerir a edição do plano já existente. |

| *Regras de Negócio*                                                                                   |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Todo plano deve possuir um nome único e um valor definido.                                     |
| RN02 - Planos só podem ser excluídos se não estiverem associados a clientes ativos.                   |
| RN03 - O sistema deve armazenar um histórico de alterações feitas nos planos.                         |

| *Requisitos de Interface com o Usuário*                                                               |
|--------------------------------------------------------------------------------------------------------|
| RI01 - O sistema deve exibir os planos em forma de tabela com opções de "Editar" e "Excluir".         |
| RI02 - O formulário de cadastro deve conter campos claros e validados para nome, valor e duração.     |
| RI03 - Ao confirmar a ação, deve haver uma mensagem visual de sucesso ou erro.                        |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                                 |
|---------------|--------------|-------------------|---------------|---------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano. Obrigatório. Deve conter entre 3 e 50 caracteres alfanuméricos. |
| valor         | Decimal (R$) | ^\d{1,5}(\,\d{2})?$ | 99999,99      | Valor monetário do plano. Obrigatório. Deve ser positivo e com duas casas decimais. |
| tipo          | Texto        | ^(Mensal|Anual|Semestral)$ | -     | Tipo do plano (ex: Mensal, Anual). Opcional. Pode ser uma lista pré-definida. |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Duração do plano em dias. Obrigatório. Deve ser maior que 0.               |
| descrição     | Texto Longo  | .*                | -             | Campo opcional para descrição adicional do plano. Sem restrições rígidas.  |
| status        | Booleano     | ^(ativo|inativo)$ | -             | Indica se o plano está ativo ou não. Utilizado para controle de exclusão lógica. |
| data_criacao  | Data         | ^\d{4}-\d{2}-\d{2}$ | dd/mm/aaaa   | Data em que o plano foi cadastrado. Gerado automaticamente pelo sistema. |
| ultima_alteracao | DataHora | ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$ | dd/mm/aaaa hh:mm:ss | Data e hora da última edição. Gerado automaticamente pelo sistema. |
| criado_por    | Texto        | ^[A-Za-z0-9]{3,30}$ | -           | Identificador do usuário que criou o plano. Registrado automaticamente.    |

