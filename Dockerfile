# Usando imagem oficial do Python
FROM python:3.11-slim

# Evita criação de arquivos .pyc e buffer no output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório principal dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias (ex: para compilar psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Copia apenas o requirements primeiro (melhora cache)
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# Expõe a porta 8000 (documentação)
EXPOSE 8000

# Comando padrão: roda o Gunicorn na porta 8000, com diretório 'parkcontrol'
CMD ["gunicorn", "parkcontrol.wsgi:application", "--chdir", "parkcontrol", "--bind", "0.0.0.0:8000"]
