| Nome do Caso de Uso | Detalhamento de Gerenciamento de Vagas |
|---------------------|-------------------------------------------|
| **Descrição** |  Permite ao frentista controlar a ocupação, liberação, manutenção, monitoramento em tempo real e geração de relatórios sobre as vagas de estacionamento. |
| **Ator Envolvido** |  Frentista |

| Caso de Uso | Descrição |
|-------------|-----------|
| **Registrar Entrada de Veículo** | Permite que o frentista registre a entrada de veículos diaristas ou reconheça automaticamente mensalistas, vinculando-os a vagas disponíveis. |
| **Registrar Saída de Veículo** | Permite que o frentista registre a saída de veículos, liberando vagas ocupadas e calculando o valor a ser cobrado para clientes diaristas. |
| **Relatório de Uso de Vagas** | Permite que o frentista gere relatórios sobre o uso das vagas, incluindo histórico de entradas, saídas, tempo médio de ocupação e vagas mais utilizadas. |
| **Solicitar Manutenção de Vaga** | Permite que o frentista solicite manutenção em vagas que apresentem problemas físicos, enviando uma solicitação com descrição e imagem opcional. |
| **Status em Tempo Real** | Permite ao frentista visualizar o status atualizado de todas as vagas do estacionamento, facilitando a organização e agilidade na operação. |

| Código | Descrição |
|--------|-----------|
| **EX01** | Campos obrigatórios não preenchidos durante entradas, saídas ou solicitações. |
| **EX02** | Veículo tentando entrar já registrado como presente. |
| **EX03** | Falha na comunicação com o servidor ao solicitar manutenção, consultar mapa ou gerar relatório. |
| **EX04** | Tentativa de gerar relatório com filtros inválidos ou período de tempo não selecionado. |

| Código | Descrição |
|--------|-----------|
| **RN01** | O sistema não deve permitir a entrada de veículos sem vaga disponível. |
| **RN02** | Cada vaga só pode ter um único status simultâneo: livre, ocupada, manutenção. |
| **RN03** | O sistema deve calcular a permanência e valores automaticamente com base nos horários registrados. |
| **RN04** | Solicitações de manutenção devem gerar protocolo único e bloquear a vaga automaticamente. |
| **RN05** | Atualização do status de vagas deve ocorrer automaticamente a cada X segundos, e manualmente sob comando do frentista. |
| **RN06** | Relatórios devem conter dados atualizados e permitir filtros por período, tipo de veículo e status da vaga. |

## Requisitos de Interface Globais

| Código | Descrição |
|--------|-----------|
| **RI01** | O sistema deve utilizar cores e ícones claros para indicar o status das vagas no mapa. |
| **RI02** | Os formulários devem validar obrigatoriamente os dados em tempo real. |
| **RI03** | Após qualquer ação (entrada, saída, manutenção, relatório), o sistema deve exibir uma confirmação visual clara. |
| **RI04** | Deve ser possível filtrar visualmente o mapa por status: livre, ocupada, manutenção. |
| **RI05** | A geração de relatórios deve permitir filtros rápidos e exportação em formatos como PDF ou CSV. |

## Dicionário de Dados Global

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `vaga_id` | Inteiro | Identificação única da vaga. |
| `status_vaga` | Texto | Estado atual da vaga (`livre`, `ocupada`, `manutencao`). |
| `placa_veiculo` | Texto | Placa do veículo associado à vaga (se ocupada). |
| `data_entrada` | Data | Data de entrada do veículo. |
| `hora_entrada` | Hora | Hora de entrada do veículo. |
| `data_saida` | Data | Data de saída do veículo. |
| `hora_saida` | Hora | Hora de saída do veículo. |
| `descricao_problema` | Texto | Descrição do problema na vaga (em caso de manutenção). |
| `protocolo_manutencao` | Texto | Número do protocolo gerado para a manutenção. |
| `usuario_responsavel` | Texto | Usuário (frentista) que realizou a operação. |
| `data_criacao` | DataHora | Data e hora da criação do registro no sistema. |
| `tempo_ocupacao` | Número | Tempo total de ocupação de uma vaga para fins de relatório. |
| `tipo_veiculo` | Texto | Indicação do tipo de veículo (carro, moto). |

---

> **Observação:**  
> Todas as operações realizadas no gerenciamento de vagas são registradas automaticamente para fins de auditoria e rastreabilidade do sistema.

