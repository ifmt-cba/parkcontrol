

| Nome do Caso de Uso       | Excluir Usuário |
|---------------------------|-----------------|
| *Descrição*               | Permite que o Administrador exclua um usuário existente no sistema ParkControl. A exclusão é feita após confirmação do Administrador, removendo permanentemente o usuário e seus dados. |
| *Ator Envolvido*          | Administrador |

---



| *Interação entre Ator e Sistema* | |
|----------------------------------|---|
| *Ator* | *Sistema* |
| Acessa a opção "Gerenciar Usuário" no menu principal. | Exibe a tela com a lista de usuários e as opções para criar, editar, visualizar e excluir. (RI01) |
| Clica em "Excluir" ao lado de um usuário. | Exibe uma solicitação de confirmação para a exclusão do usuário selecionado. (RI02) |
| Confirma a exclusão. | Remove o usuário do sistema permanentemente e exibe mensagem de sucesso. (EX01, RN01) |

---



| *Exceções* |
|------------|
| EX01 - O administrador cancela a exclusão: o sistema retorna à tela de listagem de usuários sem realizar a exclusão. |
| EX02 - O usuário não pode ser excluído se estiver associado a dados críticos no sistema (caso de uma regra de negócio mais complexa), e o sistema exibe mensagem informando a impossibilidade da operação. |

---



| *Alternativas* |
|----------------|
| AL01 - O administrador pode cancelar a operação de exclusão, retornando à tela de listagem de usuários. |
| AL02 - O administrador pode buscar por nome ou e-mail de um usuário específico antes de tentar excluir. (RI03) |

---


| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com perfil de administrador podem excluir usuários do sistema. |

---


| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A tela de listagem de usuários deve exibir uma opção visível de "Excluir" para cada usuário. |
| RI02 - O sistema deve exibir uma confirmação clara antes de realizar a exclusão de um usuário. |
| RI03 - A interface deve permitir ao administrador localizar facilmente o usuário a ser excluído através de busca por nome ou e-mail. |

---

# Dicionário de Dados

| Nome do Campo     | Tipo de Dado    | Expressão Regular                         | Máscara               | Descrição                                                                 | Obrigatório | Único | Default               |
|-------------------|-----------------|--------------------------------------------|------------------------|---------------------------------------------------------------------------|-------------|-------|-----------------------|
| nome              | Texto            | ^[A-Za-zÀ-ÿ\s]{3,50}$                      | -                      | Nome completo do usuário, entre 3 e 50 caracteres.                        | Sim         | Não   | -                     |
| email             | Texto            | ^[\w\.-]+@[\w\.-]+\.\w{2,}$                | -                      | Endereço de e-mail válido e único no sistema.                             | Sim         | Sim   | -                     |
| perfil_acesso     | Texto            | ^(Administrador\|Operador\|Visualizador)$  | -                      | Perfil de acesso (Administrador, Operador ou Visualizador).               | Sim         | Não   | Visualizador          |
| status            | Booleano         | ^(ativo\|inativo)$                         | -                      | Indica se o usuário está ativo ou inativo no sistema.                     | Não         | Não   | ativo                 |
| ultima_alteracao  | DataHora         | ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$     | dd/mm/aaaa hh:mm:ss    | Data e hora da última modificação nos dados do usuário.                   | Não         | Não   | Atualizado automaticamente |
| data_criacao      | Data             | ^\d{2}-\d{2}-\d{4}$                        | dd/mm/aaaa              | Data em que o usuário foi cadastrado, gerado automaticamente.             | Sim         | Não   | Gerado pelo sistema   |
| criado_por        | Texto            | ^[A-Za-z0-9]{3,30}$                       | -                      | Identificador do administrador que cadastrou o usuário.                  | Sim         | Não   | Gerado pelo sistema   |

---
