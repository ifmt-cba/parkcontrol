| Nome do Caso de Uso       | Excluir Cliente Mensalista |
|---------------------------|-----------------------------|
| *Descrição*               | Permite o administrador  excluir um cliente mensalista do sistema. |
| *Ator Envolvido*          | Administrador  |

| *Interação entre Ator e Sistema*       |                                                    |
|----------------------------------------|----------------------------------------------------|
| *Ator*                                 | *Sistema*                                          |
| Acessa a opção “Clientes Mensalistas”  | Exibe lista de clientes cadastrados (RI01, RN01)  |
| Busca o cliente desejado               | Exibe cliente filtrado conforme entrada (RI01, RN02) |
| Clica no botão “Excluir” ao lado do cliente | Exibe caixa de confirmação da exclusão (RI02)        |
| Confirma a exclusão                    | Remove o cliente do sistema (RN03), registra log da exclusão (RN04) |
| Cancela a exclusão                     | Retorna à tela anterior sem alterar nada (AL01)    |
| Tenta excluir cliente já inativo       | Exibe mensagem informando que o cliente já está inativo (EX01) |
| Ocorre falha de conexão ou banco       | Exibe mensagem de erro e não realiza exclusão (EX02) |

| *Exceções* |
|------------|
| EX01 - Cliente já está inativo: sistema impede a exclusão e exibe aviso. |
| EX02 - Erro de conexão com o banco de dados: sistema exibe mensagem de falha. |
| EX03 - Cliente com cobranças pendentes: sistema bloqueia exclusão e alerta o usuário. |

| *Alternativas* |
|----------------|
| AL01 - Administrador cancela a exclusão após abrir a confirmação. |
| AL02 - Administrador realiza nova busca e exclui outro cliente. |
| AL03 - Exclusão realizada parcialmente: sistema salva log, mas falha ao atualizar interface. |

| *Regras de Negócio* |
|---------------------|
| RN01 - A listagem de clientes deve mostrar apenas os ativos por padrão. |
| RN02 - A busca deve aceitar nome, e-mail ou CPF. |
| RN03 - Clientes excluídos são marcados como "inativos", sem perder histórico. |
| RN04 - Toda exclusão deve ser registrada com data, hora e usuário responsável. |
| RN05 - Clientes com pendências financeiras não podem ser excluídos. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Interface deve ter campo de busca por nome, e-mail ou CPF. |
| RI02 - Botão de “Excluir” deve solicitar confirmação com mensagem clara. |
| RI03 - Mensagens de erro devem indicar o motivo exato do bloqueio da exclusão. |

| Nome do Campo     | Tipo de Dado | Expressão Regular                  | Máscara           | Descrição                                             | Obrigatório | Único | Default                   |
|-------------------|--------------|------------------------------------|-------------------|-------------------------------------------------------|-------------|-------|----------------------------|
| nome              | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$              | -                 | Nome do cliente.                                      | Sim         | Não   | -                          |
| cpf               | Texto        | ^\d{3}\.\d{3}\.\d{3}-\d{2}$        | 000.000.000-00    | CPF único do cliente.                                | Sim         | Sim  | -                          |
| email             | Texto        | ^[\w\.-]+@[\w\.-]+\.\w{2,}$        | -                 | E-mail do cliente.                                   | Sim         | Sim  | -                          |
| status            | Booleano        | ^(ativo \|inativo)$                  | -                 | Indica se o cliente está ativo ou inativo.           | Sim         | Não   | ativo                      |
| data_exclusao     | Data         | ^\d{2}-\d{2}-\d{4}$                | dd/mm/aaaa        | Data em que o cliente foi excluído.                  | Não         | Não   | Gerado automaticamente     |
| excluido_por      | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$              | -                 | Nome do funcionário que realizou a exclusão.         | Não         | Não   | Gerado automaticamente     |
