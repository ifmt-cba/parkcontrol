## Nome do Caso de Uso  
**Encerrar Solicitação de Manutenção**

## Descrição  
Permite ao administrador registrar o encerramento de uma solicitação de manutenção, após a conclusão do serviço, atualizando seu status e registrando a data e o responsável pelo encerramento.

## Ator Envolvido  
**Administrador**

---

## Interação entre Ator e Sistema

| **Ator** | **Sistema** |
|----------|-------------|
| Acessa o módulo de solicitações. | Exibe a lista de solicitações com opções. (RI01) |
| Clica em "Visualizar" em uma solicitação. | Exibe os detalhes da solicitação. |
| Clica na opção "Encerrar Solicitação". | Exibe campo para confirmação e preenchimento da data e responsável. |
| Confirma o encerramento. | Atualiza o status para "resolvido", libera a vaga e salva data e usuário responsável. (RN01, RN02, RI02) |

---

## Exceções

| **Código** | **Descrição** |
|-----------|----------------|
| EX01 | Solicitação já encerrada: ação não permitida. |
| EX02 | Dados obrigatórios não preenchidos. |

---

## Alternativas

| **Código** | **Descrição** |
|-----------|----------------|
| AL01 | O administrador pode cancelar o encerramento a qualquer momento. |

---

## Regras de Negócio

| **Código** | **Descrição** |
|-----------|----------------|
| RN01 | Apenas solicitações com status "pendente" ou "em andamento" podem ser encerradas. |
| RN02 | O encerramento deve registrar a data e o usuário responsável. |

---

## Requisitos de Interface com o Usuário

| **Código** | **Descrição** |
|-----------|----------------|
| RI01 | Exibir botão "Encerrar Solicitação" apenas para solicitações ativas. |
| RI02 | Exibir formulário simples para encerramento com campos de confirmação. |

---

## Dicionário de Dados (Campos Relacionados)

| **Campo** | **Tipo** | **Descrição** | **Obrigatório** |
|-----------|----------|----------------|------------------|
| status | Texto | Deve ser atualizado para "resolvido". | Sim |
| data_resolucao | Data | Data do encerramento da solicitação. | Sim |
| resolvido_por | Texto | Identificação do usuário que encerrou. | Sim |
