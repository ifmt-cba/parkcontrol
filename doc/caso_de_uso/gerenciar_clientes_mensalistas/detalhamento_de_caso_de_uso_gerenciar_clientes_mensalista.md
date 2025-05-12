| Nome do Caso de Uso       | Gerenciar Clientes Mensalistas |
|---------------------------|---------------------------------|
| *Descrição*               | Permitir que o administrador cadastre, edite, visualize ou exclua mensalistas no sistema de estacionamento. |
| *Ator Envolvido*          | Administrador |


| *Interação entre Ator e Sistema*       |                                                                                     |
|----------------------------------------|-----------------------------------------------------------|
| *Ator*                                 | *Sistema*                                                                          |
| Acessa o menu "Mensalistas"            | Exibe lista de clientes mensalistas cadastrados com opções: cadastrar, editar, excluir. (RN01, RN04, RI01) |
| Seleciona a opção "Cadastrar Mensalista" | Exibe formulário com campos obrigatórios: nome, CPF, telefone, e-mail, placa, plano contratado. (RI02) |
| Preenche os dados do novo cliente      | Valida dados conforme regras. (EX01, EX02, RN02, RN03) |
| Confirma o cadastro                    | Exibe mensagem de sucesso e salva o mensalista com status "ativo". Gera data_criacao. (RN04, RI03) |
| Seleciona mensalista na lista          | Exibe opções: visualizar, editar ou excluir. |
| Escolhe "Editar"                       | Exibe formulário com dados atuais preenchidos. |
| Altera os dados                        | Valida e atualiza o cadastro. Exibe confirmação. (EX02) |
| Escolhe "Excluir"                      | Solicita confirmação. Remove o mensalista e exibe aviso. (EX03, RN05) |


| *Exceções* |
|------------|
| EX01 - Campos obrigatórios não preenchidos: o sistema exibe mensagem de erro indicando quais campos faltam. |
| EX02 - CPF ou placa duplicados: o sistema informa que o CPF ou placa já estão cadastrados. |
| EX03 - Tentativa de excluir mensalista com pendência de pagamento: o sistema bloqueia a exclusão e exibe alerta "Erro ao excluir cliente: Dívida Pendente!". |


| *Alternativas* |
|----------------|
| AL01 - Caso o frentista cancele o cadastro/edição, o sistema retorna para a lista sem salvar alterações. |
| AL02 - O sistema pode permitir a busca de mensalistas por nome, CPF ou placa para facilitar a edição ou visualização. |


| *Regras de Negócio* |
|---------------------|
| RN01 - Apenas usuários com perfil "Frentista" ou superior podem gerenciar mensalistas. |
| RN02 - O CPF deve ser válido e único para cada cliente mensalista. |
| RN03 - Cada placa de veículo deve ser única no sistema. |
| RN04 - Todos os campos obrigatórios devem estar preenchidos para concluir o cadastro. |
| RN05 - Mensalistas com pendências financeiras não podem ser excluídos até a regularização. |


| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A lista de mensalistas deve ser paginada e conter filtros por nome, CPF e placa. |
| RI02 - O formulário de cadastro/edição deve destacar visualmente os campos obrigatórios. |
| RI03 - Após cadastro, o sistema deve exibir mensagem de sucesso com data e horário de criação. |


| Nome do Campo     | Tipo de Dado | Expressão Regular                  | Máscara           | Descrição                                             | Obrigatório | Único | Default                   |
|-------------------|--------------|------------------------------------|-------------------|-------------------------------------------------------|-------------|-------|----------------------------|
| nome              | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$              | -                 | Nome completo do cliente                             | Sim         | Não   | -                          |
| cpf               | Texto        | ^\d{3}\.\d{3}\.\d{3}\-\d{2}$       | 000.000.000-00     | CPF válido do cliente                                | Sim         | Sim   | -                          |
| telefone          | Texto        | ^\(?\d{2}\)?[\s-]?\d{4,5}-\d{4}$   | (00) 00000-0000   | Telefone para contato                                | Sim         | Não   | -                          |
| email             | Texto        | ^[\w\.-]+@[\w\.-]+\.\w{2,}$        | -                 | E-mail válido e único                                | Sim         | Sim   | -                          |
| placa         | Texto        | `^([A-Z]{3}-\d{4} \|  [A-Z]{3}\d[A-Z]\d{2})$` | AAA-0000 ou AAA0A00 | Placa do veículo (modelo antigo ou Mercosul). | Sim | Sim | - |
| plano             | Texto        | ^(Básico or Integral or Noturno or Empresarial)$   | -                 | Tipo de plano contratado pelo cliente                | Sim         | Não   | Básico                    |
| status            | Booleano     | ^(ativo \| inativo)$                  | -                 | Situação atual do cliente mensalista                 | Não         | Não   | ativo                     |
| data_criacao      | Data         | ^\d{4}-\d{2}-\d{2}$                | aaaa-mm-dd        | Data de criação do cadastro                          | Sim         | Não   | Gerado automaticamente     |
