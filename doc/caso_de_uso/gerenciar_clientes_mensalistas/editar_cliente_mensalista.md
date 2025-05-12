| Nome do Caso de Uso       | Editar Cliente Mensalista |
|---------------------------|---------------------------|
| *Descrição*               | Permite o administrador e o frentista editar os dados de um cliente mensalista já cadastrado. |
| *Ator Envolvido*          | Administrador e Frentista  |

| *Interação entre Ator e Sistema*       |                                                   |
|----------------------------------------|---------------------------------------------------|
| *Ator*                                 | *Sistema*                                         |
| Acessa a opção “Clientes Mensalistas” no menu | Exibe lista de clientes cadastrados (RI01, RN01)         |
| Busca o cliente desejado               | Filtra resultados conforme entrada (RI01, RN03)           |
| Clica no botão “Editar” ao lado do cliente | Exibe formulário com dados atuais preenchidos (RI02)      |
| Altera os dados necessários            | Valida os novos dados inseridos (RN04, RN05)             |
| Confirma a edição                      | Atualiza o cadastro no sistema e exibe mensagem de sucesso (RN06) |
| Cancela a edição                       | Retorna à tela anterior sem salvar alterações (AL01)     |
| Insere dados inválidos                 | Exibe mensagens de erro e impede salvamento (EX01, RN04) |
| Ocorre falha de conexão                | Exibe mensagem de erro e não salva dados (EX02)          |
| Cadastra e-mail já usado por outro cliente | Exibe aviso de duplicidade (EX03, RN05)                  |

| *Exceções* |
|------------|
| EX01 - Dados inválidos inseridos: o sistema exibe mensagens indicando os campos com erro. |
| EX02 - Falha de conexão com o banco de dados: sistema exibe mensagem e não salva alterações. |
| EX03 - E-mail ou CPF já cadastrado para outro cliente: sistema exibe aviso de duplicidade e bloqueia a edição. |

| *Alternativas* |
|----------------|
| AL01 - Administrador e frentista cancela a edição antes de salvar, retornando à tela anterior. |
| AL02 - Administrador e frentista apaga todos os campos e decide não preencher nenhum (sistema alerta e bloqueia ação). |
| AL03 - Administrador e frentista altera somente parte dos dados, mantendo o restante inalterado. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Apenas clientes com status "ativo" podem ser editados. |
| RN03 - A busca por cliente deve desconsiderar acentuação e caixa. |
| RN04 - Todos os campos obrigatórios devem ser validados antes da edição. |
| RN05 - E-mail e CPF devem ser únicos no sistema. |
| RN06 - Após salvar, o sistema deve registrar a alteração com data/hora. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Tela de busca deve permitir localizar clientes por nome. |
| RI02 - Formulário de edição deve exibir os dados atuais do cliente. |
| RI03 - Mensagens de erro devem indicar o campo específico e a causa do erro. |

| Nome do Campo     | Tipo de Dado | Expressão Regular                  | Máscara           | Descrição                                             | Obrigatório | Único | Default                   |
|-------------------|--------------|------------------------------------|-------------------|-------------------------------------------------------|-------------|-------|----------------------------|
| nome              | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$              | -                 | Nome completo do cliente.                            | Sim         | Não   | -                          |
| cpf               | Texto        | ^\d{3}\.\d{3}\.\d{3}-\d{2}$        | 000.000.000-00    | CPF do cliente.                                      | Sim         | Sim  | -                          |
| email             | Texto        | ^[\w\.-]+@[\w\.-]+\.\w{2,}$        | -                 | E-mail para contato.                                 | Sim         | Sim  | -                          |
| placa         | Texto        | ^([A-Z]{3}-\d{4} \| [A-Z]{3}\d[A-Z]\d{2})$ | AAA-0000 ou AAA0A00 | Placa do veículo (modelo antigo ou Mercosul). | Sim | Sim | - |
| status            | Booleano     | ^(ativo \|inativo)$                  | -                 | Indica se o cliente está ativo no sistema.           | Sim         | Não
