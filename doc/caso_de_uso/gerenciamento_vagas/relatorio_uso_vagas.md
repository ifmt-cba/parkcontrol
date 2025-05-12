| Nome do Caso de Uso | Relatório de Uso de Vagas |
|---------------------|---------------------------------|
| **Descrição** | Permite que o frentista gere relatórios sobre a utilização das vagas do estacionamento em determinado período, exibindo dados como vagas ocupadas, horários de pico e períodos de baixa ocupação, para fins de acompanhamento operacional. |
| **Ator Envolvido** | Frentista |

| **Ator** | **Sistema** |
|----------|-------------|
| Acessa o menu de "Relatórios" | Exibe a tela de geração de relatórios de uso de vagas. (RI01) |
| Informa o período desejado (data inicial e final) | Valida as datas informadas. (EX01, RI02, AL01) |
| Solicita a geração do relatório | Processa os dados e gera o relatório das vagas. (RN01, RI03) |

| **Exceções** |
|--------------|
| **EX01** - Datas inválidas (data inicial maior que data final): sistema exibe mensagem de erro impedindo a geração do relatório. |

| **Alternativas** |
|------------------|
| **AL01** - Se o frentista não informar filtros de período, o sistema gera o relatório considerando o dia atual como padrão. |

| **Regras de Negócio** |
|------------------------|
| **RN01** - O relatório deve apresentar informações de ocupação de vagas, horário de maior movimentação e status atual das vagas. |

| **Requisitos de Interface com o Usuário** |
|--------------------------------------------|
| **RI01** - A tela deve permitir a seleção do período para geração do relatório. |
| **RI02** - Campos de data devem ser obrigatórios e validados antes da geração do relatório. |
| **RI03** - O relatório deve ser exibido em formato de lista ou tabela, de forma clara e objetiva. |

## Dicionário de Dados

| Nome do Campo       | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                                                 | Obrigatório | Único | Default                   |
|---------------------|--------------|----------------------------------|-----------------|---------------------------------------------------------------------------|-------------|-------|----------------------------|
| data_inicial        | Data         | ^\d{2}-\d{2}-\d{4}$              | dd/mm/yyyy       | Data inicial para o relatório.                                           | Sim         | Não   | Dia atual                   |
| data_final          | Data         | ^\d{2}-\d{2}-\d{4}$              | dd/mm/yyyy       | Data final para o relatório.                                             | Sim         | Não   | Dia atual                   |
| criado_por          | Texto        | ^[A-Za-z0-9_]{3,30}$             | -                | Frentista logado que solicitou o relatório.                              | Sim         | Não   | Sessão atual                |
| data_geracao        | DataHora     | ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$  | dd/mm/yyyy HH:mm | Data e hora da geração do relatório.                                     | Sim         | Não   | Gerado automaticamente     |
