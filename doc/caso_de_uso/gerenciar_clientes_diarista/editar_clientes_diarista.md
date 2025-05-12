| Nome do Caso de Uso       | Editar Cliente Diarista |
|---------------------------|--------------------------|
| *Descrição*               | Permite o administrador e o frentista alterar informações de cadastro de um cliente diarista. |
| *Ator Envolvido*          | Atendente |

| *Interação entre Ator e Sistema* | |
|----------------------------------|--------------------------------------------------------------------------|
| *Ator*                           | *Sistema*                                                               |
| Solicita editar informações de um cliente diarista | Exibe formulário com dados atuais preenchidos para edição. (RI09) |
| Altera informações desejadas (nome, telefone, e-mail, placa) | Sistema valida os campos obrigatórios e formato dos dados. (RN10, RN11, RI10) |
| Confirma a edição | Sistema atualiza as informações no cadastro do cliente e exibe mensagem de sucesso. (RI11) |

| *Exceções* |
|------------|
| EX08 - Dados inválidos (ex.: formato de CPF ou placa incorreto). Sistema exibe mensagem informando o erro. |
| EX09 - CPF duplicado (tentativa de alterar para CPF já existente). Sistema impede alteração e informa o erro. |
| EX10 - Falha ao salvar alterações. Sistema exibe mensagem de erro e solicita nova tentativa. |

| *Alternativas* |
|----------------|
| AL07 - Administrador e frentista pode cancelar a edição antes de confirmar, sem alterar os dados. |
| AL08 - Sistema permite apenas atualização parcial (ex.: apenas telefone ou e-mail). |
| AL09 - Sistema mantém histórico de alterações realizadas para auditoria. |

| *Regras de Negócio* |
|---------------------|
| RN10 - A placa deve ser validada conforme o padrão antigo ou Mercosul. |
| RN11 - O CPF deve permanecer único no sistema após a edição. |
| RN12 - Alterações devem registrar a data e o usuário que realizou a edição. |

| *Requisitos de Interface com o Usuário* |
|------------------------------------------|
| RI09 - Tela de edição deve apresentar os campos preenchidos para alteração. |
| RI10 - Campos obrigatórios devem ser destacados com asterisco (*) ou borda vermelha em caso de erro. |
| RI11 - Exibir mensagem de confirmação após edição concluída com sucesso. |

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara | Descrição | Obrigatório | Único | Default |
|---------------|--------------|-------------------|---------|-----------|-------------|-------|---------|
| nome          | Texto        | ^[A-Za-zÀ-ÿ\s]{3,50}$ | - | Nome completo do cliente. | Sim | Não | - |
| cpf           | Texto        | ^\d{3}\.\d{3}\.\d{3}-\d{2}$ | 000.000.000-00 | CPF do cliente. | Sim | Sim | - |
| telefone      | Texto        | ^\(\d{2}\)\s\d{4,5}-\d{4}$ | (00) 00000-0000 | Número de telefone do cliente. | Sim | Não | - |
| email         | Texto        | ^[\w\.-]+@[\w\.-]+\.\w{2,}$ | - | E-mail do cliente. | Não | Sim | - |
| placa         | Texto        | ^([A-Z]{3}-\d{4}or^([A-Z]{3}-\d{4} or [A-Z]{3}\d[A-Z]\d{2})$ | AAA-0000 ou AAA0A00 | Placa do veículo (modelo antigo ou Mercosul). | Sim | Sim | - |
| status        | Booleano     | ^(ativo \| inativo)$ | - | Indica se o cliente está ativo ou inativo. | Sim | Não | ativo |
| data_criacao  | Data          | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa | Data de cadastro do cliente. | Sim | Não | Gerado automaticamente |
| alterado_por  | Texto         | ^[A-Za-zÀ-ÿ\s]{3,50}$ | - | Nome do usuário que realizou a alteração. | Sim | Não | - |
| data_alteracao| Data          | ^\d{2}-\d{2}-\d{4}$ | dd/mm/aaaa | Data da última alteração do cadastro. | Sim | Não | Gerado automaticamente |
