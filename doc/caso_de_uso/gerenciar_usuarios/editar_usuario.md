

| Nome do Caso de Uso       | Editar Usuário |
|---------------------------|-----------------|
| *Descrição*               | Permite que o Administrador edite os dados de um usuário existente no sistema ParkControl, incluindo nome, e-mail, perfil de acesso e status. |
| *Ator Envolvido*          | Administrador |

---


| *Interação entre Ator e Sistema* | |
|----------------------------------|---|
| *Ator* | *Sistema* |
| Acessa a opção "Gerenciar Usuário" no menu principal. | Exibe a tela com a lista de usuários e as opções para criar, editar, visualizar e excluir. (RI01) |
| Clica em "Editar" ao lado de um usuário. | Exibe um formulário com os dados atuais do usuário, permitindo alterações nos campos: nome, e-mail, perfil de acesso e status. (RI02) |
| Altera os dados e clica em "Atualizar". | Valida os campos obrigatórios, verifica a unicidade do e-mail e atualiza as informações no sistema. (EX01, EX02, RN02, RN03, RI02) |

---


| *Exceções* |
|------------|
| EX01 - Campos obrigatórios não preenchidos: o sistema exibe mensagem de erro destacando os campos em falta. |
| EX02 - E-mail já cadastrado: o sistema bloqueia a atualização e informa sobre duplicidade do e-mail. |

---

| *Alternativas* |
|----------------|
| AL01 - O administrador pode cancelar a operação, retornando à tela de listagem de usuários. |
| AL02 - O administrador pode usar filtros ou a barra de busca para localizar rapidamente o usuário a ser editado. |

---


| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com perfil de administrador podem acessar a funcionalidade de edição de usuários. |
| RN02 - Cada usuário deve possuir um e-mail único no sistema, mesmo após edição. |
| RN03 - O sistema deve registrar automaticamente a data e hora da última modificação no usuário. |

---



| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A tela de edição deve exibir um formulário com campos para nome, e-mail, perfil de acesso e status do usuário. |
| RI02 - O formulário de edição deve apresentar validações visuais e mensagens de erro claras em tempo real para campos obrigatórios e erros de e-mail duplicado. |

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
