## Caso de Uso: Criar Plano Mensalista

| Nome do Caso de Uso       | Criar Plano Mensalista                                                                                     |
|---------------------------|------------------------------------------------------------------------------------------------------------|
| *Descrição*               | Este caso de uso permite ao administrador cadastrar um novo plano de mensalidade no sistema, informando nome, valor, validade e tipo do plano. |
| *Ator Envolvido*          | Administrador                                                                                              |

| *Interação entre Ator e Sistema*       |                                                                                                           |
|----------------------------------------|-----------------------------------------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                                                 |
| Acessa o menu de administração.        | Exibe as opções de gerenciamento. *(RI01)*|
| Seleciona a opção "Gerenciar Planos". | Carrega a tela com os planos cadastrados. *(RI01)*|
| Clica em "Novo Plano".                 | Exibe o formulário para cadastro de plano. *(RI02)*|
| Preenche os dados do plano e confirma. | Valida os dados e salva o novo plano no sistema. *(RN01, RN03, EX01, EX02, AL01, RI02, RI03)*|
| Cancela o cadastro.                   | O sistema retorna à tela de gerenciamento de planos. *(AL02)*|

| *Exceções*                                                                                      |
|--------------------------------------------------------------------------------------------------|
| EX01 - Dados obrigatórios não preenchidos. O sistema exibe uma mensagem de erro.                |
| EX02 - Tentativa de salvar plano com nome duplicado. O sistema exibe notificação de erro.        |

| *Alternativas*                                                                                       |
|--------------------------------------------------------------------------------------------------------|
| AL01 - O administrador pode corrigir dados inválidos e tentar novamente.                              |
| AL02 - O administrador pode cancelar o cadastro a qualquer momento. Retorna à tela de gerenciamento.  |

| *Regras de Negócio*                                                                                   |
|--------------------------------------------------------------------------------------------------------|
| RN01 - Todo plano deve possuir um nome único e valor definido.                                         |
| RN02 - O sistema deve armazenar a data de criação e a última alteração do plano.                      |

| *Requisitos de Interface com o Usuário*                                                               |
|--------------------------------------------------------------------------------------------------------|
| RI01 - O sistema deve exibir os planos em forma de tabela com opções de "Editar" e "Excluir".         |
| RI02 - O formulário de cadastro deve conter campos claros e validados para nome, valor, tipo e validade. |
| RI03 - Após salvar, deve exibir mensagem visual de sucesso ou erro.                                   |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara       | Descrição                                                                 |
|---------------|--------------|-------------------|---------------|---------------------------------------------------------------------------|
| nome          | Texto        | ^[A-Za-z0-9\s]{3,50}$ | -           | Nome do plano. Obrigatório. Deve conter entre 3 e 50 caracteres alfanuméricos. |
| valor         | Decimal (R$) | ^\d{1,5}(,\d{2})?$  | 99999,99      | Valor monetário do plano. Obrigatório. Deve ser positivo e com duas casas decimais. |
| tipo          | Texto        | ^(Mensal|Anual|Semestral)$ | -     | Tipo do plano (Mensal, Anual, Semestral). Obrigatório.                       |
| validade      | Número inteiro | ^\d{1,3}$        | -             | Duração do plano em dias. Obrigatório. Deve ser maior que 0.               |
| descrição     | Texto Longo  | .*                | -             | Campo opcional para descrição adicional do plano. Sem restrições rígidas.  |
| status        | Booleano     | ^(ativo \| inativo)$| -             | Indica se o plano está ativo ou não. Controle de exclusão lógica.           |
| data_criacao  | Data         | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa   | Data em que o plano foi cadastrado. Gerado automaticamente pelo sistema.   |
| ultima_alteracao | DataHora | ^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}$ | dd/mm/aaaa hh:mm:ss | Data e hora da última edição. Gerado automaticamente. |
| criado_por    | Texto        | ^[A-Za-z0-9]{3,30}$ | -           | Identificador do usuário que criou o plano. Registrado automaticamente.    |
