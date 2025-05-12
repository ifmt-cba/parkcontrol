| Nome do Caso de Uso       | Registrar Entrada de Veículo |
|---------------------------|--------------------------------|
| *Descrição*               | Permite ao frentista registrar a entrada de veículos diaristas manualmente, que inclui as informações do cliente (CPF, nome), do veículo (placa, tipo de veículo) e da vaga (data e horário de entrada). Para clientes mensalistas, a entrada é identificada automaticamente pelo sistema com base na placa do veículo, sem a necessidade de intervenção do frentista, nem a emissão de ticket. |
| *Ator Envolvido*        | Frentista                      |

| *Ator*                                 | *Sistema*                                                     |
|----------------------------------------|--------------------------------------------------------------|
| Seleciona "Registrar entrada" no menu principal | Exibe formulário com os campos obrigatórios: placa do veículo e tipo de veículo.  (EX01, RN01, RI01) |
| Informa a placa do veículo            | Verifica se o veículo já está registrado como presente no estacionamento. (EX02, RN02) |
| Seleciona o tipo de cliente mensalista | Se "mensalista", sistema busca os dados do cliente automaticamente com base na placa. (AL01, RI02) |
| Seleciona o tipo de cliente diarista  | Valida o preenchimento obrigatório dos campos: nome e CPF. (RN01, RI03) |
| Confirma o registro da entrada        | Registra data e hora da entrada, vincula uma vaga livre ao veículo e atualiza o status da vaga para “ocupada”. (RN03, RI04) |

| *Exceções* |
|------------|
| EX01 - Campos obrigatórios não preenchidos: sistema exibe mensagens de erro e impede o envio do formulário. |
| EX02 - Veículo já registrado como presente: sistema bloqueia o registro e exibe notificação informando que a entrada já foi registrada. |

| *Alternativas* |
|----------------|
| AL01 - Caso a placa seja de um cliente mensalista já cadastrado, o sistema preenche automaticamente os dados do cliente. |
| AL02 - Se não houver vagas disponíveis, o sistema exibe uma mensagem informando a indisponibilidade e impede o registro. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Todos os campos obrigatórios devem ser preenchidos para habilitar o botão de confirmação. |
| RN02 - Não é permitido registrar entrada para veículos que já constam como presentes no estacionamento. |
| RN03 - A data e hora da entrada são geradas automaticamente no momento da confirmação e não podem ser editadas pelo ator. |
| RN04 - O sistema deve garantir que apenas vagas livres sejam atribuídas no momento da entrada. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - O formulário de entrada deve destacar os campos obrigatórios com asterisco vermelho e mensagens de validação em tempo real. |
| RI02 - Caso a placa seja de um cliente mensalista, os campos de cliente devem ser preenchidos automaticamente e bloqueados para edição. |
| RI03 - O formulário deve adaptar os campos exibidos com base na escolha do tipo de cliente (mensalista ou diarista). |
| RI04 - O sistema deve atualizar visualmente o mapa de vagas e destacar a vaga recém-ocupada com um indicativo de “ocupada”. |

### Dicionário de Dados

| Nome do Campo     | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                                                 | Obrigatório | Único | Default                   |
|-------------------|--------------|----------------------------------|-----------------|---------------------------------------------------------------------------|-------------|-------|----------------------------|
| placa_veiculo     | Texto        | ^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$ | AAA-0A00        | Placa do veículo. Padrão brasileiro.                                      | Sim         | Sim   | -                          |
| tipo_veiculo      | Texto        | ^(carro\|moto)$                 | -               | Tipo de veículo que está entrando (carro ou moto).                        | Sim         | Não   | -                          |
| tipo_cliente      | Texto        | ^(mensalista\|diarista)$        | -               | Define se o cliente possui plano mensalista ou é diarista.                | Sim         | Não   | -                          |
| nome_cliente      | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$           | -               | Nome do cliente (apenas para diaristas).                                  | Sim (se diarista) | Não | -                          |
| cpf_cliente       | Texto        | ^\d{3}\.\d{3}\.\d{3}-\d{2}$     | XXX.XXX.XXX-XX  | CPF do cliente (apenas para diaristas).                                   | Sim (se diarista) | Não | -                          |
| data_entrada| Data | `^\d{2}-\d{2}-\d{4}$` | dd/mm/yyyy | Data de entrada do veículo. | Sim | Não | Gerado automaticamente |
| hora_entrada | Hora | `^\d{2}:\d{2}$` | HH:mm | Hora de entrada do veículo. | Sim | Não | Gerado automaticamente |
| vaga_id           | Inteiro      | ^\d+$                           | -               | ID da vaga associada ao veículo.                                          | Sim         | Não   | Selecionado automaticamente|
| status_vaga       | Texto        | ^(livre\|ocupada\|manutencao)$  | -               | Status atual da vaga.                                                     | Sim         | Não   | ocupada                    |
| criado_por        | Texto        | ^[A-Za-z0-9_]{3,30}$            | -               | Usuário logado que realizou o registro.                                   | Sim         | Não   | Sessão atual               |
| data_criacao      | DataHora     | ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$ | dd/mm/yyyy HH:mm| Data e hora em que o registro foi salvo no sistema.                       | Sim         | Não   | Gerado automaticamente     |
