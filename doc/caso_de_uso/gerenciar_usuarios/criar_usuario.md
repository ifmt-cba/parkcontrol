
| Nome do Caso de Uso       | Criar Usuário |
|---------------------------|---------------|
| *Descrição*               | Permite que o Administrador crie um novo usuário no sistema ParkControl, preenchendo dados obrigatórios como nome, e-mail, senha e perfil de acesso. |
| *Ator Envolvido*          | Administrador |

---


| *Interação entre Ator e Sistema* | |
|----------------------------------|---|
| *Ator* | *Sistema* |
| Acessa a opção "Gerenciar Usuário" no menu principal. | Exibe a tela com a lista de usuários e as opções para criar, editar, visualizar e excluir. (RI01) |
| Clica em "Criar Usuário". | Exibe um formulário para o preenchimento dos dados obrigatórios: nome, e-mail, senha e perfil de acesso. (RI02) |
| Preenche os dados e clica em "Salvar". | Valida os campos obrigatórios (nome, e-mail, senha, perfil de acesso), verifica a unicidade do e-mail e salva o novo usuário no sistema. (EX01, EX02, RN02, RN03, RI02) |

---



| *Exceções* |
|------------|
| EX01 - Campos obrigatórios não preenchidos: o sistema exibe mensagem de erro destacando os campos em falta. |
| EX02 - E-mail já cadastrado: o sistema bloqueia o cadastro e informa sobre duplicidade do e-mail. |

---



| *Alternativas* |
|----------------|
| AL01 - O administrador pode cancelar a operação, retornando à tela de listagem de usuários. |
| AL02 - O administrador pode usar a busca para localizar um usuário por nome ou e-mail antes de tentar criar um novo. |

---



| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com perfil de administrador podem acessar a funcionalidade de criação de usuários. |
| RN02 - Cada usuário deve possuir um e-mail único no sistema. |
| RN03 - O sistema deve registrar automaticamente a data e hora de criação do usuário. |

---


| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A tela deve exibir um formulário com campos para nome, e-mail, senha e perfil de acesso. |
| RI02 - O formulário deve apresentar validações visuais e mensagens de erro claras em tempo real para campos obrigatórios e erros de e-mail duplicado. |

---

# Dicionário de Dados

| Nome do Campo     | Tipo de Dado    | Expressão Regular                         | Máscara               | Descrição                                                                 | Obrigatório | Único | Default               |
|-------------------|-----------------|--------------------------------------------|------------------------|---------------------------------------------------------------------------|-------------|-------|-----------------------|
| nome              | Texto            | ^[A-Za-zÀ-ÿ\s]{3,50}$                      | -                      | Nome completo do usuário, entre 3 e 50 caracteres.                        | Sim         | Não   | -                     |
| email             | Texto            | ^[\w\.-]+@[\w\.-]+\.\w{2,}$                | -                      | Endereço de e-mail válido e único no sistema.                             | Sim         | Sim   | -                     |
| senha             | Texto (hash)     | .{8,}                                     | -                      | Senha do usuário, armazenada de forma criptografada.                      | Sim         | Não   | -                     |
| perfil_acesso     | Texto            | ^(Administrador\|Operador\|Visualizador)$  | -                      | Perfil de acesso (Administrador, Operador ou Visualizador).               | Sim         | Não   | Visualizador          |
| data_criacao      | Data             | ^\d{2}-\d{2}-\d{4}$                        | dd/mm/aaaa              | Data em que o usuário foi cadastrado, gerado automaticamente.             | Sim         | Não   | Gerado pelo sistema   |

---
