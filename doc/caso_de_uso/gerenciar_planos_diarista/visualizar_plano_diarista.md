## Caso de Uso: Visualizar Plano Diarista

| Nome do Caso de Uso       | Visualizar Plano Diarista                                                                               |
|---------------------------|---------------------------------------------------------------------------------------------------------|
| *Descrição*               | Permite ao administrador consultar a lista de planos de diária cadastrados no sistema.                  |
| *Ator Envolvido*          | Administrador                                                                                           |

| *Interação entre Ator e Sistema*       |                                                                                                         |
|----------------------------------------|---------------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                               |
| Acessa o menu de administração.        | Exibe opções de gerenciamento. *(AL01, RI01, RI02, RN01)*                                                                 |
| Seleciona "Gerenciar Planos Diaristas". | Lista todos os planos disponíveis. *(RI01, EX01)*                                                             |
| Visualiza detalhes dos planos.          | Exibe informações como nome, valor, validade e status. *(RI02, RN02)*                                          |

| *Exceções*                                                                                             |
|--------------------------------------------------------------------------------------------------------|
| EX01 - Nenhum plano encontrado. O sistema exibe uma mensagem informativa.                             |

| *Alternativas*                                                                                         |
|--------------------------------------------------------------------------------------------------------|
| AL01 - Caso não existam planos cadastrados, o sistema permite cadastrar um novo diretamente da tela.   |

| *Regras de Negócio*                                                                                     |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Somente administradores autorizados podem visualizar planos.                                    |
| RN02 - Todas as informações exibidas devem ser atualizadas em tempo real.                              |

| *Requisitos de Interface com o Usuário*                                                                 |
|--------------------------------------------------------------------------------------------------------|
| RI01 - Exibir lista em formato de tabela, com filtros por nome e status.                               |
| RI02 - Permitir acesso rápido a opções de editar ou excluir planos.                                    |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                              |
|---------------|--------------|-------------------|---------------|------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano.                                                         |
| valor_diario  | Decimal (R$) | ^\d{1,5}(\,\d{2})?$ | 99999,99      | Valor por diária.                                                      |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Validade em dias.                                                      |
| status        | Booleano     | ^(ativo\|inativo)$ | -             | Indica se o plano está ativo.                                           |
| descricao     | Texto Longo  | .*                | -             | Informações adicionais sobre o plano.                                 |
