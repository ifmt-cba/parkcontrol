| Nome do Caso de Uso       | GerenciarCobranças                                                                                                 |
|---------------------------|---------------------------------------------------------------------------------------------|
| **Descrição**             | Este caso de uso permite ao contador e ao frentista realizar o gerenciamento das cobranças para clientes mensalistas e diaristas. As funcionalidades incluem a geração de cobranças, envio por email, emissão de recibos e acompanhamento de inadimplência. |
| **Ator Envolvido**        | Contador, Frentista                                                                                                |

| **Interação entre Ator e Sistema**           |                                                                                                                       |
|---------------------------------------------|---------------------------------------------------------------------------------------------|
| **Ator**                                     | **Sistema**                                                                                                           |
| Contador acessa a opção "Gerar cobrança mensalista". | Sistema cria os registros de cobrança com base nas mensalidades dos planos ofertados (RI01, RN01).|
| Contador seleciona "Enviar cobrança por email". | Sistema envia as cobranças aos respectivos clientes mensalistas por email (RN02).                             |
| Frentista acessa "Gerar cobrança diarista".  | Sistema calcula a cobrança com base no tempo de permanência e registra o valor (RI02, RN03).                        |
| Frentista seleciona "Emitir recibo cliente diarista". | Sistema gera o recibo com os dados da cobrança registrada (RI04, RN04).                                              |
| Contador acessa "Acompanhar inadimplência".  | Sistema exibe lista de clientes inadimplentes com status das cobranças (RI04, RN05).                                 |

| **Exceções**   |                                                                                                                                  |
|----------------|--------------------------------------------------------------------------------------------------------------------------|
| EX01 | Tentativa de gerar cobrança para cliente mensalista sem plano cadastrado. Mensagem: "Cliente não possui plano ativo".|
| EX02 | Falha no envio de email. Mensagem: "Erro ao enviar cobrança. Verifique a conexão ou endereço do destinatário".|
| EX03 | Cliente não encontrado para cobrança diarista. Mensagem: "Dados do cliente não localizados".                              |
| EX04 | Recibo solicitado antes do registro da cobrança. Mensagem: "Nenhuma cobrança disponível para gerar recibo".   |

| **Alternativas** |                                                                                                                                  |
|------------------|------------------------------------------------------------------------------------------------------------------------|
| AL01 | Se o sistema de cobrança por email estiver indisponível, o contador pode exportar a cobrança em PDF para um envio manual por outros métodos de comunicação.|
| AL02 | Caso o frentista não tenha acesso ao sistema, ele poderá registrar a cobrança diarista manualmente em formulário físico.        |

| **Regras de Negócio** |                                                                                                                            |
|-----------------------|----------------------------------------------------------------------------------------------------------------|
| RN01 | A geração de cobrança para mensalistas deve ocorrer automaticamente no início de cada mês.                  |
| RN02 | As cobranças devem ser enviadas para os emails cadastrados no sistema.                                                   |
| RN03 | O valor da cobrança diarista é baseado nas horas de uso da vaga, de acordo com a tarifa configurada.      |
| RN04 | Somente cobranças concluídas podem gerar recibo.                                                                                      |
| RN05 | Clientes com cobranças vencidas há mais de 5 dias devem constar na lista de inadimplência.                      |

| **Requisitos de Interface com o Usuário** |                                                                                                             |
|------------------------------------------|----------------------------------------------------------------------------------------|
| RI01 | Tela com botão "Gerar cobrança mensalista" e seleção por mês/cliente.            |
| RI02 | Interface para cálculo de cobrança diarista com entrada de horários.                 |
| RI03 | Botão de emissão de recibo com exportação em PDF.                                        |
| RI04 | Painel de inadimplência com filtro por período e status da cobrança.                |
