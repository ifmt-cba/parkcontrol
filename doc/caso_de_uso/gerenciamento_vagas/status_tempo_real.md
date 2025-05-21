| Nome do Caso de Uso | Status em Tempo Real |
|---------------------|-------------------------------------------|
| **Descrição** | Permite que o frentista visualize em tempo real a situação das vagas do estacionamento (livre, ocupada ou manutenção), facilitando a operação de entrada de veículos e a organização do pátio. |
| **Ator Envolvido** | Frentista |

| **Ator** | **Sistema** |
|----------|-------------|
| Acessa o menu "Status das Vagas" | Carrega e exibe uma lista atualizada das vagas. (RI01) |
| Visualiza o status de cada vaga (livre, ocupada ou em manutenção) | Atualiza o status em tempo real com base nos registros do sistema. (RN01, RI02, EX01) |
| Seleciona uma vaga para mais detalhes  | Exibe informações adicionais: placa do veículo (se ocupada) ou descrição de problema (se em manutenção). (AL01) |

| **Exceções** |
|--------------|
| **EX01** - Falha na atualização da lista: sistema exibe mensagem de erro e permite nova tentativa de atualização. |

| **Alternativas** |
|------------------|
| **AL01** - Se o frentista clicar em uma vaga ocupada, o sistema exibe informações do veículo estacionado. Se clicar em uma vaga em manutenção, exibe os dados da solicitação. |

| **Regras de Negócio** |
|------------------------|
| **RN01** - O sistema deve atualizar automaticamente a visualização de vagas a cada X segundos (parâmetro configurável). |

| **Requisitos de Interface com o Usuário** |
|--------------------------------------------|
| **RI01** - A lista de vagas deve utilizar cores para diferenciar status: verde (livre), vermelho (ocupada) e amarelo (manutenção). |
| **RI02** - A atualização do status das vagas deve ser automática e também permitir atualização manual por botão "Atualizar". |
| **RI03** - Ao clicar em uma vaga, o sistema deve abrir um pop-up ou modal com detalhes da vaga selecionada. |

## Dicionário de Dados

| Nome do Campo       | Tipo de Dado | Expressão Regular               | Máscara         | Descrição                                                                 | Obrigatório | Único | Default                   |
|---------------------|--------------|----------------------------------|-----------------|---------------------------------------------------------------------------|-------------|-------|----------------------------|
| vaga_id             | Inteiro      | ^\d+$                           | -               | ID da vaga.                                                              | Sim         | Sim   | -                          |
| status_vaga         | Texto        | ^(livre\|ocupada\|manutencao)$   | -               | Status atual da vaga.                                                    | Sim         | Não   | -                          |
| placa_veiculo       | Texto        | ^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$  | AAA-0A00        | Placa do veículo (se ocupado).                                            | Não         | Não   | -                          |
| descricao_  | Texto        | ^.{0,255}$                      | -               | Descrição do problema (se em manutenção).                                | Não         | Não   | -                          |
| ultima_atualizacao  | DataHora     | ^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$  | dd/mm/yyyy HH:mm | Data e hora da última atualização da vaga.                               | Sim         | Não   | Atualizado automaticamente |

