| Nome do Caso de Uso       | Visualizar Cliente Diarista |
|---------------------------|-----------------------------|
| *Descrição*               | Permite o administrador e o frentista visualizar as informações dos clientes diaristas cadastrados. |
| *Ator Envolvido*          | Administrador e frentista |

| *Interação entre Ator e Sistema* | |
|----------------------------------|--------------------------------------------------------------------------|
| *Ator*                           | *Sistema*                                                               |
| Solicita a lista de clientes diaristas | Exibe a lista de clientes diaristas com nome, CPF, placa do veículo e status. (RI06) |
| Pesquisa cliente pelo nome ou CPF | Exibe resultados filtrados conforme o critério de busca. (AL04, RN07, RI07) |
| Seleciona um cliente para ver detalhes | Exibe informações completas do cliente: Nome, CPF, Telefone, E-mail, Placa, Status. (RI08) |

| *Exceções* |
|------------|
| EX05 - Nenhum cliente diarista encontrado. Sistema exibe mensagem: "Nenhum cliente encontrado para os critérios informados." |
| EX06 - Falha ao carregar lista de clientes. Sistema exibe mensagem de erro genérica e solicita nova tentativa. |
| EX07 - Sistema indisponível. Informa usuário que deve tentar novamente mais tarde. |

| *Alternativas* |
|----------------|
| AL04 - Administrador e frentista pode listar todos os clientes sem aplicar filtro. |
| AL05 - Administrador e pode refinar a busca utilizando apenas parte do nome ou CPF. |
| AL06 - Administrador e frentista pode ordenar a lista por nome ou data de cadastro. |

| *Regras de Negócio* |
|---------------------|
| RN07 - A pesquisa de clientes deve ser feita de forma insensível a maiúsculas/minúsculas. |
| RN08 - Resultados devem ser paginados para melhorar desempenho se houver muitos registros. |
| RN09 - Cliente diarista inativo também deve ser listado, mas destacado visualmente. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI06 - Tela de listagem deve apresentar nome, CPF, placa do veículo e status do cliente. |
| RI07 - Campo de pesquisa para nome e CPF deve permitir busca parcial. |
| RI08 - Tela de detalhes deve exibir todos os dados do cliente em modo somente leitura. |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara | Descrição | Obrigatório | Único | Default |
|---------------|--------------|-------------------|---------|-----------|-------------|-------|---------|
| nome          | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$ | - | Nome completo do cliente. | Sim | Não | - |
| cpf           | Texto        | ^\d{3}\.\d{3}\.\d{3}-\d{2}$ | 000.000.000-00 | CPF do cliente. | Sim | Sim | - |
| telefone      | Texto        | ^\(\d{2}\)\s\d{4,5}-\d{4}$ | (00) 00000-0000 | Número de telefone do cliente. | Sim | Não | - |
| email         | Texto        | ^[\w\.-]+@[\w\.-]+\.\w{2,}$ | - | E-mail do cliente. | Não | Sim | - |
| placa         | Texto        | ^([A-Z]{3}-\d{4} or [A-Z]{3}\d[A-Z]\d{2})$ | AAA-0000 ou AAA0A00 | Placa do veículo (antigo ou Mercosul). | Sim | Sim | - |
| status        | Booleano     | ^(ativo \| inativo)$ | - | Indica se o cliente está ativo ou inativo. | Sim | Não | ativo |
| data_criacao  | Data          | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa | Data de cadastro do cliente. | Sim | Não | Gerado automaticamente 
