## Nome do Caso de Uso  
**Gerenciamento de Planos Diaristas**

## Descrição  
Permite ao administrador realizar o gerenciamento completo dos planos de diária do sistema, incluindo **criação**, **edição**, **visualização** e **exclusão** de planos, garantindo controle sobre os dados e status de cada plano.

## Ator Envolvido  
**Administrador**

---

## Interação entre Ator e Sistema

| **Ator** | **Sistema** |
|----------|-------------|
| Administrador acessa o módulo "Gerenciar Planos". | Exibe a interface principal com listagem de planos e opções: **"Criar"**, **"Editar"**, **"Visualizar"** e **"Excluir"**. (RI01, RN01) |
| Seleciona a opção **"Criar Novo Plano"**. | Exibe formulário de cadastro com campos obrigatórios. (RI02) |
| Preenche os dados e clica em **"Salvar"**. | Valida os campos e cria o novo plano no sistema. (RN02, RN03, EX01, EX02, RI03) |
| Seleciona um plano e clica em **"Editar"**. | Exibe formulário com os dados atuais para edição. (RI02) |
| Altera os dados e confirma. | Valida os dados e salva as alterações. (RN01, RN03, EX01, AL01, RI03) |
| Clica em **"Visualizar"** em um plano. | Exibe detalhes do plano (nome, valor, validade, status, etc.). (RI01) |
| Clica em **"Excluir"** em um plano. | Solicita confirmação e, se permitido, exclui o plano. (RN04, EX03, EX04, RI04) |

---

## Exceções

| **Código** | **Descrição** |
|-----------|----------------|
| EX01 | Campos obrigatórios não preenchidos: o sistema exibe mensagem de erro. |
| EX02 | Nome do plano já cadastrado: o sistema bloqueia o cadastro e informa a duplicidade. |
| EX03 | Plano associado a clientes ativos: exclusão não permitida. |
| EX04 | Plano inexistente ou já excluído: sistema informa erro. |

---

## Alternativas

| **Código** | **Descrição** |
|-----------|----------------|
| AL01 | O administrador pode corrigir erros e reenviar a ação. |
| AL02 | O administrador pode cancelar qualquer ação, retornando à tela de listagem de planos. |
| AL03 | Pode utilizar filtros para localizar planos específicos. |

---

## Regras de Negócio

| **Código** | **Descrição** |
|-----------|----------------|
| RN01 | Apenas administradores têm acesso ao gerenciamento de planos. |
| RN02 | Nome do plano deve ser único. |
| RN03 | Valor deve ser um número positivo com duas casas decimais. |
| RN04 | Um plano só pode ser excluído se não estiver vinculado a clientes ativos. |

---

## Requisitos de Interface com o Usuário

| **Código** | **Descrição** |
|-----------|----------------|
| RI01 | A interface deve exibir os planos em formato de tabela com ações: Visualizar, Editar e Excluir. |
| RI02 | Formulários de cadastro e edição devem conter campos claros e validados. |
| RI03 | Exibir mensagens de erro ou sucesso ao criar/editar planos. |
| RI04 | A exclusão deve ser confirmada em uma janela/modal, com mensagem clara sobre a ação. |

---

## Dicionário de Dados

| **Nome do Campo** | **Tipo de Dado** | **Expressão Regular** | **Máscara** | **Descrição** | **Obrigatório** | **Único** | **Default** |
|-------------------|------------------|------------------------|-------------|----------------|------------------|------------|------------|
| nome              | Texto            | ^[A-Za-z0-9\s]{3,50}$  | -           | Nome do plano. | Sim              | Sim        | -          |
| valor_diario      | Decimal (R$)     | ^\d{1,5}(,\d{2})?$     | 99999,99    | Valor da diária. | Sim            | Não        | -          |
| validade          | Número inteiro   | ^\d{1,3}$              | -           | Validade em dias. | Sim           | Não        | -          |
| descrição         | Texto Longo      | .*                     | -           | Descrição opcional. | Não         | Não        | -          |
| status            | Booleano         | ^(ativo\|inativo)$     | -           | Status do plano. | Não           | Não        | ativo      |
| data_criacao      | Data             | ^\d{2}-\d{2}-\d{4}$    | dd/mm/aaaa  | Data de criação. | Sim            | Não        | Gerado automaticamente |
| ultima_alteracao  | DataHora         | ^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}$ | dd/mm/aaaa hh:mm:ss | Última alteração feita. | Não | Não | Gerado automaticamente |
| criado_por        | Texto            | ^[A-Za-z0-9]{3,30}$    | -           | ID do criador do plano. | Sim     | Não        | Gerado automaticamente |
| clientes_associado | Booleano        | ^(sim\|não)$           | -           | Indica se há clientes associados. | Não | Não | não |
| data_exclusao     | Data             | ^\d{4}-\d{2}-\d{2}$    | dd/mm/aaaa  | Data da exclusão (se houver). | Não | Não | - |
| excluido_por      | Texto            | ^[A-Za-z0-9]{3,30}$    | -           | Usuário que realizou a exclusão. | Não | Não | - |
