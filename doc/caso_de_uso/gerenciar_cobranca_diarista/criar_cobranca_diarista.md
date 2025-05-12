| Nome do Caso de Uso       | Criar Cobrança Diarista |
|---------------------------|--------------------------|
| *Descrição*               | Permite ao frentista registrar uma nova cobrança para clientes diaristas com base no período de permanência no estacionamento. |
| *Ator Envolvido*          | Frentista |

---

| *Interação entre Ator e Sistema* |                                                  |
|----------------------------------|--------------------------------------------------|
| *Ator*                           | *Sistema*                                        |
| O frentista acessa a funcionalidade "Criar Cobrança Diarista". | Sistema exibe formulário para preenchimento dos dados obrigatórios: placa do veículo, horário de entrada, horário de saída, valor calculado. (RI01) |
| O frentista preenche os campos obrigatórios. | Sistema valida se todos os campos foram preenchidos corretamente. (RN01, EX01) |
| O frentista pode optar por corrigir os dados preenchidos antes de confirmar. | Sistema permite edição dos campos preenchidos. (AL02) |
| O frentista pode cancelar o cadastro da cobrança antes da confirmação. | Sistema descarta os dados preenchidos e retorna para tela principal. (AL01) |
| O frentista confirma a criação da cobrança. | Sistema valida se o veículo está registrado no sistema. Se não encontrado, exibe erro e impede continuação. (EX02, RN01) |
| Após validações, sistema calcula automaticamente o valor da cobrança com base no tempo de permanência e tabela de preços. | Sistema preenche o campo "Valor da Cobrança". (RN02) |
| Sistema cria o registro da cobrança no banco de dados. | Sistema exibe mensagem de sucesso confirmando a criação. (RI03) |

---

| *Exceções* |
|------------|
| EX01 - Dados obrigatórios não preenchidos ou inválidos: o sistema exibe mensagem de erro específica e impede o envio até correção. |
| EX02 - Tentativa de cobrança para veículo não registrado: o sistema exibe alerta de erro e bloqueia a criação da cobrança. |

---

| *Alternativas* |
|----------------|
| AL01 - O frentista pode cancelar o preenchimento da cobrança antes de confirmar. |
| AL02 - O frentista pode alterar o horário de entrada/saída ou a placa antes de confirmar o envio. |

---

| *Regras de Negócio* |
|---------------------|
| RN01 - Só é permitido criar cobrança para veículos previamente registrados no sistema. |
| RN02 - O valor da cobrança deve ser calculado automaticamente com base no tempo de permanência e na tabela vigente de preços. |

---

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Formulário deve conter campos para placa, horário de entrada, horário de saída e valor da cobrança (editável antes da confirmação). |
| RI02 - Deve haver botões \"Confirmar Cobrança\" e \"Cancelar Operação\" claramente visíveis. |
| RI03 - O sistema deve exibir mensagem de sucesso após a criação da cobrança. |

---

### Dicionário de Dados

| Nome do Campo        | Tipo de Dado | Expressão Regular               | Máscara        | Descrição                                          | Obrigatório | Único | Default |
|----------------------|--------------|----------------------------------|----------------|----------------------------------------------------|-------------|-------|---------|
| placa_veiculo        | Texto         | `^[A-Z]{3}-[0-9][A-Z0-9][0-9]{2}$` | AAA-0A00       | Placa do veículo (formato Mercosul antigo ou novo) | Sim         | Não   | -       |
| horario_entrada      | DataHora      | `^\d{2}:\d{2}$`                   | HH:MM          | Horário de entrada registrado.                     | Sim         | Não   | -       |
| horario_saida        | DataHora      | `^\d{2}:\d{2}$`                   | HH:MM          | Horário de saída registrado.                       | Sim         | Não   | -       |
| valor_cobranca       | Decimal(10,2) | `^\d+(\.\d{2})?$`                 | -              | Valor calculado com base no tempo de permanência.   | Sim         | Não   | -       |
| status_cobranca      | Texto         | `^(pendente\|pago)$`               | -              | Estado da cobrança.                               | Sim         | Não   | pendente |
| data_criacao         | Data          | `^\d{4}-\d{2}-\d{2}$`             | dd/mm/aaaa     | Data em que a cobrança foi criada.                 | Sim         | Não   | Gerado automaticamente |
| criado_por           | Texto         | `^[A-Za-zÀ-ÿ\s]{3,50}$`            | -              | Nome do usuário (frentista) que criou a cobrança.  | Sim         | Não   | Usuário logado |
