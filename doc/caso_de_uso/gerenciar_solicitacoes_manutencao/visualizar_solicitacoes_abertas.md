| Nome do Caso de Uso | Visualizar Solicitações Abertas |
|---------------------|----------------------------------------|
| **Descrição** | Permite que o administrador visualize todas as solicitações de manutenção de vagas que foram encaminhadas para seu acompanhamento e posterior resolução. O administrador pode visualizar os detalhes, como descrição, local da vaga, data da solicitação e status atual (pendente, em andamento ou finalizada). |
| **Ator Envolvido** | Administrador |

| *Ator* | *Sistema* |
|---------------------------------------------------------------------------------------------------------------------------|
| Acessa o menu “Solicitações de Manutenção” | Recupera todas as solicitações encaminhadas. (**RI01**, **RN01**) |
| Visualiza lista de solicitações | Exibe os dados básicos (protocolo, local, status, data da solicitação). (**RI02**) |
| Seleciona uma solicitação | Exibe os detalhes completos da solicitação. (**RI03**) |

| * Exceções*                                                                                                                                                              |
|-----------------------------------------------------------------------------------------------------------------------------|
| **EX01** | Nenhuma solicitação encaminhada: sistema informa que não há solicitações disponíveis no momento. |

| * Regra de Negocio* |
|-----------------------------------------------------------------------------------------------------------------------------|
| **RN01** | Somente solicitações com status diferente de “rascunho” ou “cancelada” devem ser listadas. |
| **RN02** | O administrador pode apenas visualizar nessa etapa, sem alterar o status diretamente por esse módulo. |


|*Requisitos de interface com o usuario* |
|---------------------------------------------------------------------------------------------------------------------------------|
| **RI01** | A tela deve conter uma tabela com as solicitações encaminhadas, mostrando protocolo, local, status e datas. |
| **RI02** | Cada item da tabela deve ser clicável para exibir os detalhes completos. |
| **RI03** | Os detalhes devem incluir descrição do problema, frentista responsável pelo envio e data/hora. |

Dicionário de Dados

| Nome do Campo      | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                                                | Obrigatório | Único | Default                   |
|--------------------|--------------|----------------------------------|-----------------|-------------------------------------------------------------------------|-------------|-------|----------------------------|
| `protocolo`        | Texto        | `^[A-Z0-9]{8,12}$`               | -               | Código único da solicitação.                                            | Sim         | Sim   | -                          |
| `descricao`        | Texto        | `^[A-Za-z0-9\s]{1,50}$`          | -               | Descrição do problema relatado.                                         | Sim         | Não   | -                          |
| `local_vaga`       | Texto        | `^[A-Za-z0-9\s]{1,50}$`          | -               | Identificação da vaga com problema.                                     | Sim         | Não   | -                          |
| `status_solicitacao` | Texto      | `^(pendente|em_andamento|finalizada)$` | -       | Status atual da solicitação.                                            | Sim         | Não   | `pendente`                 |
| `data_solicitacao` | Data         | `^\d{2}-\d{2}-\d{4}$`            | `dd/mm/yyyy`    | Data do registro da solicitação.                                        | Sim         | Não   | -                          |
| `hora_solicitacao` | Hora         | `^\d{2}:\d{2}$`                  | `HH:mm`         | Hora da solicitação.                                                    | Sim         | Não   | -                          |
| `criado_por`       | Texto        | `^[A-Za-z0-9_]{3,30}$`           | -               | Nome do frentista que criou a solicitação.                              | Sim         | Não   | Sessão do frentista       |
| `encaminhada_para` | Texto        | `^[A-Za-z0-9_]{3,30}$`           | -               | Usuário administrador responsável por acompanhar.                       | Sim         | Não   | Sessão do administrador   |
