


| Nome do Caso de Uso       | Gerenciar Usuário |
|---------------------------|-------------------|
| *Descrição*               | Permite que o Administrador cadastre, edite, visualize, exclua e recupere a senha de usuários no sistema ParkControl, mantendo controle de acesso e permissões. |
| *Ator Envolvido*          | Administrador |

---


| *Interação entre Ator e Sistema* | |
|----------------------------------|---|
| *Ator* | *Sistema* |
| Acessa a opção "Gerenciar Usuário" no menu principal. | Exibe tela com lista de usuários em tabela, com ações visíveis para criar, editar, visualizar, excluir e recuperar senha. (RI01) |
| Clica em "Criar Usuário". | Exibe formulário para preenchimento dos dados obrigatórios: nome, e-mail, senha e perfil de acesso. (RI02) |
| Preenche os dados e clica em "Salvar". | Valida campos obrigatórios (nome, e-mail, senha, perfil de acesso), verifica unicidade do e-mail e salva o novo usuário no sistema. (EX01, EX02, RN02, RN03, RI02) |
| Seleciona um usuário na lista e clica em "Editar". | Exibe formulário com dados atuais preenchidos para edição. (RI02) |
| Altera os dados e clica em "Atualizar". | Valida novamente os campos obrigatórios e atualiza o registro do usuário. (EX01, RN02, RN03, RI02) |
| Clica em "Visualizar" em um usuário. | Exibe detalhes completos do usuário, incluindo data de criação e última modificação. (RN03) |
| Clica em "Excluir" em um usuário. | Solicita confirmação da ação e, se confirmada, remove o usuário do sistema. (RN01) |
| Clica em "Recuperar Senha" em um usuário. | Exibe campo para inserir o e-mail ou nome do usuário para enviar instruções de recuperação de senha. (RI02) |
| Preenche o e-mail/nome e clica em "Enviar". | Envia um e-mail com um link para redefinir a senha ou um código de recuperação. (EX03, RI02) |

---


| *Exceções* |
|------------|
| EX01 - Campos obrigatórios não preenchidos: o sistema destaca os campos em falta e exibe mensagem de erro. |
| EX02 - E-mail já cadastrado: o sistema bloqueia o cadastro e informa sobre duplicidade do e-mail. |
| EX03 - E-mail não encontrado: o sistema informa que o e-mail não está cadastrado e solicita uma nova tentativa ou contato com o suporte. |

---



| *Alternativas* |
|----------------|
| AL01 - O administrador pode cancelar as ações de criação ou edição, retornando à tela de listagem de usuários. |
| AL02 - Pode usar filtros ou a barra de busca para localizar usuários por nome, e-mail ou perfil de acesso. |
| AL03 - O administrador pode acessar diretamente o link de recuperação de senha caso o usuário tenha problemas para recuperá-la. |

---



| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com perfil de administrador podem acessar a funcionalidade de gerenciamento de usuários. |
| RN02 - Cada usuário deve possuir um e-mail único no sistema. |
| RN03 - O sistema deve registrar automaticamente a data e hora de criação e da última modificação dos usuários. |
| RN04 - O sistema deve garantir que a recuperação de senha seja realizada apenas por meio de um e-mail válido e cadastrado. |

---



| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A tela deve apresentar os usuários em uma tabela, com botões visíveis para editar, visualizar, excluir e recuperar senha. |
| RI02 - O formulário de recuperação de senha deve exibir campos claros para o preenchimento de e-mail ou nome do usuário e exibir mensagens de erro, se necessário. |
| RI03 - A interface deve permitir ao administrador realizar a busca por nome, e-mail ou perfil de acesso. |

---

# Dicionário de Dados

| Nome do Campo     | Tipo de Dado    | Expressão Regular                         | Máscara               | Descrição                                                                 | Obrigatório | Único | Default               |
|-------------------|-----------------|--------------------------------------------|------------------------|---------------------------------------------------------------------------|-------------|-------|-----------------------|
| nome              | Texto            | ^[A-Za-zÀ-ÿ\s]{3,50}$                      | -                      | Nome completo do usuário, entre 3 e 50 caracteres.                        | Sim         | Não   | -                     |
| email             | Texto            | ^[\w\.-]+@[\w\.-]+\.\w{2,}$                | -                      | Endereço de e-mail válido e único no sistema.                             | Sim         | Sim   | -                     |
| senha             | Texto (hash)     | .{8,}                                     | -                      | Senha do usuário, armazenada de forma criptografada.                      | Sim         | Não   | -                     |
| perfil_acesso     | Texto            | ^(Administrador\|Operador\|Visualizador)$  | -                      | Perfil de acesso (Administrador, Operador ou Visualizador).               | Sim         | Não   | Visualizador          |
| status            | Booleano         | ^(ativo\|inativo)$                         | -                      | Indica se o usuário está ativo ou inativo no sistema.                     | Não         | Não   | ativo                 |
| data_criacao      | Data             | ^\d{2}-\d{2}-\d{4}$                        | dd/mm/aaaa              | Data em que o usuário foi cadastrado, gerado automaticamente.             | Sim         | Não   | Gerado pelo sistema   |
| ultima_alteracao  | DataHora         | ^\d{}-\d{2}-\d{2} \d{4}:\d{2}:\d{2}$      | dd/mm/aaaa hh:mm:ss     | Data e hora da última modificação nos dados do usuário.                   | Não         | Não   | Atualizado automaticamente |
| criado_por        | Texto            | ^[A-Za-z0-9]{3,30}$                       | -                      | Identificador do administrador que cadastrou o usuário.                  | Sim         | Não   | Gerado pelo sistema   |

---
