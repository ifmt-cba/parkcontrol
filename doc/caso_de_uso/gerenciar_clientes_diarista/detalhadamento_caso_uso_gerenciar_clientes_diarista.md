| Nome do Caso de Uso       | Gerenciar Cliente Diarista |
|---------------------------|-----------------------------|
| *Descrição*               | Permite o administrador e o frentista realizar a gestão de clientes diaristas, incluindo cadastro, visualização, edição e exclusão. |
| *Ator Envolvido*          | Administrador e Frentista  |

| *Interação entre Ator e Sistema*       |                                                  |
|----------------------------------------|--------------------------------------------------|
| *Ator*                                 | *Sistema*                                        |
| Acessa a opção “Clientes Diaristas”    | Exibe lista de clientes diaristas cadastrados (RI01, RN01) |
| Clica em “Novo Cliente”                | Exibe formulário de cadastro com campos obrigatórios: nome, placa, telefone (RI02) |
| Preenche os dados obrigatórios         | Valida preenchimento e cadastra cliente (RN02) |
| Seleciona um cliente existente         | Exibe opções para visualizar, editar ou excluir (RI03) |
| Edita dados de um cliente              | Sistema atualiza as informações (RN03) |
| Exclui um cliente                      | Sistema confirma e remove cliente (RN04) |
| Busca cliente pelo nome ou placa       | Filtra resultados conforme entrada (RN05) |
| Ocorre erro de conexão                 | Exibe mensagem de erro (EX01) |
| Tenta excluir cliente sem placa cadastrada | Bloqueia ação e alerta o usuário (EX02) |

| *Exceções* |
|------------|
| EX01 - Erro de conexão com o servidor: sistema informa falha e solicita tentar novamente. |
| EX02 - Tentativa de excluir cliente sem placa cadastrada: sistema impede e exibe alerta. |
| EX03 - Dados inválidos no cadastro (ex: telefone incorreto): sistema exibe erro de validação. |

| *Alternativas* |
|----------------|
| AL01 - Administrado e frentista cancela o cadastro ou edição antes de salvar. |
| AL02 - Administrador e frentista decide apenas visualizar sem alterar informações. |
| AL03 - Cliente cadastrado retorna à tela principal sem ação adicional. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Apenas clientes ativos são exibidos por padrão na listagem. |
| RN02 - Todos os campos obrigatórios devem ser preenchidos para cadastro. |
| RN03 - Edição só pode ocorrer se o cliente estiver ativo. |
| RN04 - Exclusão remove apenas os dados do cliente, mantendo os registros de passagem. |
| RN05 - Busca deve aceitar tanto nome quanto placa do veículo. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Tela de listagem de clientes com busca e filtros. |
| RI02 - Formulário de cadastro com validação de campos obrigatórios. |
| RI03 - Botões de ação (visualizar, editar, excluir) ao lado de cada cliente. |
| RI04 - Mensagens claras de confirmação para edição e exclusão. |

| Nome do Campo     | Tipo de Dado | Expressão Regular                  | Máscara           | Descrição                                             | Obrigatório | Único | Default                   |
|-------------------|--------------|------------------------------------|-------------------|-------------------------------------------------------|-------------|-------|----------------------------|
| nome              | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$              | -                 | Nome completo do cliente diarista.                   | Sim         | Não   | -                          |
| placa         | Texto        | ^([A-Z]{3}-\d{4} \| [A-Z]{3}\d[A-Z]\d{2})$ | AAA-0000 ou AAA0A00 | Placa do veículo (modelo antigo ou Mercosul). | Sim | Sim | - |
| telefone          | Texto        | ^\(\d{2}\)\s\d{4,5}-\d{4}$         | (00) 00000-0000   | Telefone de contato.                                 | Sim         | Não   | -                          |
| status            | Booleano        | ^ativo \| inativo)$                  | -                 | Indica se o cliente está ativo ou inativo.            | Sim         | Não   | ativo                      |
| data_cadastro     | Data          | ^\d{2}-\d{2}-\d{4}$                | dd/mm/aaaa         | Data do cadastro do cliente.                         | Sim         | Não   | Gerado automaticamente     |
| atualizado_por    | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$              | -                 | Funcionário responsável pela última atualização.     | Não         | Não   | Gerado automaticamente     |
