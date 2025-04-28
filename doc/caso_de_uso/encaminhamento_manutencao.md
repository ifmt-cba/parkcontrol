| Nome do Caso de Uso       | Encaminhamento de Manutenção                                                                                     |
|---------------------------|------------------------------------------------------------------------------------------------------|
| Descrição             | Permite que o administrador analise e aprove solicitações de manutenção. Caso aprovada, a vaga torna-se temporariamente indisponível. |
| Ator Envolvido        | Administrador. |

| Interação entre Ator e Sistema            |                                                                                               |
|----------------------------------------------|-----------------------------------------------------------------------------------------------|
| Ator                               | Sistema                                                                                   |
| Administrador acessa o módulo de manutenções. | Exibe lista de solicitações pendentes.|
| Administrador aprova a solicitação. | Sistema muda o status da vaga para "em manutenção". |
| Administrador rejeita a solicitação. | Sistema marca a solicitação como "rejeitada" e mantém a vaga ativa. |

| Exceções                                   |                                                                                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------|
| EX01                    | O administrador tenta aprovar uma solicitação de manutenção para uma vaga que já se encontra com status "em manutenção", mesmo que a solicitação ainda esteja pendente. O sistema bloqueia a ação para evitar duplicidade. |
| EX02                    | O administrador tenta aprovar ou rejeitar uma solicitação que já foi tratada. O sistema informa que a ação não é permitida, pois a solicitação está finalizada. |

| Alternativas        |                                                                                                      |
|-------------------------|------------------------------------------------------------------------------------------------------|
| AL01                    | O administrador pode rejeitar uma solicitação com uma justificativa e o sistema envia uma notificação ao frentista.
| AL02                    | O administrador pode identificar uma necessidade de manutenção sem solicitação do frentista e registrar diretamente no sistema a vaga como "em manutenção". |

| Regras de Negócio   |                                                                                                      |
|-------------------------|------------------------------------------------------------------------------------------------------|
|RN01 | O administrador pode iniciar uma solicitação de manutenção diretamente, sem depender do frentista. |
|RN02 | Apenas administradores podem aprovar ou rejeitar solicitações de manutenção. |
|RN03 | Vagas com status “em manutenção” ficam indisponíveis para entrada de veículos até que o status seja alterado manualmente. |

| Requisitos de Interface com o Usuário |                                                                                       |
|------------------------------------------|----------------------------------------------------------------------------------------|
|RI01 | O sistema deve exibir uma lista de solicitações de manutenção pendentes com filtros por data, vaga e status. |
|RI02 | Deve haver um botão visível para “Aprovar”, "Rejeitar" e "Vizualizar detalhes". |
|RI03 | O status da vaga "em manutenção" deve estar claramente visível com ícones intuitivos. |
