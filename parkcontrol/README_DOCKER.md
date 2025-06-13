# ParkControl – Ambiente de Desenvolvimento com Docker

Este repositório utiliza Docker para padronizar o ambiente de desenvolvimento do sistema **ParkControl**, garantindo que todos os colaboradores tenham uma experiência consistente sem precisar configurar dependências localmente.

---

## Requisitos

Antes de começar, certifique-se de ter instalado:

- [Docker](https://www.docker.com/)
- [Git](https://git-scm.com/)

---

## Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/parkcontrol.git
cd parkcontrol
````

### 2. Suba o container

```bash
docker-compose up --build
```

Esse comando irá:

* Construir a imagem do projeto com base no `Dockerfile`
* Instalar as dependências definidas em `requirements.txt`
* Iniciar o servidor Django em `http://localhost:8000`

---

## Acessar o Sistema

Após o build, abra no navegador:

```
http://localhost:8000
```

---

## Estrutura dos Arquivos Docker

| Arquivo              | Função                                                                 |
| -------------------- | ---------------------------------------------------------------------- |
| `Dockerfile`         | Define a imagem base, dependências e instruções de build               |
| `docker-compose.yml` | Orquestra os serviços (Django, banco, volumes, etc.)                   |
| `.env`               | Armazena variáveis sensíveis como `SECRET_KEY`                         |
| `.dockerignore`      | Lista de arquivos e pastas que não devem ser copiados para o container |

---

## Estrutura do Projeto

```text
parkcontrol/
│
├── apps/                        # Aplicações internas da plataforma
│   ├── usuarios/                # Autenticação e gestão de usuários
│   ├── frentistas/             # Entrada e saída de veículos
│   ├── clientes/               # Clientes mensalistas e diaristas
│   ├── planos/                 # Gestão de planos
│   ├── pagamentos/             # Cobranças e registros financeiros
│   ├── manutencao/             # Solicitações de manutenção de vagas
│   ├── relatorios/             # Relatórios financeiros e operacionais
│   ├── vagas/                  # Controle de vagas
│   └── core/                   # Utilitários e abstrações comuns
│
├── manage.py                   # Script de gerenciamento do Django
├── parkcontrol/                # Configurações globais do projeto
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # Rotas principais
│   ├── wsgi.py / asgi.py       # Gateways de aplicação
│
├── requirements.txt            # Lista de dependências
├── .env                        # Variáveis de ambiente (não subir para o Git)
├── Dockerfile                  # Configura imagem Docker da aplicação
├── docker-compose.yml          # Define os serviços, volumes e portas
└── docs/                       # Documentação técnica do projeto
```

---

## Comandos Úteis

### Acessar o container

```bash
docker exec -it parkcontrol_web bash
```

### Rodar migrações

```bash
docker exec -it parkcontrol_web python manage.py migrate
```

### Criar superusuário

```bash
docker exec -it parkcontrol_web python manage.py createsuperuser
```

---

## Convenção de Branches

Crie uma nova branch por funcionalidade:

```bash
git checkout -b feature/[app]-[descricao]
```

**Exemplos:**

* `feature/usuarios-registro`
* `feature/planos-crud`
* `feature/frentistas-entrada-saida`

---

## Variáveis de Ambiente (.env)

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

> Este arquivo **não deve ser versionado**, pois contém dados sensíveis.

---

## Fluxo para Atualizar o Container

### 1. Pare o container atual (se estiver rodando)

```bash
docker-compose down
```

### 2. Suba novamente com o rebuild

```bash
docker-compose up --build
```

> Use `--build` sempre que houver alterações em código ou dependências.

### 3. (Opcional) Rode migrações ou comandos dentro do container

```bash
docker exec -it parkcontrol_web python manage.py migrate
```

```bash
docker exec -it parkcontrol_web python manage.py createsuperuser
```

---

## Dicas

* Evite editar diretamente dentro do container. Faça alterações localmente e reconstrua.
* Use o `.env` para configurar senhas, chave secreta, e parâmetros de depuração.
* Mantenha seu container leve e estável. Não instale pacotes aleatórios dentro dele.

