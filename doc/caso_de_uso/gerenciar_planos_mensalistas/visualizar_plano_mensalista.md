## Caso de Uso: Visualizar Plano Mensalista

| Nome do Caso de Uso       | Visualizar Plano Mensalista                                                                                  |
|---------------------------|--------------------------------------------------------------------------------------------------------------|
| *Descrição*               | Permite ao administrador visualizar detalhes dos planos de mensalidade cadastrados no sistema (nome, valor, tipo, validade, status).               |
| *Ator Envolvido*          | Administrador                                                                                               |

| *Interação entre Ator e Sistema*       |                                                                                                         |
|----------------------------------------|---------------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                               |
| Acessa o menu de administração.        | Exibe opções de gerenciamento. *(RI01)*                                                                 |
| Seleciona "Gerenciar Planos".           | Lista os planos existentes em formato de tabela. *(RI01)*                                               |
| Visualiza informações do plano. | Exibe os dados conforme cadastrado. *(RI01)*                                                            |

| *Exceções*                                                                                           |
|------------------------------------------------------------------------------------------------------|
| EX01 - Nenhum plano cadastrado. O sistema exibe uma mensagem informando ausência de dados.            |

| *Alternativas*                                                                                       |
|------------------------------------------------------------------------------------------------------|
| AL01 - Pode aplicar filtros ou ordenações para localizar planos mais facilmente.                    |

| *Regras de Negócio*                                                                                   |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Deve exibir todos os planos ativos e inativos com informações básicas.                         |
| RN02 - Exibir status atualizado dos planos (ativo/inativo).                                           |

| *Requisitos de Interface com o Usuário*                                                               |
|--------------------------------------------------------------------------------------------------------|
| RI01 - Exibir a lista de planos em formato de tabela com dados principais.                            |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                                 |
|---------------|--------------|-------------------|---------------|---------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano. |
| valor         | Decimal (R$) | ^\d{1,5}(,\d{2})?$  | 99999,99      | Valor monetário do plano. |
| tipo          | Texto        | ^(Mensal|Anual|Semestral)$ | -     | Tipo de plano. |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Validade em dias. |
| status        | Booleano     | ^(ativo|inativo)$ | -             | Indica se o plano está ativo ou inativo. |
