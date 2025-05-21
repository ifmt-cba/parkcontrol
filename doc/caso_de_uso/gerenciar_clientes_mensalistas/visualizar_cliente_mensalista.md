| Nome do Caso de Uso       | Visualizar Cliente Mensalista |
|---------------------------|-------------------------------|
| *Descrição*               | Permite o administrador e o frentista acessar os dados de um cliente mensalista cadastrado. |
| *Ator Envolvido*          | Administrador e Frentista |

| *Interação entre Ator e Sistema*       |                                                  |
|----------------------------------------|--------------------------------------------------|
| *Ator*                                 | *Sistema*                                        |
| Seleciona a opção “Clientes Mensalistas” no menu | Exibe lista de clientes mensalistas cadastrados (RI01, RN01, RN02) |
| Utiliza campo de busca                 | Filtra clientes pelo nome conforme digitado (RI01, RN03, AL02) |
| Escolhe um cliente na lista            | Exibe os dados detalhados do cliente selecionado (RI02) |
| Não há clientes cadastrados            | Sistema exibe mensagem e retorna ao menu principal (EX01) |
| Erro ao buscar dados                   | Sistema informa falha de conexão (EX02) |
| Dados de algum cliente estão corrompidos | Sistema não exibe cliente e mostra aviso (EX03) |
| Sai da tela sem selecionar cliente     | Sistema retorna ao menu (AL01) |
| Exporta a lista de clientes            | Sistema gera arquivo PDF da listagem (AL03) |

| *Exceções* |
|------------|
| EX01 - Nenhum cliente mensalista cadastrado: sistema exibe mensagem de aviso e retorna ao menu principal. |
| EX02 - Falha de conexão com o banco de dados: sistema exibe mensagem de erro e solicita nova tentativa. |
| EX03 - Dados corrompidos ou incompletos no cadastro: sistema exibe aviso e oculta cliente da lista. |

| *Alternativas* |
|----------------|
| AL01 - Administrador e o frentista retorna ao menu sem visualizar detalhes de nenhum cliente. |
| AL02 - Administrador e o frentista realiza nova busca após resultado anterior sem correspondência. |
| AL03 - Administrador e o frentista opta por exportar a lista de clientes visualizados em PDF. |

| *Regras de Negócio* |
|---------------------|
| RN01 - O sistema deve exibir todos os clientes cadastrados, ordenados por nome. |
| RN02 - Clientes com status “inativo” devem ser exibidos com destaque visual (ex: cor cinza). |
| RN03 - A busca por nome deve ignorar acentos e caixa (maiúscula/minúscula). |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Lista com nomes dos clientes mensalistas deve permitir busca por nome. |
| RI02 - Tela de detalhes deve apresentar nome, CPF, e-mail, placa e status. |

| Nome do Campo     | Tipo de Dado | Expressão Regular                  | Máscara           | Descrição                                             | Obrigatório | Único | Default                   |
|-------------------|--------------|------------------------------------|-------------------|-------------------------------------------------------|-------------|-------|----------------------------|
| nome              | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$              | -                 | Nome completo do cliente.                            | Sim         | Não   | -                          |
| cpf               | Texto        | ^\d{3}\.\d{3}\.\d{3}-\d{2}$        | 000.000.000-00    | CPF do cliente.                                      | Sim         | Sim  | -                          |
| email             | Texto        | ^[\w\.-]+@[\w\.-]+\.\w{2,}$        | -                 | E-mail para contato.                                 | Sim         | Sim  | -                          |
| placa         | Texto        | `^([A-Z]{3}-\d{4}or^([A-Z]{3}-\d{4} \| [A-Z]{3}\d[A-Z]\d{2})$` | AAA-0000 ou AAA0A00 | Placa do veículo (modelo antigo ou Mercosul). | Sim | Sim | - |
| status            | Booleano     | ^(ativo \| inativo)$                  | -                 | Indica se o cliente está ativo no sistema.           | Sim         | Não   | ativo                      |
