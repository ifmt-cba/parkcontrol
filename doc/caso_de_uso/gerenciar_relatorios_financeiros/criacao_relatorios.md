| Nome do Caso de Uso       | Criação de Relatórios |
|---------------------------|--------------------------------------------------|
| *Descrição*               | Permite que o contador crie um relatório financeiro mensal, com dados de pagamentos e inadimplência dos clientes mensalistas do estacionamento. |
| *Ator Envolvido*          | Contador |

| *Interação entre Ator e Sistema*       |                                                  |
|----------------------------------------|--------------------------------------------------|
| *Ator*                                 | *Sistema*                                        |
| Contador acessa a área de relatórios.  | Sistema exibe a opção "Criar relatório". |
| Contador seleciona "Criar relatório". | Exibe formulário com campos obrigatórios: data inicial, data final, criado por. *(RI01, RN01)* |
| Contador preenche o período do mês de referência e confirma. | Sistema gera uma pré-visualização com os totais: mensalidades emitidas, pagas e inadimplência. *(RI02)* |
| Contador revisa os dados. | Sistema permite voltar e ajustar o período ou confirmar a criação. *(AL02)* |
| Contador confirma a criação do relatório. | Sistema salva o relatório como “Finalizado”, gera um PDF e o disponibiliza para consulta. *(RN02, RI03, AL01)* |

| *Exceções* |
|------------|
| EX01 - Nenhum dado de clientes mensalistas encontrado para o período informado. O sistema exibe mensagem informando que não há movimentações registradas no período informado. |

| *Alternativas* |
|----------------|
| AL01 - Contador pode exportar a prévia do relatório em PDF antes da finalização. |
| AL02 - Contador pode salvar o relatório como rascunho para finalização posterior. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com o perfil de contador podem criar relatórios financeiros de mensalistas. |
| RN02 - O relatório deve conter data e hora de geração e o usuário responsável. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A interface deve permitir seleção do período de análise (mês/ano) e requer o campo "criado_por". |
| RI02 - Deve haver pré-visualização com dados resumidos: valores totais, número de clientes, inadimplência. |
| RI03 - Após gerar o relatório, deve ser exibida uma mensagem de confirmação e opção de download em PDF |

**Dicionário de Dados**

| Nome do Campo          | Tipo de Dado  | Expressão Regular               | Máscara           | Descrição                                                      | Obrigatório | Único | Default                       |
|------------------------|---------------|---------------------------------|-------------------|----------------------------------------------------------------|-------------|-------|-------------------------------|
| data_inicio            | Data          | ^\d{2}-\d{2}-\d{4}$             | dd/mm/aaaa        | Data inicial do período de análise.                           | Sim         | Não   | -                             |
| data_fim               | Data          | ^\d{2}-\d{2}-\d{4}$             | dd/mm/aaaa        | Data final do período de análise.                             | Sim         | Não   | -                             |
| criado_por             | Texto         | ^[a-zA-Z0-9_.-]+$               | -                 | Usuário responsável pela geração do relatório.                | Sim         | Não   | -                             |
| data_criacao           | DataHora      | ^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}$ | dd/mm/aaaa HH:MM:SS | Data e hora em que o relatório foi criado.                   | Sim         | Não   | Gerado automaticamente        |
