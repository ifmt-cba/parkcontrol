# Usa a imagem oficial do Python 3.13
FROM python:3.13

# Define o diretório padrão do container
WORKDIR /app

# Copia todos os arquivos do projeto para dentro do container
COPY . /app

# Atualiza o pip e instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta 8000
EXPOSE 8000

# Comando padrão ao iniciar o container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
