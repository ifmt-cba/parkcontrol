## Nome do Caso de Uso  
**Gerenciar Solicitações de Manutenção de Vagas**

## Descrição  
Permite ao administrador visualizar, encaminhar, acompanhar e encerrar solicitações de manutenção de vagas realizadas por usuários do sistema, garantindo o controle e a resolução adequada das demandas.

## Ator Envolvido  
**Administrador**

---

## Interação entre Ator e Sistema

| **Ator** | **Sistema** |
|----------|-------------|
| Acessa o módulo de solicitações de manutenção. | Exibe a lista de solicitações com filtros e ações disponíveis. (RI01, RI02) |
| Seleciona uma solicitação. | Exibe os detalhes da solicitação. |
| Clica em "Encaminhar Solicitação". | Exibe formulário para selecionar responsável e adicionar observações. (RI03) |
| Confirma encaminhamento. | Atualiza status para "em andamento" e registra o responsável. (RN02) |
| Após resolução, clica em "Encerrar Solicitação". | Exibe campos para encerramento. (RI04) |
| Confirma encerramento. | Atualiza status para "resolvido", salva data e responsável. (RN03) |

---

## Exceções

| **Código** | **Descrição** |
|-----------|----------------|
| EX01 | Solicitação já encerrada: nenhuma ação permitida. |
| EX02 | Falta de dados obrigatórios no encaminhamento ou encerramento. |
| EX03 | Falha na atualização do status. |

---

## Alternativas

| **Código** | **Descrição** |
|-----------|----------------|
| AL01 | O administrador pode utilizar filtros por status, data, setor ou prioridade. |
| AL02 | O administrador pode cancelar as ações de encaminhamento ou encerramento antes da confirmação. |

---

## Regras de Negócio

| **Código** | **Descrição** |
|-----------|----------------|
| RN01 | Apenas administradores podem gerenciar solicitações. |
| RN02 | Encaminhamentos só são possíveis para solicitações com status "pendente". |
| RN03 | Encerramentos só podem ser feitos após o encaminhamento. |

---

## Requisitos de Interface com o Usuário

| **Código** | **Descrição** |
|-----------|----------------|
| RI01 | A interface deve exibir todas as solicitações em tabela com filtros. |
| RI02 | Solicitações devem exibir ícones ou botões de ação para visualização, encaminhamento e encerramento. |
| RI03 | Encaminhamento deve conter campo para selecionar responsável e registrar observações. |
| RI04 | Encerramento deve registrar data, responsável e observações. |

---

## Dicionário de Dados (Campos Relacionados)

| **Campo** | **Tipo** | **Descrição** | **Obrigatório** |
|-----------|----------|----------------|------------------|
| id_solicitacao | Inteiro | Identificador da solicitação. | Sim |
| status | Texto | Status atual da solicitação (pendente, em andamento, resolvido). | Sim |
| encaminhado_para | Texto | Nome ou ID do responsável designado. | Sim (no encaminhamento) |
| observacoes | Texto Longo | Observações da solicitação ou do encaminhamento. | Não |
| data_encerramento | Data | Data de encerramento da solicitação. | Sim (no encerramento) |
| resolvido_por | Texto | Administrador responsável pelo encerramento. | Sim |
