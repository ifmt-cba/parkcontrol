# ParkControl – Sistema de Gestão de Estacionamentos

<div align="center">
  <img src="parkcontrol/static/images/logo.png" alt="Logo ParkControl" width="200"/>
</div>

---

O **ParkControl** é um sistema web desenvolvido para a gestão completa de estacionamentos, oferecendo controle eficiente sobre entradas e saídas de veículos, gerenciamento de clientes, planos e relatórios financeiros. O projeto foi concebido como parte da disciplina de **Engenharia de Software (2025/01)** do IFMT.

---

## Visão Geral do Produto

O ParkControl foi projetado para digitalizar e automatizar processos operacionais de estacionamentos de pequeno e médio porte. Sua interface simples e recursos robustos garantem que diferentes perfis de usuários consigam operar o sistema com segurança, clareza e rapidez.

---

## Funcionalidades Principais

- Registro de **entrada e saída** de veículos
- Controle em tempo real das **vagas** (livres, ocupadas e manutenção)
- Cadastro, visualização e edição de **clientes mensalistas e diaristas**
- Geração e gestão de **cobranças** e **recibos**
- Emissão de **relatórios financeiros** e de ocupação
- **Gestão de usuários** e permissões por perfil
- Solicitação e monitoramento de **manutenções de vaga**
- Recuperação e redefinição de **senhas**
- Navegação adaptada por **perfil de acesso**

---

## Perfis de Usuário

| Perfil        | Permissões Principais |
|---------------|------------------------|
| **Administrador** | Gerencia usuários, planos, solicitações de manutenção e tem acesso total ao sistema |
| **Frentista**     | Realiza controle de entrada/saída de veículos, cadastra clientes e solicita manutenções |
| **Contador**      | Visualiza relatórios, acompanha inadimplência e realiza cobranças |
| **TI (Futuro)**   | Destinado à manutenção técnica e controle de segurança do sistema |

---

## Tecnologias Utilizadas

- **Linguagem Backend**: Python 3.11
- **Framework Web**: Django
- **Banco de Dados**: SQLite (com possibilidade de migração para PostgreSQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Versionamento**: Git + GitHub Projects (Kanban + Sprints)
- **Modelagem e Prototipação**:
  - Figma – Prototipação de Telas
  - BPMN.IO – Modelagem de Processos
  - Lucidchart – Diagrama de Casos de Uso
  - Mermaid.js – Diagrama de Classes

---

## Estrutura da Documentação

A documentação completa do projeto está disponível na pasta [`/DOC`](./DOC), incluindo:

- Documento de Visão de Produto
- Cronograma de Desenvolvimento (Sprints)
- Casos de Uso detalhados
- Diagrama de Classes
- Diagrama de Processo (BPMN)
- Protótipos de Telas
- Arquitetura de Software
- Checklist das Etapas do Scrum

---

## Como Executar o Projeto

> Instruções completas de instalação e execução do ambiente estão no arquivo [`README_DOCKER.md`](./README_DOCKER.md) e `docker-compose.yml`.

---

## Equipe de Desenvolvimento

| Nome             | GitHub                                       |
|------------------|----------------------------------------------|
| Emmylly Maria    | [@emmyllydev](https://github.com/emmyllydev) |
| Fábio Júnior     | [@Fabio-jr-SM](https://github.com/Fabio-jr-SM) |
| Filomena Soares  | [@filomenasoares](https://github.com/filomenasoares) |
| Karla Viethia    | [@belokarla7](https://github.com/belokarla7) |
| Maria Clara      | [@Giraldellis](https://github.com/Giraldellis) |
| Pedro Lucas      | [@pedrolucasS86](https://github.com/pedrolucasS86) |

---

## Licença

Este é um projeto de caráter acadêmico, sem fins comerciais, licenciado apenas para uso educacional.

---
