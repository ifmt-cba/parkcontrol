

| Nome do Caso de Uso       | Visualizar Usuário |
|---------------------------|---------------------|
| *Descrição*               | Permite que o Administrador visualize os detalhes completos de um usuário, incluindo dados como nome, e-mail, perfil de acesso e histórico de alterações. |
| *Ator Envolvido*          | Administrador |

---



| *Interação entre Ator e Sistema* | |
|----------------------------------|---|
| *Ator* | *Sistema* |
| Acessa a opção "Gerenciar Usuário" no menu principal. | Exibe a tela com a lista de usuários e as opções para criar, editar, visualizar e excluir. (RI01) |
| Clica em "Visualizar" ao lado de um usuário. | Exibe os detalhes completos do usuário selecionado, incluindo nome, e-mail, perfil de acesso, status, data de criação e última modificação. (RN03) |

---



| *Exceções* |
|------------|
| EX01 - Usuário não encontrado: o sistema exibe uma mensagem de erro informando que o usuário não foi encontrado. |
| EX02 - Falha ao carregar os dados: o sistema exibe uma mensagem de erro informando que não foi possível carregar os detalhes do usuário. |

---



| *Alternativas* |
|----------------|
| AL01 - O administrador pode retornar à tela de listagem de usuários, cancelando a visualização. |
| AL02 - O administrador pode usar filtros ou a barra de busca para localizar rapidamente o usuário a ser visualizado. |

---



| *Regras de Negócio* |
|---------------------|
| RN01 - Somente usuários com perfil de administrador podem acessar a funcionalidade de visualização de usuários. |
| RN02 - O sistema deve garantir que todos os detalhes do usuário sejam visíveis, incluindo data de criação e última modificação. |

---



| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI01 - A tela de visualização deve exibir informações completas sobre o usuário selecionado, incluindo nome, e-mail, perfil de acesso, status, data de criação e última modificação. |
| RI02 - O administrador deve ter a opção de voltar para a tela de listagem de usuários a qualquer momento durante a visualização. |

---

# Dicionário de Dados

| Nome do Campo     | Tipo de Dado    | Expressão Regular                         | Máscara               | Descrição                                                                 | Obrigatório | Único | Default               |
|-------------------|-----------------|--------------------------------------------|------------------------|---------------------------------------------------------------------------|-------------|-------|-----------------------|
| nome              | Texto            | ^[A-Za-zÀ-ÿ\s]{3,50}$                      | -                      | Nome completo do usuário, entre 3 e 50 caracteres.                        | Sim         | Não   | -                     |
| email             | Texto            | ^[\w\.-]+@[\w\.-]+\.\w{2,}$                | -                      | Endereço de e-mail válido e único no sistema.                             | Sim         | Sim   | -                     |
| perfil_acesso     | Texto            | ^(Administrador\|Operador\|Visualizador)$  | -                      | Perfil de acesso (Administrador, Operador ou Visualizador).               | Sim         | Não   | Visualizador          |
| status            | Booleano         | ^(ativo\|inativo)$                         | -                      | Indica se o usuário está ativo ou inativo no sistema.                     | Não         | Não   | ativo                 |
| data_criacao      | Data             | ^\d{2}-\d{2}-\d{4}$                        | dd/mm/aaaa              | Data em que o usuário foi cadastrado, gerado automaticamente.             | Sim         | Não   | Gerado pelo sistema   |
| ultima_alteracao  | DataHora         | ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$     | dd/mm/aaaa hh:mm:ss     | Data e hora da última modificação nos dados do usuário.                   | Não         | Não   | Atualizado automaticamente |
| criado_por        | Texto            | ^[A-Za-z0-9]{3,30}$                       | -                      | Identificador do administrador que cadastrou o usuário.                  | Sim         | Não   | Gerado pelo sistema   |

---
