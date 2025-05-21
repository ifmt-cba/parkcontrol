| Nome do Caso de Uso       | Editar Cobrança Diarista |
|---------------------------|---------------------------|
| *Descrição*               | Permite ao frentista alterar informações de cobranças de clientes diaristas que ainda não foram quitadas. |
| *Ator Envolvido*          | Frentista |

---

| *Interação entre Ator e Sistema* |                                                  |
|----------------------------------|--------------------------------------------------|
| *Ator*                           | *Sistema*                                        |
| O frentista acessa a funcionalidade "Visualizar Cobrança Diarista". | Sistema exibe lista de cobranças com filtros aplicáveis. (RI01) |
| O frentista seleciona uma cobrança na lista para edição. | Sistema abre a tela de edição da cobrança selecionada, exibindo campos editáveis: horário de entrada, horário de saída. (RI02) |
| O frentista altera os campos desejados. | Sistema valida os novos valores inseridos. (RN01, EX01) |
| O frentista confirma a atualização dos dados. | Sistema salva as alterações e recalcula o valor da cobrança, se necessário. (RN02, RI03) |
| Em caso de sucesso, o sistema exibe mensagem de confirmação. | (RI04) |
| Em caso de erro de validação, o sistema informa o erro e impede a atualização até correção. | (EX02) |
| O frentista pode optar por cancelar a edição antes de confirmar. | Sistema descarta as alterações e retorna para a tela anterior. (AL01) |

---

| *Exceções* |
|------------|
| EX01 - Dados obrigatórios não preenchidos ou inválidos durante edição: o sistema exibe mensagem de erro e impede o envio até correção. |
| EX02 - Tentativa de editar cobrança já quitada: o sistema bloqueia a edição e exibe mensagem de erro. |

---

| *Alternativas* |
|----------------|
| AL01 - O frentista pode cancelar a edição antes da confirmação, descartando todas as alterações feitas. |

---

| *Regras de Negócio* |
|---------------------|
| RN01 - Não é permitido deixar campos obrigatórios (horário de entrada/saída) vazios após edição. |
| RN02 - Caso o horário de entrada ou saída seja alterado, o valor da cobrança deve ser recalculado automaticamente com base nas regras vigentes. |

---

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Lista de cobranças deve ter opção de seleção para edição. |
| RI02 - Tela de edição deve permitir alteração apenas de horário de entrada, horário de saída (placa e status são bloqueados). |
| RI03 - O campo \"Valor da Cobrança\" deve ser recalculado automaticamente e atualizado em tela. |
| RI04 - Mensagem de sucesso deve ser exibida após a confirmação da edição. |

---

### Dicionário de Dados

| Nome do Campo        | Tipo de Dado | Expressão Regular               | Máscara        | Descrição                                          | Obrigatório | Único | Default |
|----------------------|--------------|----------------------------------|----------------|----------------------------------------------------|-------------|-------|---------|
| id_cobranca          | Inteiro       | `^\d+$`                           | -              | Identificador único da cobrança.                   | Sim         | Sim   | -       |
| placa_veiculo        | Texto         | `^[A-Z]{3}-[0-9][A-Z0-9][0-9]{2}$` | AAA-0A00       | Placa do veículo.                                 | Sim         | Não   | Não editável |
| horario_entrada      | DataHora      | `^\d{2}:\d{2}$`                   | HH:MM          | Horário de entrada registrado.                     | Sim         | Não   | Editável |
| horario_saida        | DataHora      | `^\d{2}:\d{2}$`                   | HH:MM          | Horário de saída registrado.                       | Sim         | Não   | Editável |
| valor_cobranca       | Decimal(10,2) | `^\d+(\.\d{2})?$`                 | -              | Valor recalculado com base no novo tempo de permanência. | Sim         | Não   | Calculado |
| status_cobranca      | Texto         | `^(pendente\|pago)$`               | -              | Estado atual da cobrança.                         | Sim         | Não   | Não editável |

---
