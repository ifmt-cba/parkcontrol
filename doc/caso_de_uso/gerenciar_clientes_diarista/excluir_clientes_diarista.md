| Nome do Caso de Uso       | Excluir Cliente Diarista |
|---------------------------|---------------------------|
| *Descrição*               | Permite ao administrador excluir um cadastro de cliente diarista do sistema. |
| *Ator Envolvido*          | Administrador |

| *Interação entre Ator e Sistema* | |
|----------------------------------|-------------------------------------------------------------------------|
| *Ator*                           | *Sistema*                                                              |
| Solicita exclusão de cliente diarista | Exibe confirmação da ação solicitada. (RI12) |
| Confirma a exclusão | Sistema remove o cliente do cadastro e exibe mensagem de sucesso. (RI13) |

| *Exceções* |
|------------|
| EX11 - Cliente não encontrado. Sistema exibe mensagem de erro. |
| EX12 - Erro de conexão com banco de dados. Sistema exibe mensagem de falha ao excluir. |
| EX13 - Cliente com movimentações financeiras associadas. Sistema bloqueia exclusão e orienta desassociar. |

| *Alternativas* |
|----------------|
| AL10 - Administrador pode cancelar a exclusão antes da confirmação. |
| AL11 - Sistema pode inativar o cliente ao invés de excluir definitivamente. |
| AL12 - Sistema gera um backup dos dados antes da exclusão. |

| *Regras de Negócio* |
|---------------------|
| RN13 - A exclusão só é permitida se o cliente não possuir movimentações financeiras vinculadas. |
| RN14 - Operações de exclusão devem ser registradas no log do sistema. |
| RN15 - Exclusão lógica (inativação) pode ser aplicada ao invés de remoção física dos dados. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI12 - Exibir caixa de confirmação ("Tem certeza que deseja excluir?") antes da ação definitiva. |
| RI13 - Mensagem visual clara após sucesso ou falha na operação. |
| RI14 - Botão de 'Cancelar' acessível durante a confirmação da exclusão. |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara | Descrição | Obrigatório | Único | Default |
|---------------|--------------|-------------------|---------|-----------|-------------|-------|---------|
| nome          | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$ | - | Nome completo do cliente. | Sim | Não | - |
| cpf           | Texto        | ^\d{3}\.\d{3}\.\d{3}-\d{2}$ | 000.000.000-00 | CPF do cliente. | Sim | Sim | - |
| telefone      | Texto        | ^\(\d{2}\)\s\d{4,5}-\d{4}$ | (00) 00000-0000 | Número de telefone do cliente. | Sim | Não | - |
| email         | Texto        | ^[\w\.-]+@[\w\.-]+\.\w{2,}$ | - | E-mail do cliente. | Não | Sim | - |
| placa         | Texto        | ^([A-Z]{3}-\d{4}or^([A-Z]{3}-\d{4} or [A-Z]{3}\d[A-Z]\d{2})$ | AAA-0000 ou AAA0A00 | Placa do veículo (modelo antigo ou Mercosul). | Sim | Sim | - |
| status        | Booleano     | ^(ativo  \| inativo)$ | - | Indica se o cliente está ativo ou inativo. | Sim | Não | ativo |
| data_criacao  | Data          | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa | Data de cadastro do cliente. | Sim | Não | Gerado automaticamente |
| excluido_por  | Texto         | ^[A-Za-zÀ-ÿ\s]{3,50}$ | - | Nome do usuário que realizou a exclusão. | Sim | Não | - |
| data_exclusao | Data          | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa | Data da exclusão do cliente. | Sim | Não | Gerado automaticamente |

