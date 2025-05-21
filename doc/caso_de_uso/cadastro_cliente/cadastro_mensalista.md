| Nome do Caso de Uso       | Cadastrar Cliente Mensalista |
|---------------------------|-------------------------------|
| *Descrição*               | Permite ao frentista registrar no sistema os dados pessoais de clientes que contratarão um plano mensal para uso do estacionamento. |
| *Ator Envolvido*          | Frentista |

---

| *Interação entre Ator e Sistema* |                                                  |
|----------------------------------|--------------------------------------------------|
| *Ator*                           | *Sistema*                                        |
| O frentista acessa a funcionalidade "Cadastrar Cliente Mensalista". | Sistema exibe formulário de cadastro contendo campos obrigatórios: nome completo, telefone, e-mail, placa do veículo e seleção de plano mensalista. (RI01) |
| O frentista preenche todos os campos obrigatórios. | Sistema valida os dados preenchidos. (RN01, EX01) |
| O frentista pode corrigir informações antes de confirmar. | Sistema mantém os campos editáveis até a confirmação. (AL02) |
| O frentista seleciona o plano mensalista desejado para o cliente. | Sistema exibe lista de planos cadastrados para seleção. (RI02) |
| O frentista pode cancelar o cadastro antes da confirmação. | Sistema descarta os dados inseridos e retorna para a tela principal. (AL01) |
| O frentista confirma o cadastro do cliente. | Sistema armazena o cadastro no banco de dados, gera o vencimento inicial e exibe mensagem de sucesso. (RI03, RN02) |
| Caso ocorra falha de comunicação com o banco de dados, o sistema exibe mensagem de erro e orienta a tentar novamente. | (EX02) |

---

| *Exceções* |
|------------|
| EX01 - Campos obrigatórios não preenchidos ou inválidos: o sistema exibe mensagem de erro e impede a confirmação. |
| EX02 - Falha ao salvar o cliente devido a erro de banco de dados: o sistema exibe mensagem de erro e orienta o frentista a tentar novamente. |

---

| *Alternativas* |
|----------------|
| AL01 - O frentista pode cancelar o cadastro antes da confirmação, descartando todas as informações preenchidas. |
| AL02 - O frentista pode corrigir os dados preenchidos antes de confirmar o envio. |

---

| *Regras de Negócio* |
|---------------------|
| RN01 - Todos os campos obrigatórios (nome, telefone, e-mail, placa do veículo, plano) devem ser preenchidos para efetivar o cadastro. |
| RN02 - Após o cadastro, o sistema deve gerar automaticamente a primeira cobrança com data de vencimento baseada no plano escolhido. |

---

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Formulário deve conter campos para Nome Completo, Telefone, E-mail, Placa do Veículo e Seleção de Plano Mensalista. |
| RI02 - Tela deve exibir lista suspensa ou equivalente para seleção do plano disponível. |
| RI03 - Após a confirmação, o sistema deve exibir uma mensagem de sucesso clara e objetiva. |

---

### Dicionário de Dados

| Nome do Campo        | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                          | Obrigatório | Único | Default |
|----------------------|--------------|----------------------------------|-----------------|----------------------------------------------------|-------------|-------|---------|
| nome_completo        | Texto         | `^[A-Za-zÀ-ÿ\s]{3,50}$`           | -               | Nome completo do cliente.                         | Sim         | Não   | -       |
| telefone             | Texto         | `^\(?\d{2}\)?[\s-]?\d{4,5}-\d{4}$` | (00) 00000-0000 | Telefone para contato.                             | Sim         | Não   | -       |
| email                | Texto         | `^[\w\.-]+@[\w\.-]+\.\w{2,}$`      | -               | E-mail de contato do cliente.                     | Sim         | Sim   | -       |
| placa_veiculo        | Texto         | `^[A-Z]{3}-[0-9][A-Z0-9][0-9]{2}$` | AAA-0A00        | Placa do veículo associado ao cliente.             | Sim         | Não   | -       |
| plano_mensalista     | Texto         | `^[A-Za-z0-9\s]{3,50}$`           | -               | Nome do plano mensalista contratado.               | Sim         | Não   | -       |
| vencimento           | Data          | `^\d{4}-\d{2}-\d{2}$`             | dd/mm/aaaa      | Data de vencimento gerada com base na data de cadastro. | Sim         | Não   | Gerado automaticamente |
| status_cliente       | Texto         | `^(ativo\|inativo)$`               | -               | Status do cliente no sistema.                     | Sim         | Não   | ativo |
| data_cadastro        | Data          | `^\d{4}-\d{2}-\d{2}$`             | dd/mm/aaaa      | Data de criação do cadastro.                      | Sim         | Não   | Gerado automaticamente |
| criado_por           | Texto         | `^[A-Za-zÀ-ÿ\s]{3,50}$`           | -               | Nome do usuário (frentista) que realizou o cadastro. | Sim         | Não   | Usuário logado |

---
