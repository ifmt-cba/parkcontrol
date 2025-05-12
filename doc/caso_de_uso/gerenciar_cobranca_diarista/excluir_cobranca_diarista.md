| Nome do Caso de Uso       | Excluir Cobrança Diarista |
|---------------------------|----------------------------|
| *Descrição*               | Permite ao frentista remover do sistema cobranças de clientes diaristas que ainda não foram pagas. |
| *Ator Envolvido*          | Frentista |

---

| *Interação entre Ator e Sistema* |                                                  |
|----------------------------------|--------------------------------------------------|
| *Ator*                           | *Sistema*                                        |
| O frentista acessa a funcionalidade "Visualizar Cobrança Diarista". | Sistema exibe lista de cobranças cadastradas com filtros aplicáveis. (RI01) |
| O frentista seleciona a cobrança que deseja excluir. | Sistema solicita confirmação para exclusão da cobrança. (RI02) |
| O frentista confirma a exclusão da cobrança. | Sistema verifica se a cobrança está no status "pendente". Se sim, procede com a exclusão. (RN01, EX01) |
| Sistema remove a cobrança do banco de dados e exibe mensagem de sucesso. | (RI03) |
| Caso a cobrança já esteja no status "pago", o sistema bloqueia a exclusão e informa o usuário. | (EX02) |
| O frentista pode optar por cancelar o processo de exclusão antes da confirmação. | Sistema cancela a operação e retorna à tela anterior. (AL01) |

---

| *Exceções* |
|------------|
| EX01 - Erro ao tentar excluir uma cobrança pendente devido a problema de comunicação com o banco de dados: o sistema exibe mensagem de erro e orienta a tentar novamente. |
| EX02 - Tentativa de excluir cobrança já paga: o sistema bloqueia a exclusão e exibe mensagem de erro. |

---

| *Alternativas* |
|----------------|
| AL01 - O frentista pode cancelar o processo de exclusão antes de confirmar, sem alterações no sistema. |

---

| *Regras de Negócio* |
|---------------------|
| RN01 - Só é permitido excluir cobranças que estejam no status "pendente". |

---

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Tela de listagem de cobranças deve permitir selecionar cobranças para ação de exclusão. |
| RI02 - Sistema deve exibir mensagem de confirmação antes de efetuar a exclusão. |
| RI03 - Mensagem de sucesso deve ser exibida após exclusão realizada com êxito. |

---

### Dicionário de Dados

| Nome do Campo        | Tipo de Dado | Expressão Regular               | Máscara        | Descrição                                          | Obrigatório | Único | Default |
|----------------------|--------------|----------------------------------|----------------|----------------------------------------------------|-------------|-------|---------|
| id_cobranca          | Inteiro       | `^\d+$`                           | -              | Identificador único da cobrança.                   | Sim         | Sim   | -       |
| placa_veiculo        | Texto         | `^[A-Z]{3}-[0-9][A-Z0-9][0-9]{2}$` | AAA-0A00       | Placa associada à cobrança.                        | Sim         | Não   | -       |
| status_cobranca      | Texto         | `^(pendente\|pago)$`               | -              | Estado da cobrança.                               | Sim         | Não   | -       |
| data_criacao         | Data          | `^\d{4}-\d{2}-\d{2}$`             | dd/mm/aaaa     | Data de criação da cobrança.                      | Sim         | Não   | -       |

---
