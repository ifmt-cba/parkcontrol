| Nome do Caso de Uso       | Cadastrar Cliente Diarista |
|---------------------------|-----------------------------|
| *Descrição*               | Permite ao frentista registrar no sistema os dados básicos de clientes que utilizarão o estacionamento com pagamento por diária. |
| *Ator Envolvido*          | Frentista |

---

| *Interação entre Ator e Sistema* |                                                  |
|----------------------------------|--------------------------------------------------|
| *Ator*                           | *Sistema*                                        |
| O frentista acessa a funcionalidade "Cadastrar Cliente Diarista". | Sistema exibe formulário de cadastro contendo os campos obrigatórios: nome completo, telefone, e placa do veículo. (RI01) |
| O frentista preenche os campos obrigatórios. | Sistema valida os dados preenchidos. (RN01, EX01) |
| O frentista pode corrigir informações preenchidas antes de confirmar. | Sistema mantém os campos editáveis até a confirmação. (AL02) |
| O frentista pode cancelar o cadastro antes de confirmar. | Sistema descarta os dados inseridos e retorna à tela principal. (AL01) |
| O frentista confirma o cadastro do cliente. | Sistema armazena o cadastro no banco de dados e exibe mensagem de sucesso. (RI02) |
| Caso ocorra falha de comunicação com o banco de dados, o sistema exibe mensagem de erro e orienta a tentar novamente. | (EX02) |

---

| *Exceções* |
|------------|
| EX01 - Campos obrigatórios não preenchidos ou inválidos: o sistema exibe mensagem de erro e bloqueia a confirmação. |
| EX02 - Falha ao salvar o cliente devido a erro de banco de dados: o sistema exibe mensagem de erro e orienta o frentista a tentar novamente. |

---

| *Alternativas* |
|----------------|
| AL01 - O frentista pode cancelar o cadastro antes da confirmação, descartando todas as informações preenchidas. |
| AL02 - O frentista pode corrigir os dados digitados antes da confirmação. |

---

| *Regras de Negócio* |
|---------------------|
| RN01 - Todos os campos obrigatórios (nome, telefone, placa) devem ser preenchidos corretamente para permitir o cadastro. |

---

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Formulário deve conter campos para Nome Completo, Telefone e Placa do Veículo. |
| RI02 - Após o cadastro, o sistema deve exibir uma mensagem de confirmação clara e objetiva. |

---

### Dicionário de Dados

| Nome do Campo        | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                          | Obrigatório | Único | Default |
|----------------------|--------------|----------------------------------|-----------------|----------------------------------------------------|-------------|-------|---------|
| nome_completo        | Texto         | `^[A-Za-zÀ-ÿ\s]{3,50}$`           | -               | Nome completo do cliente. Deve conter entre 3 e 50 caracteres. | Sim         | Não   | -       |
| telefone             | Texto         | `^\(?\d{2}\)?[\s-]?\d{4,5}-\d{4}$` | (00) 00000-0000 | Telefone para contato. Deve ser válido.            | Sim         | Não   | -       |
| placa_veiculo        | Texto         | `^[A-Z]{3}-[0-9][A-Z0-9][0-9]{2}$` | AAA-0A00        | Placa do veículo associado ao cliente.             | Sim         | Não   | -       |
| data_cadastro        | Data          | `^\d{4}-\d{2}-\d{2}$`             | dd/mm/aaaa      | Data em que o cadastro foi realizado.              | Sim         | Não   | Gerado automaticamente |
| criado_por           | Texto         | `^[A-Za-zÀ-ÿ\s]{3,50}$`           | -               | Nome do usuário (frentista) que realizou o cadastro. | Sim         | Não   | Usuário logado |

---
