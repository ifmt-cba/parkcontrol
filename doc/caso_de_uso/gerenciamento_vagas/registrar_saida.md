| Nome do Caso de Uso       | Registrar Saída de Veículo |
|---------------------------|----------------------------|
| *Descrição*               | Permite ao frentista registrar a saída de veículos do estacionamento, atualizando o status da vaga para "livre" e gerando o valor a ser pago no caso de clientes diaristas. Para mensalistas, a saída é registrada sem cobrança. A data e hora de saída são geradas automaticamente pelo sistema. |
| *Ator Envolvido*           | Frentista                  |

| *Ator*                                 | *Sistema*                                                     |
|----------------------------------------|--------------------------------------------------------------|
| Seleciona "Registrar saída" no menu principal | Exibe campo para digitar a placa do veículo. (EX01, RN01, RI01) |
| Informa a placa do veículo             | Valida se o veículo está registrado como presente. (EX02, RN02) |
| Exibe resumo da saída                    | Valor cobrado, tempo de permanência, e confirmação de saída da vaga. (AL01, AL02, RN04) |
| Confirma o registro da saída           | Registra data e hora da saída, libera a vaga associada e calcula o valor devido para clientes diaristas. (RN03, RI02, RI03) |

| *Exceções* |
|------------|
| EX01 - Placa não informada: sistema exibe mensagem de erro e impede a confirmação da saída. |
| EX02 - Placa não encontrada como presente: sistema informa que o veículo não está registrado como presente e impede a operação. |

| *Alternativas* |
|----------------|
| AL01 - Se o veículo for de cliente mensalista, o sistema registra a saída sem cobrança e apenas libera a vaga. |
| AL02 - Se o veículo for de cliente diarista, o sistema calcula automaticamente o valor conforme o tempo de permanência e tipo de veículo. |

| *Regras de Negócio* |
|---------------------|
| RN01 - A placa é obrigatória para localizar o veículo. |
| RN02 - Somente veículos presentes podem ter a saída registrada. |
| RN03 - A data e hora de saída são geradas automaticamente e não podem ser editadas pelo ator. |
| RN04 - O valor cobrado para clientes diaristas deve ser calculado com base no tempo de permanência e tarifa do tipo de veículo. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - O formulário de saída deve validar imediatamente se a placa informada corresponde a um veículo presente. |
| RI02 - Se cliente diarista, exibir o valor a pagar antes de confirmar a saída. |
| RI03 - O sistema deve atualizar o mapa de vagas e marcar a vaga associada como "livre" após a saída. |

### Dicionário de Dados

| Nome do Campo     | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                                                 | Obrigatório | Único | Default                   |
|-------------------|--------------|----------------------------------|-----------------|---------------------------------------------------------------------------|-------------|-------|----------------------------|
| placa_veiculo     | Texto        | ^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$ | AAA-0A00        | Placa do veículo.                                       | Sim         | Sim   | -                          |
| tipo_cliente      | Texto        | ^(mensalista\|diarista)$        | -               | Define se o cliente é mensalista ou diarista.                             | Sim         | Não   | -                          |
| tipo_veiculo      | Texto        | ^(carro\|moto)$                 | -               | Tipo de veículo (carro ou moto).                                           | Sim         | Não   | -                          |
| data_saida        | Data         | ^\d{2}-\d{2}-\d{4}$             | dd/mm/yyyy      | Data de saída do veículo.                                                 | Sim         | Não   | Gerado automaticamente     |
| hora_saida        | Hora         | ^\d{2}:\d{2}$                   | HH:mm           | Hora de saída do veículo.                                                 | Sim         | Não   | Gerado automaticamente     |
| tempo_permanencia | Inteiro      | ^\d+$                           | -               | Tempo total de permanência em minutos.                                    | Sim         | Não   | Calculado automaticamente  |
| valor_cobrado     | Decimal      | ^\d+(\.\d{2})?$                 | 0.00            | Valor total a ser pago.                       
| Sim      | Não | Calculado automaticamente  |
| vaga_id           | Inteiro      | ^\d+$                           | -               | ID da vaga que foi liberada.                                               | Sim         | Não   | Relacionado automaticamente|
| status_vaga       | Texto        | ^(livre\|ocupada\|manutencao)$  | -               | Status atual da vaga (após a saída: "livre").                              | Sim         | Não   | livre                      |
| atualizado_por    | Texto        | ^[A-Za-z0-9_]{3,30}$            | -               | Usuário logado que realizou a saída.                                       | Sim         | Não   | Sessão atual               |
| data_atualizacao  | DataHora     | ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$ | dd/mm/yyyy HH:mm| Data e hora em que o registro da saída foi salvo no sistema.              | Sim         | Não   | Gerado automaticamente     |
