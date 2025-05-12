| Nome do Caso de Uso | Solicitar Manutenção |
|---------------------|-----------------------|
| **Descrição** | Permite que o frentista solicite manutenção em uma vaga de estacionamento ao identificar um problema físico, como buracos, goteiras, rachaduras, entre outros. A solicitação inclui a descrição do problema e localização da vaga. Um número de protocolo único é gerado para controle e acompanhamento. |
| **Ator Envolvido** | Frentista |

| **Ator** | **Sistema** |
|----------|-------------|
| Acessa o menu de "Manutenção" | Exibe o formulário de solicitação de manutenção. (RI01) |
| Preenche os dados da solicitação (descrição do problema, local da vaga) | Valida os campos obrigatórios. (EX01, RN01, RI02) |
| Envia a solicitação | Armazena a solicitação, gera número de protocolo e exibe confirmação do envio.(AL01, RN02, RI03) |

| **Exceções** |
|--------------|
| **EX01** - Campos obrigatórios não preenchidos: sistema exibe mensagem de erro solicitando o preenchimento antes do envio. |

| **Alternativas** |
|------------------|
| **AL01** - Se o problema já tiver sido reportado, o sistema informa que uma solicitação de manutenção já está em andamento para a vaga. |

| **Regras de Negócio** |
|------------------------|
| **RN01** - Toda solicitação de manutenção deve conter a identificação da vaga ou do local exato do problema. |
| **RN02** - O sistema deve gerar um número único de protocolo para cada solicitação. |

## Requisitos de Interface com o Usuário

| **Requisitos de Interface com o Usuário** |
|--------------------------------------------|
| **RI01** - O formulário deve conter campos para descrição do problema e seleção do local. |
| **RI02** - O sistema deve exibir mensagens claras de erro em caso de campos inválidos ou não preenchidos. |
| **RI03** - Após o envio da solicitação, o sistema deve exibir uma confirmação visual com o número de protocolo e opção para visualizar o status da solicitação. |

## Dicionário de Dados

| Nome do Campo      | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                                                | Obrigatório | Único | Default                   |
|--------------------|--------------|----------------------------------|-----------------|-------------------------------------------------------------------------|-------------|-------|----------------------------|
| descricao    | Texto        |  ^[A-Za-z0-9\s]{1,50}$                   | -               | Descrição detalhada do problema encontrado na vaga.                    | Sim         | Não   | -                          |
| local_vaga         | Texto        | ^[A-Za-z0-9\s]{1,50}$            | -               | Identificação da vaga no estacionamento.                | Sim         | Não   | -                          |
| status_solicitacao | Texto        | ^(pendente\|em_andamento\|finalizada)$ | -           | Status atual da solicitação de manutenção.                             | Sim         | Não   | pendente                   |
| protocolo          | Texto        | ^[A-Z0-9]{8,12}$                | -               | Número único de protocolo gerado para acompanhar a solicitação.        | Sim         | Sim   | Gerado automaticamente     |
| data_solicitacao   | Data          | ^\d{2}-\d{2}-\d{4}$             | dd/mm/yyyy      | Data em que a solicitação foi registrada.                              | Sim         | Não   | Gerado automaticamente     |
| hora_solicitacao   | Hora          | ^\d{2}:\d{2}$                   | HH:mm           | Hora da solicitação.                                                   | Sim         | Não   | Gerado automaticamente     |
| criado_por         | Texto        | ^[A-Za-z0-9_]{3,30}$             | -               | Usuário logado que realizou a solicitação.                             | Sim         | Não   | Sessão atual               |
| data_criacao       | DataHora      | ^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$ | dd/mm/yyyy HH:mm| Data e hora em que o registro foi salvo no sistema.                    | Sim         | Não   | Gerado automaticamente     |
