| Nome do Caso de Uso       | Visualizar Cobrança Diarista |
|---------------------------|------------------------------|
| *Descrição*               | Permite ao frentista consultar as cobranças registradas de clientes diaristas, filtrando por status, placa ou data. |
| *Ator Envolvido*          | Frentista |

---

| *Interação entre Ator e Sistema* |                                                  |
|----------------------------------|--------------------------------------------------|
| *Ator*                           | *Sistema*                                        |
| O frentista acessa a funcionalidade "Visualizar Cobrança Diarista". | Sistema exibe uma tela com filtros para busca: placa do veículo, status da cobrança, data de criação. (RI01) |
| O frentista preenche um ou mais filtros de busca. | Sistema valida os filtros preenchidos. (RI02) |
| O frentista solicita a busca. | Sistema busca e lista as cobranças correspondentes. Se não houver resultados, informa ao usuário. (EX01) |
| O frentista pode visualizar detalhes de uma cobrança específica selecionada na lista. | Sistema exibe as informações detalhadas da cobrança selecionada. (RI03) |
| O frentista pode optar por refinar a pesquisa ou limpar os filtros e realizar uma nova busca. | Sistema limpa os filtros e exibe novamente a tela de busca vazia. (AL01) |

---

| *Exceções* |
|------------|
| EX01 - Nenhuma cobrança encontrada para os filtros aplicados: o sistema exibe mensagem de "Nenhum registro encontrado" e mantém o usuário na tela de busca. |

---

| *Alternativas* |
|----------------|
| AL01 - O frentista pode limpar os filtros preenchidos e realizar uma nova busca. |

---

| *Regras de Negócio* |
|---------------------|
| RN01 - Apenas cobranças pertencentes à unidade operacional do frentista podem ser visualizadas. |
| RN02 - A busca deve permitir múltiplos filtros combinados (placa + status + data). |

---

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - Formulário de filtros deve conter campos para placa do veículo, status da cobrança (pendente/pago) e data de criação. |
| RI02 - Botões \"Buscar\" e \"Limpar Filtros\" devem estar visíveis na interface. |
| RI03 - Ao clicar em um resultado, o sistema deve exibir todos os dados detalhados da cobrança selecionada. |

---

### Dicionário de Dados

| Nome do Campo        | Tipo de Dado | Expressão Regular               | Máscara        | Descrição                                          | Obrigatório | Único | Default |
|----------------------|--------------|----------------------------------|----------------|----------------------------------------------------|-------------|-------|---------|
| placa_veiculo        | Texto         | `^[A-Z]{3}-[0-9][A-Z0-9][0-9]{2}$` | AAA-0A00       | Placa do veículo para busca.                       | Não         | Não   | -       |
| status_cobranca      | Texto         | `^(pendente\|pago)$`               | -              | Status atual da cobrança (filtro).                 | Não         | Não   | -       |
| data_criacao         | Data          | `^\d{4}-\d{2}-\d{2}$`             | dd/mm/aaaa     | Data de criação da cobrança (filtro).              | Não         | Não   | -       |
| id_cobranca          | Inteiro       | `^\d+$`                           | -              | Identificador único da cobrança para consulta detalhada. | Sim         | Sim   | -       |

---
