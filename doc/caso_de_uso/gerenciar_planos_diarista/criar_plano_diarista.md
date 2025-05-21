## Caso de Uso: Criar Plano Diarista

| Nome do Caso de Uso       | Criar Plano Diarista                                                                                       |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| *Descrição*               | Permite ao administrador cadastrar novos planos de diária para o estacionamento, definindo valor a hora e condições. |
| *Ator Envolvido*          | Administrador                                                                                             |

| *Interação entre Ator e Sistema*       |                                                                                                          |
|----------------------------------------|----------------------------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                                |
| Acessa o menu de administração.        | Exibe as opções de gerenciamento. *(RI01)*                                                               |
| Seleciona "Gerenciar Planos Diaristas". | Lista os planos existentes. *(RI01)*                                                                     |
| Clica em "Novo Plano".                  | Exibe o formulário de cadastro. *(RI02)*                                                                 |
| Preenche dados do plano (nome, valor diário, validade, etc) e confirma. | Valida e salva o plano no sistema. *(RN01, RN02, RN03, EX01, AL02, RI02, RI03)*          |
| Cancelar ação de cadastro.              | Retorna à tela inicial sem salvar. *(AL01)*                                                              |

| *Exceções*                                                                                             |
|--------------------------------------------------------------------------------------------------------|
| EX01 - Dados obrigatórios do plano não preenchidos. O sistema exibe mensagem de erro.                  |
| EX02 - Tentativa de criar plano com nome já existente. O sistema exibe aviso de duplicidade.            |

| *Alternativas*                                                                                         |
|--------------------------------------------------------------------------------------------------------|
| AL01 - O administrador pode cancelar a qualquer momento.                                               |
| AL02 - Em caso de nome duplicado, sistema sugere edição do plano existente.                             |

| *Regras de Negócio*                                                                                     |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Todo plano deve ter nome único e valor diário definido.                                          |
| RN02 - Planos podem ser criados apenas se não existirem nomes idênticos.                                |
| RN03 - Alterações de planos devem ser registradas no histórico.                                         |

| *Requisitos de Interface com o Usuário*                                                                 |
|--------------------------------------------------------------------------------------------------------|
| RI01 - Exibir tabela de planos existentes.                                                             |
| RI02 - Exibir formulário de cadastro com validações obrigatórias.                                      |
| RI03 - Confirmar ações com mensagens visuais.                                                          |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                              |
|---------------|--------------|-------------------|---------------|------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano. Obrigatório.                                            |
| valor_diario  | Decimal (R$) | ^\d{1,5}(\,\d{2})?$ | 99999,99      | Valor por diária. Obrigatório.                                          |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Validade do plano em dias. Obrigatório.                                |
| status        | Booleano     | ^(ativo\|inativo)$ | -             | Indica se o plano está ativo.                                           |
| descricao     | Texto Longo  | .*                | -             | Descrição adicional do plano (opcional).                               |
