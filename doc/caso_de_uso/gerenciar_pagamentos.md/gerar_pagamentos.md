| **Nome do Caso de Uso**       | Gerar Pagamentos Mensalistas |
|------------------------------|----------------------------------------|
| **Descrição**                | Permite que o contador gere cobranças mensais para clientes mensalistas com contrato ativo, inclusive aqueles com inadimplência. O preenchimento dos campos mês de referência, vencimento e valor é obrigatório. |
| **Ator Envolvido**           | Contador |

| **Interação entre Ator e Sistema**       |                                                    |
|------------------------------------------|----------------------------------------------------|
| **Ator**                                 | **Sistema**                                        |
| Contador acessa a a área de "Gerência de Pagamentos". | Sistema exibe a opção "Gerar Pagamentos Mensalistas". |
| Contador acessa a opção "Gerar Pagamentos Mensalista" no menu. | Sistema exibe lista de mensalistas ativos e opção "Gerar cobrança". |
| Contador seleciona um usuário mensalista e clica em "Gerar cobrança". | Sistema exibe formulário com campos: mês de referência, vencimento, valor. *(RI01, RN01)* |
| Contador tenta confirmar sem preencher todos os campos obrigatórios. | Sistema bloqueia a ação, destaca os campos obrigatórios e exibe mensagem de erro. *(EX02, RN03, RI03)* |
| Contador preenche os dados obrigatórios e confirma. | Sistema cria uma nova cobrança com status “Aguardando pagamento”. *(RI02, RN02)* |
| Contador revisa lista de cobranças geradas. | Sistema permite exportar a lista ou visualizar detalhes individuais. *(AL01)* |

| **Exceções** |
|-------------|
| EX01 - Mensalista com contrato inativo: sistema não permite geração da cobrança e exibe mensagem de erro. |
| EX02 - O contador tenta confirmar sem preencher todos os campos obrigatórios: sistema bloqueia a ação, destaca os campos não preenchidos e exibe a mensagem "Preencha todos os campos obrigatórios antes de confirmar". |

| **Alternativas** |
|------------------|
| AL01 - Contador pode exportar todas as cobranças geradas em PDF. |

| **Regras de Negócio** |
|-----------------------|
| RN01 - Podem ser geradas cobranças para mensalistas com contrato ativo, independentemente da situação de inadimplência. |
| RN02 - O valor da cobrança deve ser baseado no plano atual do cliente no momento da geração. |
| RN03 - Os campos mês de referência, vencimento e valor são obrigatórios para criação da cobrança. |

| **Requisitos de Interface com o Usuário** |
|-------------------------------------------|
| RI01 - A interface deve permitir seleção de mês/ano e data de vencimento, além do valor da cobrança. |
| RI02 - Deve exibir confirmação da cobrança e status inicial "Aguardando pagamento". |
| RI03 - Caso o usuário tente confirmar sem preencher os campos obrigatórios, deve ser exibida uma mensagem de erro destacando os campos ausentes. |

**Dicionário de Dados – Campos de Entrada**

| Nome do Campo          | Tipo de Dado     | Expressão Regular               | Máscara           | Descrição                                                      | Obrigatório | Único | Default                       |
|------------------------|------------------|---------------------------------|-------------------|----------------------------------------------------------------|-------------|-------|-------------------------------|
| mes_referencia         | Texto (Mês/Ano)  | ^(0[1-9]\|1[0-2])\/\d{4}$       | mm/aaaa           | Mês e ano ao qual a cobrança se refere.                        | Sim         | Não   | -                             |
| vencimento             | Data             | ^\d{2}-\d{2}-\d{4}$             | dd/mm/aaaa        | Data de vencimento da cobrança.                                | Sim         | Não   | -                             |
| valor                  | Decimal          | ^\d+(\.\d{2})?$                 | 9999,99           | Valor da cobrança conforme o plano contratado.                 | Sim         | Não   | Definido pelo plano           |
