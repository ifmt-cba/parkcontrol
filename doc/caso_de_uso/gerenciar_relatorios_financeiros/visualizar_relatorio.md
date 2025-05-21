| Nome do Caso de Uso       | Visualizar Relatórios |
|---------------------------|-----------------------------|
| *Descrição*               | Permite que o contador visualize todos os relatórios financeiros mensais já gerados e finalizados. |
| *Ator Envolvido*          | Contador e Administrador |

| *Interação entre Ator e Sistema*       |                                                  |
|----------------------------------------|--------------------------------------------------|
| *Ator*                                 | *Sistema*                                        |
| Contador acessa a área de relatórios.  | Sistema exibe a opção "Visualizar Relatórios". |
| Contador seleciona "Visualizar Relatórios". | Sistema exibe uma lista com todos os relatórios finalizados, ordenados por data de criação. *(RI01, RN01)* |
| Contador acessa a área de visualização de relatórios | Sistema exibe mensagem de erro caso não tenha relatórios finalizados cadastrados. *(EX01)* | 
| Contador seleciona um relatório da lista. | Sistema exibe o relatório completo com os dados: total emitido, total pago e período. *(RI02)* |
| Contador clica em "Exportar PDF". | Sistema gera o arquivo PDF do relatório exibido e permite o download ou impressão. *(AL01, RI03)* |

| *Exceções* |
|------------|
| EX01 - Nenhum relatório disponível. O sistema exibe mensagem informando que não há relatórios finalizados cadastrados. |

| *Alternativas* |
|----------------|
| AL01 - Contador pode exportar o relatório visualizado como PDF. |

| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com o perfil de contador e administrador podem acessar a visualização de relatórios financeiros. |
| RN02 - Apenas relatórios com status “Finalizado” podem ser visualizados. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A interface deve exibir todos os relatórios com colunas: data de criação e status. |
| RI02 - A visualização do relatório deve exibir os dados financeiros de forma clara e organizada. |
| RI03 - Deve haver botão de exportação em PDF na visualização do relatório. |

# Dicionário de Dados – Visualizar Relatórios

| **Nome do Campo**        | **Tipo de Dado** | **Expressão Regular**                  | **Máscara**        | **Descrição**                                                                 | **Obrigatório** | **Único** | **Default**              |
|--------------------------|------------------|----------------------------------------|--------------------|-------------------------------------------------------------------------------|------------------|-----------|--------------------------|
| `data_criacao`           | Data             | ^\d{2}-\d{2}-\d{4}$                    | dd/mm/aaaa         | Data em que o relatório foi gerado.                                          | Sim              | Não       | Gerado automaticamente   |
| `periodo_inicio`         | Data             | ^\d{2}-\d{2}-\d{4}$                    | dd/mm/aaaa         | Data de início do período analisado no relatório.                            | Sim              | Não       | -                        |
| `periodo_fim`            | Data             | ^\d{2}-\d{2}-\d{4}$                    | dd/mm/aaaa         | Data de fim do período analisado no relatório.                               | Sim              | Não       | -                        |
| `status`                 | Texto (Enum)     | ^(Finalizado|Pendente)$                | -                  | Status do relatório. Apenas “Finalizado” pode ser visualizado.               | Sim              | Não       | "Pendente"               |
| `criado_por`             | Texto            | ^[a-zA-Z0-9_.-]+$                      | -                  | Nome do usuário (contador) responsável pela criação do relatório.            | Sim              | Não       | -                        |
| `arquivo_pdf`            | Texto (URL/Caminho) | ^[a-zA-Z0-9_.-/]+\.pdf$                | -                  | Caminho do arquivo PDF gerado do relatório.                                  | Não              | Sim       | -                        |

