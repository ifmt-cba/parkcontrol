| Nome do Caso de Uso       | Editar Relatórios |
|---------------------------|--------------------------------------------------|
| *Descrição*               | Permite que o contador edite dados de um relatório financeiro, inclusive os que já estão finalizados. |
| *Ator Envolvido*          | Contador |

| *Interação entre Ator e Sistema*       |                                                  |
|----------------------------------------|--------------------------------------------------|
| *Ator*                                 | *Sistema*                                        |
| Contador acessa a área de relatórios.  | Sistema exibe a opção "Editar Relatórios". |
| Contador seleciona a ferramenta de "Editar Relatórios". | Sistema exibe os relatórios disponíveis para edição, ordenados por data de criação. *(RI01)* |
| Contador seleciona um relatório da lista. | Sistema exibe os detalhes do relatório. *(RI02)* |
| Contador clica na opção "Editar relatório". | Sistema exibe o formulário com os campos editáveis: data inicial, data final e valores inseridos. *(RI03, RN01)* |
| Contador altera os dados necessários. | Sistema atualiza a pré-visualização com os novos dados. *(RI04)* |
| Contador salva as alterações. | Sistema reprocessa os dados com base nas novas informações, atualiza o relatório e mantém status como “Finalizado”. *(RN02)* |
| Contador pode baixar o novo PDF atualizado. | Sistema gera novo arquivo PDF e substitui a versão anterior. *(AL01, RI05)* |

| *Exceções* |
|------------|
| EX01 - Período inválido (data final anterior à data inicial). O sistema exibe mensagem de erro e impede a atualização. |

| *Alternativas* |
|----------------|
| AL01 - Contador pode exportar o novo relatório em PDF imediatamente após a edição. |
| AL02 - Contador pode cancelar a edição e manter a versão anterior do relatório. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com perfil de contador podem editar relatórios financeiros. |
| RN02 - A edição de relatórios finalizados é permitida. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A lista de relatórios deve permitir filtro por status (rascunho, finalizado). |
| RI02 - A visualização do relatório deve conter botão "Editar" para o contador. |
| RI03 - O formulário de edição deve conter campos: data inicial, data final, status, valores inseridos. |
| RI04 - A pré-visualização deve ser atualizada automaticamente após qualquer alteração. |
| RI05 - Após a edição, o sistema deve disponibilizar novo PDF para download. |

|**Dicionário de Dados** 

| Nome do Campo    | Tipo de Dado | Expressão Regular               | Máscara           | Descrição                                         | Obrigatório | Único | Default               |
|------------------|--------------|---------------------------------|-------------------|---------------------------------------------------|-------------|-------|-----------------------|
| editado_em       | DataHora     | ^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}$ | dd/mm/aaaa HH:MM:SS | Data/hora da última edição.                       | Sim         | Não   | Gerado automaticamente |
| data_inicio      | Data         | ^\d{2}-\d{2}-\d{4}$             | dd/mm/aaaa        | Data inicial do período de análise.               | Sim         | Não   | -                     |
| data_fim         | Data         | ^\d{2}-\d{2}-\d{4}$             | dd/mm/aaaa        | Data final do período de análise.                 | Sim         | Não   | -                     
| `status`             | Texto (Enum)     | ^(Finalizado|Rascunho)$              | -                     | Status do relatório. Pode ser "Finalizado" ou "Rascunho".| Sim              | Não       | "Finalizado"              |
| `total_emitido`      | Decimal          | ^\d+(\.\d{1,2})?$                    | #,##0.00              | Valor total das mensalidades emitidas no relatório.     | Sim              | Não       | 0,00                       |
| `criado_por`         | Texto            | ^[a-zA-Z0-9_.-]+$                    | -                     | Nome do usuário (contador) responsável pela criação do relatório. | Sim        | Não       | -                         |
| `arquivo_pdf`        | Texto (URL/Caminho) | ^[a-zA-Z0-9_.-/]+\.pdf$              | -                     | Caminho do arquivo PDF gerado do relatório.             | Não              | Sim       | -                         |
